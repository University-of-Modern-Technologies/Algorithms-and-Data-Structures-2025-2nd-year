"""
Unit tests for physics collision detection.

Tests AABB, circle, and ellipse collision detection algorithms.
"""

import pytest

from game.core.physics import (
    Circle,
    CollisionDetector,
    Ellipse,
    Rect,
)


class TestAABB:
    """Test axis-aligned bounding box collision detection."""

    def test_aabb_aabb_overlapping(self) -> None:
        """Test AABB collision with overlapping rectangles."""
        rect1 = Rect(0, 0, 10, 10)
        rect2 = Rect(5, 5, 10, 10)
        assert CollisionDetector.check_aabb_aabb(rect1, rect2)

    def test_aabb_aabb_not_overlapping(self) -> None:
        """Test AABB collision with non-overlapping rectangles."""
        rect1 = Rect(0, 0, 10, 10)
        rect2 = Rect(20, 20, 10, 10)
        assert not CollisionDetector.check_aabb_aabb(rect1, rect2)

    def test_aabb_aabb_touching(self) -> None:
        """Test AABB collision with touching edge."""
        rect1 = Rect(0, 0, 10, 10)
        rect2 = Rect(10, 0, 10, 10)
        # Touching edge should not collide (strict inequality)
        assert not CollisionDetector.check_aabb_aabb(rect1, rect2)

    def test_aabb_aabb_inside(self) -> None:
        """Test AABB collision with one inside another."""
        rect1 = Rect(0, 0, 20, 20)
        rect2 = Rect(5, 5, 5, 5)
        assert CollisionDetector.check_aabb_aabb(rect1, rect2)

    def test_aabb_aabb_partial_overlap_horizontal(self) -> None:
        """Test AABB collision with partial horizontal overlap."""
        rect1 = Rect(0, 0, 15, 10)
        rect2 = Rect(10, 0, 15, 10)
        assert CollisionDetector.check_aabb_aabb(rect1, rect2)

    def test_aabb_aabb_partial_overlap_vertical(self) -> None:
        """Test AABB collision with partial vertical overlap."""
        rect1 = Rect(0, 0, 10, 15)
        rect2 = Rect(0, 10, 10, 15)
        assert CollisionDetector.check_aabb_aabb(rect1, rect2)


class TestCircle:
    """Test circle collision detection."""

    def test_circle_circle_overlapping(self) -> None:
        """Test circle collision with overlapping circles."""
        circle1 = Circle(0, 0, 5)
        circle2 = Circle(5, 0, 5)
        assert CollisionDetector.check_circle_circle(circle1, circle2)

    def test_circle_circle_not_overlapping(self) -> None:
        """Test circle collision with non-overlapping circles."""
        circle1 = Circle(0, 0, 5)
        circle2 = Circle(20, 0, 5)
        assert not CollisionDetector.check_circle_circle(circle1, circle2)

    def test_circle_circle_touching(self) -> None:
        """Test circle collision with just touching circles."""
        circle1 = Circle(0, 0, 5)
        circle2 = Circle(10, 0, 5)
        # Distance is exactly 10, radius sum is 10, so not overlapping
        assert not CollisionDetector.check_circle_circle(circle1, circle2)

    def test_circle_circle_same_position(self) -> None:
        """Test circle collision at same position."""
        circle1 = Circle(5, 5, 5)
        circle2 = Circle(5, 5, 5)
        assert CollisionDetector.check_circle_circle(circle1, circle2)


class TestCircleAABB:
    """Test circle-AABB collision detection."""

    def test_circle_aabb_inside_rect(self) -> None:
        """Test circle inside AABB."""
        circle = Circle(5, 5, 3)
        rect = Rect(0, 0, 20, 20)
        assert CollisionDetector.check_circle_aabb(circle, rect)

    def test_circle_aabb_overlapping_edge(self) -> None:
        """Test circle overlapping AABB edge."""
        circle = Circle(12, 5, 5)
        rect = Rect(0, 0, 10, 10)
        assert CollisionDetector.check_circle_aabb(circle, rect)

    def test_circle_aabb_not_overlapping(self) -> None:
        """Test circle not overlapping AABB."""
        circle = Circle(20, 20, 3)
        rect = Rect(0, 0, 10, 10)
        assert not CollisionDetector.check_circle_aabb(circle, rect)

    def test_circle_aabb_corner(self) -> None:
        """Test circle colliding with rect corner."""
        circle = Circle(10, 10, 2)
        rect = Rect(0, 0, 10, 10)
        assert CollisionDetector.check_circle_aabb(circle, rect)


class TestEllipseCircle:
    """Test ellipse-circle collision detection."""

    def test_ellipse_circle_inside(self) -> None:
        """Test circle inside ellipse."""
        ellipse = Ellipse(10, 10, 10, 5)
        circle = Circle(10, 10, 2)
        assert CollisionDetector.check_ellipse_circle(ellipse, circle)

    def test_ellipse_circle_overlapping(self) -> None:
        """Test circle overlapping ellipse boundary."""
        ellipse = Ellipse(10, 10, 10, 5)
        circle = Circle(18, 10, 5)
        assert CollisionDetector.check_ellipse_circle(ellipse, circle)

    def test_ellipse_circle_not_overlapping(self) -> None:
        """Test circle not overlapping ellipse."""
        ellipse = Ellipse(10, 10, 5, 5)
        circle = Circle(30, 30, 2)
        assert not CollisionDetector.check_ellipse_circle(ellipse, circle)


class TestScreenBounds:
    """Test screen boundary checks."""

    def test_projectile_in_bounds(self) -> None:
        """Test projectile within screen bounds."""
        from game.domain.entities import Position, Size

        pos = Position(100, 100)
        size = Size(5, 5)
        assert not CollisionDetector.check_projectile_screen_bounds(pos, size, 1280, 720)

    def test_projectile_out_of_bounds_left(self) -> None:
        """Test projectile outside left boundary."""
        from game.domain.entities import Position, Size

        pos = Position(-10, 100)
        size = Size(5, 5)
        assert CollisionDetector.check_projectile_screen_bounds(pos, size, 1280, 720)

    def test_projectile_out_of_bounds_right(self) -> None:
        """Test projectile outside right boundary."""
        from game.domain.entities import Position, Size

        pos = Position(1280, 100)
        size = Size(5, 5)
        assert CollisionDetector.check_projectile_screen_bounds(pos, size, 1280, 720)

    def test_projectile_out_of_bounds_top(self) -> None:
        """Test projectile outside top boundary."""
        from game.domain.entities import Position, Size

        pos = Position(100, -10)
        size = Size(5, 5)
        assert CollisionDetector.check_projectile_screen_bounds(pos, size, 1280, 720)

    def test_projectile_out_of_bounds_bottom(self) -> None:
        """Test projectile outside bottom boundary."""
        from game.domain.entities import Position, Size

        pos = Position(100, 720)
        size = Size(5, 5)
        assert CollisionDetector.check_projectile_screen_bounds(pos, size, 1280, 720)


class TestRectClamping:
    """Test rectangle clamping to screen bounds."""

    def test_clamp_rect_left(self) -> None:
        """Test clamping rect to left boundary."""
        rect = Rect(-5, 100, 10, 10)
        clamped = CollisionDetector.clamp_rect_to_screen(rect, 1280, 720)
        assert clamped.x == 0

    def test_clamp_rect_right(self) -> None:
        """Test clamping rect to right boundary."""
        rect = Rect(1275, 100, 10, 10)
        clamped = CollisionDetector.clamp_rect_to_screen(rect, 1280, 720)
        assert clamped.x == 1270

    def test_clamp_rect_inside(self) -> None:
        """Test rect clamping when already inside."""
        rect = Rect(100, 100, 10, 10)
        clamped = CollisionDetector.clamp_rect_to_screen(rect, 1280, 720)
        assert clamped.x == 100 and clamped.y == 100


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
