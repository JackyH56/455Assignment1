import csv
from board_util import GoBoardUtil
from board_util import coord_to_point
from gtp_connection import move_to_coord
import random

weights = []
reader = csv.reader(open("weights.txt"), delimiter="\t")
for entry in reader:
    code_to_weight = entry[0].split()
    weights.append((int(code_to_weight[0]), float(code_to_weight[1])))

class PatternUtil(object):
    @staticmethod
    def generate_pattern_moves(board, color):
        legal_moves = GoBoardUtil.generate_legal_moves(board, color)
        print(legal_moves)
        distribution = []
        sum = 0.0
        for move in legal_moves:
            code = PatternUtil.get_pattern_code(move, board)
            if weights[code] and weights[code] != 1.0:
                distribution.append([code, weights[code][1]])
                sum += weights[code][1]
        
        # adjust probabilities so they add up to 1, a proper distribution
        for pattern in distribution:
            pattern[1] = pattern[1] / sum

        return distribution

    @staticmethod
    def random_select(distribution):
        r = random.random()
        sum = 0.0
        for item in distribution:
            sum += item[1]
            if sum > r:
                return item
        return distribution[-1]

    @staticmethod
    def get_pattern_code(move, board):
        point = move
        # coord = move_to_coord(str(move), board.size)
        # point = coord_to_point(coord[0], coord[1], board.size)
        adjacent = [
            point - board.NS - 1,
            point - board.NS,
            point - board.NS + 1,
            point - 1,
            point + 1,
            point + board.NS - 1,
            point + board.NS,
            point + board.NS + 1]
        
        code = 0
        for i in range(8):
            code += board.board[adjacent[i]] * 4 ^ i
        return code
