import logging
import warnings

# Suppress specific warning
warnings.filterwarnings(
    "ignore", category=UserWarning, message=r".*pkg_resources is deprecated as an API.*"
)


# ANSI color codes
RESET = "\033[0m"
COLORS = {
    "USER": "\033[92m",  # Green
    "AGENT": "\033[94m",  # Blue
    "TRANSCRIBER": "\033[96m",  # Cyan
    "HOTKEY": "\033[95m",  # Magenta
    "INFO": "\033[37m",  # White (default info)
    "WARNING": "\033[93m",  # Yellow
    "ERROR": "\033[91m",  # Red
}


class ColorFormatter(logging.Formatter):
    def format(self, record):
        message = record.getMessage()

        # Choose colors by detecting tags
        if message.startswith("[User]"):
            color = COLORS["USER"]
        elif message.startswith("[Agent]"):
            color = COLORS["AGENT"]
        elif message.startswith("[Transcriber]"):
            color = COLORS["TRANSCRIBER"]
        elif message.startswith("[Hotkey]"):
            color = COLORS["HOTKEY"]
        else:
            color = COLORS.get(record.levelname, COLORS["INFO"])

        record.msg = f"{color}{message}{RESET}"
        return super().format(record)


# Logger setup
logger = logging.getLogger("responsive_ai")
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setFormatter(
    ColorFormatter(fmt="%(asctime)s | %(levelname)s | %(message)s", datefmt="%H:%M:%S")
)

logger.addHandler(console_handler)

# Suppress noisy logs from faster_whisper
logging.getLogger("faster_whisper").setLevel(logging.WARNING)
