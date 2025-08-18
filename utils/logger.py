import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%H:%M:%S",
)

logger = logging.getLogger("responsive_ai")
# Suppressing noisy logs from faster_whisper
logging.getLogger("faster_whisper").setLevel(logging.WARNING)
