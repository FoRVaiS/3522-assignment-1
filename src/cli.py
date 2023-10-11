"""
This entrypoint module is responsible for parsing command line arguments and applying setting overrides.
"""

import argparse
from Game import Game

CLI_DESC = "Initialize the snake game."


def parse():
    """
    Parse command line arguments and apply setting overrides.
    """
    parser = argparse.ArgumentParser(description=CLI_DESC)
    parser.add_argument("--width", type=str, default="900", help="The width of the game window.")
    parser.add_argument("--height", type=str, default="600", help="The height of the game window.")
    parser.add_argument("--tickrate", type=str, default="64", help="The number of times to update the game per second.")

    return parser.parse_args()


if __name__ == "__main__":
    args = parse()
    game = Game(width=int(args.width), height=int(args.height), tickrate=int(args.tickrate))
    game.start()
