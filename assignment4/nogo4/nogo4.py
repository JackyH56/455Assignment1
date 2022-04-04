#!/usr/bin/python3
# /usr/bin/python3
# Set the path to your python3 above

from gtp_connection import GtpConnection
from board_util import GoBoardUtil
from board import GoBoard
from mcts import MCTS

#################################################
'''
This is a uniform random NoGo player served as the starter code
for your (possibly) stronger player. Good luck!
'''

def count_at_depth(node, depth, nodesAtDepth):
    if not node._expanded:
        return
    nodesAtDepth[depth] += 1
    for _, child in node._children.items():
        count_at_depth(child, depth + 1, nodesAtDepth)
        
class NoGo:
    def __init__(self):
        """
        NoGo player that selects moves randomly from the set of legal moves.

        Parameters
        ----------
        name : str
            name of the player (used by the GTP interface).
        version : float
            version number (used by the GTP interface).
        """

        self.name = "NoGo4"
        self.version = 1.0
        self.MCTS = MCTS()
        self.num_simulation = 300
        self.limit = 100
        self.exploration = 0.4
        self.simulation_policy = "probabilistic"
        self.use_pattern = True
        self.in_tree_knowledge = None
        self.parent = None

    def reset(self):
        self.MCTS = MCTS()

    def update(self, move):
        self.parent = self.MCTS._root
        self.MCTS.update_with_move(move)

    def get_move(self, board:GoBoard, color:int):
        """
        Select a random move.
        """
        move = self.MCTS.get_move(
            board,
            color,
            limit=self.limit,
            use_pattern=self.use_pattern,
            num_simulation=self.num_simulation,
            exploration=self.exploration,
            simulation_policy=self.simulation_policy,
            in_tree_knowledge=self.in_tree_knowledge,
        )
        self.update(move)
        return move

    def get_node_depth(self, root):
        MAX_DEPTH = 100
        nodesAtDepth = [0] * MAX_DEPTH
        count_at_depth(root, 0, nodesAtDepth)
        prev_nodes = 1
        return nodesAtDepth

    def get_properties(self):
        return dict(version=self.version, name=self.__class__.__name__,)
        
def run():
    """
    start the gtp connection and wait for commands.
    """
    board = GoBoard(7)
    con = GtpConnection(NoGo(), board)
    con.start_connection()

if __name__ == "__main__":
    run()
