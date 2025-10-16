"""
Logging infrastructure for the game.

Handles all logging operations, writing to logs/game.log file.
"""

import logging
import sys
from pathlib import Path
from typing import Optional


class Logger:
    """Simple logger wrapper for game events."""

    _instance: Optional["Logger"] = None
    _logger: Optional[logging.Logger] = None

    def __new__(cls) -> "Logger":
        """Implement singleton pattern."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self) -> None:
        """Initialize the logger."""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        log_file = log_dir / "game.log"

        # Create logger
        self._logger = logging.getLogger("space_invaders")
        self._logger.setLevel(logging.INFO)

        # File handler
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(logging.INFO)

        # Console handler (only for errors)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.ERROR)

        # Formatter
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add handlers
        self._logger.addHandler(file_handler)
        self._logger.addHandler(console_handler)

    def info(self, message: str) -> None:
        """Log info message."""
        if self._logger:
            self._logger.info(message)

    def error(
        self, message: str, exc: Optional[Exception] = None
    ) -> None:
        """Log error message."""
        if self._logger:
            if exc:
                self._logger.error(message, exc_info=exc)
            else:
                self._logger.error(message)

    def debug(self, message: str) -> None:
        """Log debug message."""
        if self._logger:
            self._logger.debug(message)

    def warning(self, message: str) -> None:
        """Log warning message."""
        if self._logger:
            self._logger.warning(message)
