"""
Game domain entities.

Core business logic models independent from pygame and UI.
All classes are pure data structures with methods for game mechanics.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


class EntityType(Enum):
    """Types of entities in the game."""

    PLAYER = "player"
    ENEMY = "enemy"
    PROJECTILE = "projectile"
    SHIELD = "shield"
    BONUS_SHIP = "bonus_ship"


@dataclass
class Position:
    """Entity position in world coordinates."""

    x: float
    y: float

    def distance_to(self, other: "Position") -> float:
        """Calculate Euclidean distance to another position."""
        dx = self.x - other.x
        dy = self.y - other.y
        return (dx * dx + dy * dy) ** 0.5


@dataclass
class Velocity:
    """Entity velocity in pixels per second."""

    vx: float
    vy: float


@dataclass
class Size:
    """Entity dimensions in pixels."""

    width: float
    height: float


@dataclass
class Player:
    """Player-controlled ship.
    
    Lives at the bottom of the screen, can move left/right and shoot.
    """

    entity_id: int
    position: Position
    velocity: Velocity
    size: Size
    hp: int = 1
    max_hp: int = 1
    shields: List["Shield"] = field(default_factory=list)

    def take_damage(self, damage: int) -> None:
        """Take damage, reduce HP."""
        self.hp = max(0, self.hp - damage)

    def is_alive(self) -> bool:
        """Check if player is still alive."""
        return self.hp > 0


@dataclass
class Enemy:
    """Enemy ship.
    
    Moves in formation, shoots at random intervals.
    """

    entity_id: int
    position: Position
    velocity: Velocity
    size: Size
    hp: int = 1
    max_hp: int = 1
    enemy_type: str = "standard"
    animation_frame: int = 0
    last_shot_time: float = 0.0

    def take_damage(self, damage: int) -> None:
        """Take damage, reduce HP."""
        self.hp = max(0, self.hp - damage)

    def is_alive(self) -> bool:
        """Check if enemy is still alive."""
        return self.hp > 0


@dataclass
class Projectile:
    """Bullet fired by player or enemy.
    
    Travels in a straight line until collision or screen edge.
    """

    entity_id: int
    position: Position
    velocity: Velocity
    size: Size
    owner_type: EntityType  # PLAYER or ENEMY
    damage: int = 1
    lifetime: float = 10.0  # Max time in seconds
    age: float = 0.0

    def update_age(self, dt: float) -> None:
        """Update projectile age."""
        self.age += dt

    def is_expired(self) -> bool:
        """Check if projectile has exceeded lifetime."""
        return self.age >= self.lifetime


@dataclass
class ShieldSegment:
    """Single segment of a shield.
    
    Shields are made up of 4x4 grid of segments.
    """

    position: Position
    size: Size
    hp: int = 1
    max_hp: int = 1

    def is_destroyed(self) -> bool:
        """Check if segment is destroyed."""
        return self.hp <= 0

    def take_damage(self, damage: int) -> None:
        """Damage this segment."""
        self.hp = max(0, self.hp - damage)


@dataclass
class Shield:
    """Shield block that protects the player.
    
    Made up of 4x4 grid of segments. Each segment can be destroyed.
    """

    entity_id: int
    position: Position
    segments: List[ShieldSegment] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Initialize shield segments if not provided."""
        if not self.segments:
            self._create_segments()

    def _create_segments(self) -> None:
        """Create 4x4 grid of shield segments."""
        segment_size = 5  # pixels
        for row in range(4):
            for col in range(4):
                seg_x = self.position.x + col * segment_size
                seg_y = self.position.y + row * segment_size
                segment = ShieldSegment(
                    position=Position(seg_x, seg_y),
                    size=Size(segment_size, segment_size),
                )
                self.segments.append(segment)

    def take_damage(self, position: Position, damage: int) -> None:
        """Damage segments near given position."""
        for segment in self.segments:
            # Check if projectile hit this segment
            dist = position.distance_to(segment.position)
            if dist < 10:  # Simple radius check
                segment.take_damage(damage)

    def count_destroyed_segments(self) -> int:
        """Count how many segments are destroyed."""
        return sum(1 for seg in self.segments if seg.is_destroyed())

    def is_completely_destroyed(self) -> bool:
        """Check if all segments are destroyed."""
        return self.count_destroyed_segments() == len(self.segments)


@dataclass
class BonusShip:
    """Rare bonus ship that flies across the top.
    
    Appears infrequently, worth high score if destroyed.
    """

    entity_id: int
    position: Position
    velocity: Velocity
    size: Size
    hp: int = 1
    max_hp: int = 1
    bonus_value: int = 200

    def take_damage(self, damage: int) -> None:
        """Take damage."""
        self.hp = max(0, self.hp - damage)

    def is_alive(self) -> bool:
        """Check if bonus ship is alive."""
        return self.hp > 0


@dataclass
class Wave:
    """Group of enemies forming a wave.
    
    Enemies move together as a unit, bouncing off screen edges.
    """

    wave_number: int
    enemies: List[Enemy] = field(default_factory=list)
    direction: int = 1  # 1 for right, -1 for left
    velocity: Velocity = field(default_factory=lambda: Velocity(50, 0))
    drop_distance: float = 10.0  # Drop down when hitting edge

    def update_positions(self, dt: float, screen_width: float) -> bool:
        """Update wave movement. Returns True if wave hit screen edge."""
        for enemy in self.enemies:
            enemy.position.x += self.velocity.vx * self.direction * dt
            enemy.position.y += self.velocity.vy * dt

        # Check if any enemy hit screen edge
        hit_edge = False
        for enemy in self.enemies:
            if enemy.position.x <= 0 or enemy.position.x + enemy.size.width >= screen_width:
                hit_edge = True
                break

        if hit_edge:
            # Change direction and drop down
            self.direction *= -1
            for enemy in self.enemies:
                enemy.position.y += self.drop_distance

        return hit_edge

    def count_alive(self) -> int:
        """Count alive enemies in wave."""
        return sum(1 for e in self.enemies if e.is_alive())

    def all_destroyed(self) -> bool:
        """Check if all enemies are destroyed."""
        return self.count_alive() == 0

    def increase_speed(self, factor: float = 1.1) -> None:
        """Increase wave speed when enemies are destroyed."""
        self.velocity.vx *= factor
