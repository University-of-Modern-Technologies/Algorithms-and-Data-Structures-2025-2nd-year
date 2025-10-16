"""
Physics engine and collision detection.

Handles all collision detection with multiple algorithms (AABB, ellipse, circle).
"""

from dataclasses import dataclass
from enum import Enum
from typing import List, Tuple

from game.domain.entities import Position, Size


class CollisionType(Enum):
    """Types of collisions."""

    NONE = "none"
    ENEMY_PROJECTILE = "enemy_projectile"
    PLAYER_ENEMY = "player_enemy"
    PLAYER_PROJECTILE = "player_projectile"
    PROJECTILE_SHIELD = "projectile_shield"
    PLAYER_PROJECTILE_SHIELD = "player_projectile_shield"


@dataclass
class Rect:
    """Axis-aligned bounding box (AABB)."""

    x: float
    y: float
    width: float
    height: float

    @staticmethod
    def from_position_size(pos: Position, size: Size) -> "Rect":
        """Create rect from position and size."""
        return Rect(pos.x, pos.y, size.width, size.height)

    def right(self) -> float:
        """Right edge x-coordinate."""
        return self.x + self.width

    def bottom(self) -> float:
        """Bottom edge y-coordinate."""
        return self.y + self.height

    def center_x(self) -> float:
        """Center x-coordinate."""
        return self.x + self.width / 2

    def center_y(self) -> float:
        """Center y-coordinate."""
        return self.y + self.height / 2


@dataclass
class Circle:
    """Circle defined by center position and radius."""

    x: float
    y: float
    radius: float

    @staticmethod
    def from_rect(rect: Rect) -> "Circle":
        """Create circle from rect (center with radius half of smaller dimension)."""
        radius = min(rect.width, rect.height) / 2
        return Circle(rect.center_x(), rect.center_y(), radius)


@dataclass
class Ellipse:
    """Ellipse defined by center, semi-major and semi-minor axes."""

    x: float
    y: float
    half_width: float
    half_height: float

    @staticmethod
    def from_rect(rect: Rect) -> "Ellipse":
        """Create ellipse from rect."""
        return Ellipse(
            rect.center_x(), rect.center_y(), rect.width / 2, rect.height / 2
        )


class CollisionDetector:
    """Detects collisions between game entities."""

    @staticmethod
    def check_aabb_aabb(rect1: Rect, rect2: Rect) -> bool:
        """Check if two axis-aligned bounding boxes collide (AABB).
        
        This is the fastest collision check, suitable for most entities.
        """
        return (
            rect1.x < rect2.right()
            and rect1.right() > rect2.x
            and rect1.y < rect2.bottom()
            and rect1.bottom() > rect2.y
        )

    @staticmethod
    def check_circle_circle(circle1: Circle, circle2: Circle) -> bool:
        """Check if two circles collide.
        
        Useful for projectiles and small entities.
        """
        dx = circle1.x - circle2.x
        dy = circle1.y - circle2.y
        distance_sq = dx * dx + dy * dy
        min_distance_sq = (circle1.radius + circle2.radius) ** 2
        return distance_sq < min_distance_sq

    @staticmethod
    def check_circle_aabb(circle: Circle, rect: Rect) -> bool:
        """Check if circle collides with axis-aligned bounding box.
        
        Finds closest point on rect to circle center.
        """
        # Find closest point on rect to circle center
        closest_x = max(rect.x, min(circle.x, rect.right()))
        closest_y = max(rect.y, min(circle.y, rect.bottom()))

        # Calculate distance from circle center to closest point
        dx = circle.x - closest_x
        dy = circle.y - closest_y
        distance_sq = dx * dx + dy * dy

        return distance_sq < circle.radius ** 2

    @staticmethod
    def check_ellipse_circle(ellipse: Ellipse, circle: Circle) -> bool:
        """Check if ellipse collides with circle.
        
        Uses iterative approximation for accuracy.
        Useful for player ship (ellipse) vs projectiles (circles).
        """
        # Translate circle to ellipse center
        dx = circle.x - ellipse.x
        dy = circle.y - ellipse.y

        # Approximate ellipse-circle collision
        # Using point-on-ellipse distance formula
        a = ellipse.half_width
        b = ellipse.half_height

        # Normalize by ellipse semi-axes
        x = abs(dx) / a
        y = abs(dy) / b

        # If inside ellipse, definitely colliding
        if x <= 1 and y <= 1:
            return True

        # Find closest point on ellipse to circle center
        # Using iterative approach (1 iteration is usually enough)
        if x > 1 or y > 1:
            t = max(x, y)
            closest_x = (dx / t) if t > 0 else 0
            closest_y = (dy / t) if t > 0 else 0

            # Scale back to world coordinates
            closest_x = closest_x / a * a
            closest_y = closest_y / b * b

            dist_x = dx - closest_x
            dist_y = dy - closest_y
            distance_sq = dist_x * dist_x + dist_y * dist_y

            return distance_sq < circle.radius ** 2

        return False

    @staticmethod
    def check_projectile_screen_bounds(
        pos: Position, size: Size, screen_width: float, screen_height: float
    ) -> bool:
        """Check if projectile is out of screen bounds.
        
        Returns True if projectile is completely outside screen.
        """
        return (
            pos.x + size.width < 0
            or pos.x >= screen_width
            or pos.y + size.height < 0
            or pos.y >= screen_height
        )

    @staticmethod
    def check_rect_screen_bounds(
        rect: Rect, screen_width: float, screen_height: float
    ) -> bool:
        """Check if rect is completely out of screen bounds."""
        return (
            rect.right() < 0 or rect.x > screen_width or rect.bottom() < 0 or rect.y > screen_height
        )

    @staticmethod
    def clamp_rect_to_screen(
        rect: Rect, screen_width: float, screen_height: float
    ) -> Rect:
        """Clamp rect position to stay within screen bounds."""
        new_rect = Rect(rect.x, rect.y, rect.width, rect.height)

        if new_rect.x < 0:
            new_rect.x = 0
        if new_rect.right() > screen_width:
            new_rect.x = screen_width - new_rect.width

        if new_rect.y < 0:
            new_rect.y = 0
        if new_rect.bottom() > screen_height:
            new_rect.y = screen_height - new_rect.height

        return new_rect

    @staticmethod
    def get_overlap_amount(rect1: Rect, rect2: Rect) -> Tuple[float, float]:
        """Get amount of overlap between two rects.
        
        Returns (x_overlap, y_overlap) in pixels.
        """
        x_overlap = min(rect1.right(), rect2.right()) - max(rect1.x, rect2.x)
        y_overlap = min(rect1.bottom(), rect2.bottom()) - max(rect1.y, rect2.y)

        return (max(0, x_overlap), max(0, y_overlap))
