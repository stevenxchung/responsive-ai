from dataclasses import dataclass


@dataclass
class TranscriberConfig:
    device_name: str = "CABLE Output"
    partial_interval: float = 1.5
    sample_rate: int = 16_000
    model_size: str = "small"
    compute_type: str = "float16"
    vad_threshold: float = 0.5
    transcript_file: str = "transcript.log"
    block_size: int = 512
    min_silence_duration_ms: int = 1500  # Wait time before committing
    partial_word_context: int = 8  # Words to show during partial transcription
