import sys
import time
import queue
import signal
import torch
import numpy as np
import sounddevice as sd

from threading import Thread
from datetime import datetime
from typing import List
from faster_whisper import WhisperModel

from config import TranscriberConfig
from utils.logger import logger
from utils.audio import get_device_index, normalize


# -------------------------
# Live Transcriber Class
# -------------------------
class LiveTranscriber:
    def __init__(self, config: TranscriberConfig):
        self.config = config
        self.device_index = get_device_index(config.device_name)

        # Buffers
        self.audio_queue: queue.Queue[np.ndarray] = queue.Queue()
        self.speech_frames: List[float] = []
        self.in_speech = False
        self.last_partial_time = time.time()

        # Load ASR model
        self.whisper = WhisperModel(
            config.model_size, device="auto", compute_type=config.compute_type
        )

        # Load VAD model
        self.vad_model, utils = torch.hub.load(
            "snakers4/silero-vad", model="silero_vad"
        )
        _, _, _, self.VADIterator, _ = utils
        self.vad_iterator = self.VADIterator(
            self.vad_model,
            threshold=config.vad_threshold,
            min_silence_duration_ms=config.min_silence_duration_ms,
        )

        logger.info(f"Models loaded. Using device: {config.device_name}")

    # -------------------------
    # Audio Capture
    # -------------------------
    def audio_callback(self, indata, frames, time_info, status):
        """Callback from sounddevice — push audio frames into queue."""
        if status:
            logger.warning(f"Audio callback status: {status}")
        self.audio_queue.put(indata[:, 0].copy())  # mono

    def start_audio_capture(self) -> None:
        """Start capturing audio from microphone in separate thread."""
        with sd.InputStream(
            samplerate=self.config.sample_rate,
            blocksize=self.config.block_size,
            device=self.device_index,
            channels=1,
            dtype="float32",
            callback=self.audio_callback,
        ):
            logger.info("🎙️ Listening...")
            while True:
                time.sleep(0.01)

    # -------------------------
    # Processing Utilities
    # -------------------------
    def transcribe_audio(self, audio: np.ndarray, beam: int) -> str:
        """Run ASR on audio sample."""
        audio = normalize(audio)
        if len(audio) / self.config.sample_rate < 0.3:
            return ""
        segments, _ = self.whisper.transcribe(audio, beam_size=beam, language="en")
        return " ".join(s.text.strip() for s in segments if s.text.strip())

    def print_partial_inline(self, text: str) -> None:
        words = text.strip().split()
        context = " ".join(words[-self.config.partial_word_context :])
        sys.stdout.write("\r\033[K[Partial] " + context)
        sys.stdout.flush()

    def commit_final(self, text: str) -> None:
        """Outputs final transcript to stdout and file."""
        final_text = text.strip()
        sys.stdout.write("\r\033[K[Final] " + final_text + "\n")
        sys.stdout.flush()

        with open(self.config.transcript_file, "a", encoding="utf-8") as f:
            f.write(f"{datetime.now():%Y-%m-%d %H:%M:%S} {final_text}\n")

    # -------------------------
    # Main Transcription Loop
    # -------------------------
    def process_audio_stream(self) -> None:
        """Main loop for handling VAD and transcription."""
        vad_buffer = np.array([], dtype=np.float32)

        while True:
            chunk = self.audio_queue.get()
            vad_buffer = np.append(vad_buffer, chunk)

            while len(vad_buffer) >= self.config.block_size:
                frame = vad_buffer[: self.config.block_size]
                vad_buffer = vad_buffer[self.config.block_size :]

                speech_event = self.vad_iterator(
                    torch.from_numpy(frame), return_seconds=False
                )

                if speech_event and "start" in speech_event:
                    self.speech_frames.clear()
                    self.in_speech = True
                    self.last_partial_time = time.time()

                if self.in_speech:
                    self.speech_frames.extend(frame)

                    if (
                        time.time() - self.last_partial_time
                        >= self.config.partial_interval
                    ):
                        partial = self.transcribe_audio(
                            np.array(self.speech_frames), beam=1
                        )
                        if partial:
                            self.print_partial_inline(partial)
                        self.last_partial_time = time.time()

                if speech_event and "end" in speech_event and self.in_speech:
                    final_text = self.transcribe_audio(
                        np.array(self.speech_frames), beam=2
                    )
                    if final_text:
                        self.commit_final(final_text)
                    self.speech_frames.clear()
                    self.in_speech = False

    def run(self) -> None:
        """Run the live transcriber."""
        signal.signal(signal.SIGINT, self._handle_exit)  # graceful exit on Ctrl+C
        Thread(target=self.start_audio_capture, daemon=True).start()
        self.process_audio_stream()

    @staticmethod
    def _handle_exit(signum, frame):
        logger.info("\n🛑 Stopping transcriber...")
        sys.exit(0)


# -------------------------
# Main Entry Point
# -------------------------
if __name__ == "__main__":
    config = TranscriberConfig(device_name="Microphone")
    LiveTranscriber(config).run()
