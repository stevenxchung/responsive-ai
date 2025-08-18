import sounddevice as sd
import numpy as np


def normalize(audio: np.ndarray) -> np.ndarray:
    peak = np.max(np.abs(audio))
    return audio / peak * 0.9 if peak > 0 else audio


def get_device_index(name: str, for_input: bool = True) -> int:
    """Finds the input/output audio device index by name."""
    for idx, dev in enumerate(sd.query_devices()):
        if name.lower() in dev["name"].lower():
            if for_input and dev["max_input_channels"] > 0:
                return idx
            if not for_input and dev["max_output_channels"] > 0:
                return idx
    raise ValueError(
        f"No {'input' if for_input else 'output'} device found for '{name}'"
    )
