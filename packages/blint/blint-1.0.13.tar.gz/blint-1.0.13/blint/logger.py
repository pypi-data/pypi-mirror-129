import logging
import os

from rich.console import Console
from rich.logging import RichHandler
from rich.theme import Theme

custom_theme = Theme({"info": "cyan", "warning": "purple4", "danger": "bold red"})
console = Console(
    log_time=False,
    log_path=False,
    theme=custom_theme,
    width=200,
    color_system="256",
    force_terminal=True,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[
        RichHandler(
            console=console, markup=True, show_path=False, enable_link_path=False
        )
    ],
)
LOG = logging.getLogger(__name__)

# Set logging level
if os.getenv("SCAN_DEBUG_MODE") == "debug":
    LOG.setLevel(logging.DEBUG)

DEBUG = logging.DEBUG
