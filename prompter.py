import sys
import json
import requests
import keyboard

from time import sleep, time
from threading import Thread
from utils.logger import COLORS, RESET, logger
from transcriber import (
    LiveTranscriber,
    TranscriberConfig,
)


class AgentPrompter(LiveTranscriber):
    def __init__(self, config: TranscriberConfig, llm_model: str = "gemma3"):
        super().__init__(config)
        self.llm_model = llm_model
        self.llm_toggle = True
        start_hotkey_listener(self)

    def get_agent_stream(self, prompt: str):
        prompt = f"PLEASE ANSWER AS BRIEFLY AND CONCISELY AS POSSIBLE: {prompt}"
        try:
            with requests.post(
                "http://localhost:11434/api/generate",
                json={"model": self.llm_model, "prompt": prompt, "stream": True},
                stream=True,
                timeout=60,
            ) as r:
                r.raise_for_status()
                for raw_line in r.iter_lines():
                    if not raw_line:
                        continue
                    if isinstance(raw_line, bytes):
                        raw_line = raw_line.decode("utf-8")

                    try:
                        data = json.loads(raw_line)
                    except json.JSONDecodeError:
                        continue

                    if "response" in data:
                        yield data["response"]  # yield chunk

                    if data.get("done", False):
                        break
        except Exception as e:
            logger.error(f"Error contacting Ollama: {e}")
            yield "[Error contacting Ollama]"

    def commit_final(self, text: str) -> None:
        final_text = text.strip()
        # End the [Partial] line cleanly
        sys.stdout.write("\r\033[K")
        sys.stdout.flush()
        sys.stdout.write(f"{COLORS['USER']}[User] {final_text}\n{RESET}")
        sys.stdout.flush()

        if not self.llm_toggle:
            logger.info("[Agent] Skipping Ollama request (not in context mode)")
            return

        sys.stdout.write(f"{COLORS['AGENT']}[Agent] Thinking...{RESET}")
        sys.stdout.flush()

        start_time = time()
        response_time = 0
        first_chunk = True

        for chunk in self.get_agent_stream(final_text):
            if first_chunk:
                # Clear the thinking line and print agent prefix
                sys.stdout.write("\r\033[K")
                sys.stdout.write(f"{COLORS['AGENT']}[Agent] ")
                sys.stdout.flush()
                response_time = time() - start_time
                first_chunk = False

            # Stream to terminal
            sys.stdout.write(chunk)
            sys.stdout.flush()
            # Typing delay
            sleep(0.05)

        sys.stdout.write(f"{RESET}\n")
        sys.stdout.flush()

        logger.info(f"Agent response time: {response_time:.2f} seconds")


def start_hotkey_listener(transcriber: AgentPrompter):
    """Run keyboard listening in a background thread"""

    def toggle():
        transcriber.llm_toggle = not transcriber.llm_toggle
        state = "ENABLED" if transcriber.llm_toggle else "DISABLED"
        logger.info(f"[Hotkey] In-context mode {state}")

    Thread(target=lambda: keyboard.add_hotkey("ctrl+alt", toggle), daemon=True).start()


if __name__ == "__main__":
    config = TranscriberConfig(device_name="Microphone")
    transcriber = AgentPrompter(config)
    transcriber.run()
