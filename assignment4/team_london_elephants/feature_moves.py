"""
feature_moves.py
Move generation based on simple features.
"""

from board_util import GoBoardUtil, PASS
import numpy as np
from pattern_util import PatternUtil


class FeatureMoves(object):
    @staticmethod
    def playGame(board, color, **kwargs):
        """
        Run a simulation game according to give parameters.
        """
        limit = kwargs.pop("limit", 1000)
        simulation_policy = kwargs.pop("random_simulation", "random")
        use_pattern = kwargs.pop("use_pattern", True)

        if kwargs:
            raise TypeError("Unexpected **kwargs: %r" % kwargs)
        winner = board.current_player
        for _ in range(limit):
            color = board.current_player
            # assert simulation_policy == "random"
            # move = FeatureMoves.generate_moves(board)
            move = GoBoardUtil.generate_random_move(board, color)
            # distribution = PatternUtil.generate_pattern_moves(board, color)
            # move = PatternUtil.random_select_move(distribution)
            board.play_move(move, color)
            if move == PASS:
                winner = GoBoardUtil.opponent(color)
                break
        return winner
