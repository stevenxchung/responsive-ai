import sys
import requests
import keyboard

from time import time
from threading import Thread
from utils.logger import logger
from transcriber import (
    LiveTranscriber,
    TranscriberConfig,
)


def start_hotkey_listener(transcriber):
    """Run keyboard listening in a background thread"""

    def toggle():
        transcriber.in_context = not transcriber.in_context
        state = "ENABLED" if transcriber.in_context else "DISABLED"
        logger.info(f"[Hotkey] In-context mode {state}")

    Thread(target=lambda: keyboard.add_hotkey("ctrl+alt", toggle), daemon=True).start()


class LiveTranscriberWithLLM(LiveTranscriber):
    def __init__(self, config: TranscriberConfig, llm_model: str = "gemma3"):
        super().__init__(config)
        self.llm_model = llm_model
        self.in_context = True
        start_hotkey_listener(self)

    def query_ollama(self, prompt: str) -> str:
        prompt = f"PLEASE ANSWER AS BRIEFLY AND CONCISELY AS POSSIBLE: {prompt}"
        try:
            r = requests.post(
                "http://localhost:11434/api/generate",
                json={"model": self.llm_model, "prompt": prompt, "stream": False},
                timeout=60,
            )
            r.raise_for_status()
            data = r.json()
            return data.get("response", "").strip()
        except Exception as e:
            logger.error(f"Error contacting Ollama: {e}")
            return "[Error contacting Ollama]"

    def commit_final(self, text: str) -> None:
        # First: Log the final transcript
        final_text = text.strip()
        # End the partial line cleanly
        sys.stdout.write("\r\033[K")
        sys.stdout.flush()
        logger.info(f"[User] {final_text}")

        if not self.in_context:
            logger.info("[LLM] Skipping Ollama request (not in context mode)")
            return

        # Then: Query Ollama and log response
        logger.info("[LLM] Querying Ollama...")
        start = time()
        response = self.query_ollama(final_text)
        logger.info(f"[LLM Response] {response}")
        logger.info(f"Response time: {time() - start} seconds")


if __name__ == "__main__":
    config = TranscriberConfig(device_name="Microphone")
    transcriber = LiveTranscriberWithLLM(config)
    transcriber.run()
