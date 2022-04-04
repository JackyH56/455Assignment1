"""
feature_moves.py
Move generation based on simple features.
"""

from board_util import GoBoardUtil, PASS
from feature import Features_weight
from feature import Feature
import numpy as np

class FeatureMoves(object):
    @staticmethod
    def generate_moves(board):

        assert len(Features_weight) != 0
        moves = []
        gamma_sum = 0.0
        empty_points = board.get_empty_points()
        color = board.current_player
        probs = np.zeros(board.maxpoint)
        all_board_features = Feature.find_all_features(board)
        for move in empty_points:
            if board.is_legal(move, color) and not board.is_eye(move, color):
                moves.append(move)
                probs[move] = Feature.compute_move_gamma(
                    Features_weight, all_board_features[move]
                )
                gamma_sum += probs[move]
        if len(moves) != 0:
            assert gamma_sum != 0.0
            for m in moves:
                probs[m] = probs[m] / gamma_sum
        return moves, probs

    @staticmethod
    def generate_move_with_feature_based_probs_max(board):
        """Used for UI"""
        moves, probs = FeatureMoves.generate_moves(board)
        move_prob_tuple = []
        for m in moves:
            move_prob_tuple.append((m, probs[m]))
        return sorted(move_prob_tuple, key=lambda i: i[1], reverse=True)[0][0]

    @staticmethod
    def playGame(board, color, **kwargs):
        """
        Run a simulation game according to give parameters.
        """
        limit = kwargs.pop("limit", 1000)
        if kwargs:
            raise TypeError("Unexpected **kwargs: %r" % kwargs)
        winner = board.current_player
        for _ in range(limit):
            color = board.current_player
            move = FeatureMoves.generate_move(board)
            board.play_move(move, color)
            if move == PASS:
                winner = GoBoardUtil.opponent(color)
                break
        return winner
