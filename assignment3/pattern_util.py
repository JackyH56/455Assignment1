import csv
from board_util import GoBoardUtil, PASS
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
        # distribution_item[0] - the move
        # distribution_item[1] - the board code
        # distribution_item[2] - the probability
        legal_moves = GoBoardUtil.generate_legal_moves(board, color)
        distribution = []
        sum = 0.0
        for point in legal_moves:
            code = PatternUtil.get_pattern_code(point, board)
            if weights[code] and weights[code][1] != 1.0:
                distribution.append([point, code, weights[code][1]])
                sum += weights[code][1]
        
        # adjust probabilities so they add up to 1, a proper distribution
        for pattern in distribution:
            pattern[2] = pattern[2] / sum

        return distribution

    @staticmethod
    def random_select(distribution):
        # item[0] - the move
        # item[1] - the board code
        # item[2] - the probability
        if len(distribution) == 0:
            return PASS

        r = random.random()
        sum = 0.0
        for item in distribution:
            sum += item[2]
            if sum > r:
                return item[0]
        return distribution[-1][0]

    @staticmethod
    def get_pattern_code(point, board):
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
            code += board.get_color(adjacent[i]) * 4 ^ i

        return code
