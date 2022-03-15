#!/usr/local/bin/python3
# /usr/bin/python3
# Set the path to your python3 above

from gtp_connection import GtpConnection
from board_util import GoBoardUtil, PASS
from board import GoBoard
from simulation_util import writeMoves, select_best_move
from pattern_util import PatternUtil
from ucb import runUcb
import numpy as np
import argparse
import sys

class Go3:
    def __init__(self, move_select, sim_rule):
        """
        Go player that selects moves by simulation.
        """
        self.name = "Go3"
        self.version = 1.0
        self.sim = 10
        self.limit = 100
        self.move_selection = move_select # move_select = "rr" or "ucb"
        self.sim_policy = sim_rule # sim_policy = "random" or "patternbased"

    def simulate(self, board, move, toplay):
        """
        Run a simulated game for a given move.
        """
        cboard = board.copy()
        cboard.play_move(move, toplay)
        opp = GoBoardUtil.opponent(toplay)
        return self.playGame(cboard, opp)

    def simulateMove(self, board, move, toplay):
        """
        Run simulations for a given move.
        """
        wins = 0
        for _ in range(self.sim):
            result = self.simulate(board, move, toplay)
            if result == toplay:
                wins += 1
        return wins

    def get_move(self, board, color):
        """
        Run one-ply MC simulations to get a move to play.
        """
        cboard = board.copy()
        emptyPoints = board.get_empty_points()
        moves = []
        for p in emptyPoints:
            if board.is_legal(p, color):
                moves.append(p)
        if not moves:
            return None
        moves.append(None)
        if self.move_selection == "ucb":
            C = 0.4  # sqrt(2) is safe, this is more aggressive
            best = runUcb(self, cboard, C, moves, color)
            return best
        else:
            moveWins = []
            for move in moves:
                wins = self.simulateMove(cboard, move, color)
                moveWins.append(wins)
            writeMoves(cboard, moves, moveWins, self.sim)
            return select_best_move(board, moves, moveWins)

    def playGame(self, board, color):
        """
        Run a simulation game.
        """
        winner = board.current_player
        for _ in range(self.limit):
            color = board.current_player
            if self.sim_policy == "random":
                move = GoBoardUtil.generate_random_move(board, color, False)
            else:
                distribution = PatternUtil.generate_pattern_moves(board, color)
                move = PatternUtil.random_select_move(distribution)
            board.play_move(move, color)
            
            if move == PASS:
                winner = GoBoardUtil.opponent(color)
                break
        return winner
    
    def getDistribution(self, board, color):
        distribution = PatternUtil.generate_pattern_moves(board, color)
        return distribution

def run(move_select, sim_rule):
    """
    Start the gtp connection and wait for commands.
    """
    board = GoBoard(7)
    con = GtpConnection(Go3(move_select, sim_rule), board)
    con.start_connection()


def parse_args():
    """
    Parse the arguments of the program.
    """
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "--moveselect",
        type=str,
        default="rr",
        help="type of move selection: rr or ucb",
    )
    parser.add_argument(
        "--simrule",
        type=str,
        default="random",
        help="type of simulation policy: random or patternbased",
    )

    args = parser.parse_args()
    move_select = args.moveselect
    sim_rule = args.simrule
    if move_select != "rr" and move_select != "ucb":
        print("moveselect must be rr or ucb")
        sys.exit(0)
    if sim_rule != "random" and sim_rule != "patternbased":
        print("simrule must be random or patternbased")
        sys.exit(0)

    return move_select, sim_rule

if __name__ == "__main__":
    move_select, sim_rule = parse_args()
    run(move_select, sim_rule)
