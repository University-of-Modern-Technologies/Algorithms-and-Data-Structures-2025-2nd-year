"""
Main entry point for running the game as a module.

Usage: python -m game
"""

import sys
from pathlib import Path

# Add src directory to path so imports work
sys.path.insert(0, str(Path(__file__).parent.parent))

from game.infra.logging import Logger


def main() -> None:
    """Run the game."""
    logger = Logger()
    
    # Console output for visibility
    print("=" * 50)
    print("🎮 SPACE INVADERS")
    print("=" * 50)
    print(f"Python version: {sys.version.split()[0]}")
    print(f"Working directory: {Path.cwd()}")
    print()
    
    logger.info("=== Space Invaders Game ===")
    logger.info(f"Python version: {sys.version}")
    logger.info("Starting initialization...")

    try:
        print("✓ Initializing game systems...")
        # TODO: Initialize pygame and game systems
        # - ConfigManager
        # - AssetLoader
        # - InputHandler
        # - GameTimer
        # - Renderer
        # - Scene Manager
        
        logger.info("Game initialized successfully")
        print("✓ Game initialized")
        print()

        print("⚠️  WARNING: Main game loop not yet implemented")
        print("   This is phase 0 (Setup). Phase 1 will add:")
        print("   - Physics and collision detection")
        print("   - Input handling (keyboard, gamepad)")
        print("   - Game logic update")
        print("   - Rendering pipeline")
        print()
        
        # TODO: Run main game loop
        logger.info("Game started")

    except KeyboardInterrupt:
        print("\n⏹️  Game interrupted by user")
        logger.info("Game interrupted by user")
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        logger.error(f"Fatal error: {e}", exc=e)
        sys.exit(1)
    finally:
        print("=" * 50)
        print("Game closed. Logs written to: logs/game.log")
        print("=" * 50)
        logger.info("Game closed")


if __name__ == "__main__":
    main()
