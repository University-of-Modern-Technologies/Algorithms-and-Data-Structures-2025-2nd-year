"""
Game state management and difficulty parameters.

Handles global game state, transitions between states, and difficulty settings.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class GameStateEnum(Enum):
    """Possible game states."""

    MENU = "menu"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"
    SETTINGS = "settings"


class Difficulty(Enum):
    """Difficulty levels."""

    EASY = "easy"
    NORMAL = "normal"
    HARD = "hard"


@dataclass
class DifficultyParams:
    """Game difficulty parameters."""

    enemy_speed: float
    enemy_fire_rate: float  # shots per second
    enemy_fire_probability: float  # 0.0 to 1.0
    enemy_hp: int
    player_hp: int
    wave_count: int

    @staticmethod
    def create(difficulty: Difficulty) -> "DifficultyParams":
        """Create difficulty parameters based on level."""
        if difficulty == Difficulty.EASY:
            return DifficultyParams(
                enemy_speed=30.0,
                enemy_fire_rate=1.0,
                enemy_fire_probability=0.3,
                enemy_hp=1,
                player_hp=3,
                wave_count=3,
            )
        elif difficulty == Difficulty.NORMAL:
            return DifficultyParams(
                enemy_speed=50.0,
                enemy_fire_rate=2.0,
                enemy_fire_probability=0.5,
                enemy_hp=1,
                player_hp=2,
                wave_count=5,
            )
        else:  # HARD
            return DifficultyParams(
                enemy_speed=80.0,
                enemy_fire_rate=3.0,
                enemy_fire_probability=0.7,
                enemy_hp=2,
                player_hp=1,
                wave_count=7,
            )

    def increase_difficulty(self, factor: float = 1.1) -> None:
        """Increase difficulty parameters."""
        self.enemy_speed *= factor
        self.enemy_fire_rate *= factor
        self.enemy_fire_probability = min(1.0, self.enemy_fire_probability * factor)


@dataclass
class GameState:
    """Global game state.
    
    Contains all mutable state of the game session.
    """

    state: GameStateEnum
    difficulty: Difficulty
    difficulty_params: DifficultyParams
    score: int = 0
    high_score: int = 0
    lives: int = 1
    current_wave: int = 0
    screen_width: float = 1280
    screen_height: float = 720
    paused_at: Optional[float] = None

    @staticmethod
    def create_new(difficulty: Difficulty) -> "GameState":
        """Create new game session."""
        params = DifficultyParams.create(difficulty)
        return GameState(
            state=GameStateEnum.PLAYING,
            difficulty=difficulty,
            difficulty_params=params,
            score=0,
            lives=params.player_hp,
            current_wave=0,
        )

    def add_score(self, points: int) -> None:
        """Add points to score."""
        self.score += points
        if self.score > self.high_score:
            self.high_score = self.score

    def lose_life(self) -> None:
        """Player loses a life."""
        self.lives -= 1
        if self.lives <= 0:
            self.state = GameStateEnum.GAME_OVER

    def next_wave(self) -> None:
        """Progress to next wave."""
        self.current_wave += 1
        self.difficulty_params.increase_difficulty()

    def is_game_over(self) -> bool:
        """Check if game is over."""
        return self.state == GameStateEnum.GAME_OVER or self.lives <= 0

    def pause(self, current_time: float) -> None:
        """Pause the game."""
        if self.state == GameStateEnum.PLAYING:
            self.state = GameStateEnum.PAUSED
            self.paused_at = current_time

    def resume(self) -> None:
        """Resume the game."""
        if self.state == GameStateEnum.PAUSED:
            self.state = GameStateEnum.PLAYING
            self.paused_at = None

    def toggle_pause(self, current_time: float) -> None:
        """Toggle pause state."""
        if self.state == GameStateEnum.PLAYING:
            self.pause(current_time)
        elif self.state == GameStateEnum.PAUSED:
            self.resume()
