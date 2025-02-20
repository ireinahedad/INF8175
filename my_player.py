
from player_divercite import PlayerDivercite
from seahorse.game.action import Action
from seahorse.game.game_state import GameState
import random
from game_state_divercite import GameStateDivercite
from seahorse.utils.custom_exceptions import MethodNotImplementedError

class MyPlayer(PlayerDivercite):
    """
    Player class for Divercite game that makes random moves.

    Attributes:
        piece_type (str): piece type of the player
    """


    def __init__(self, piece_type: str, name: str = "MyPlayer"):
        """
        Initialize the PlayerDivercite instance.

        Args:
            piece_type (str): Type of the player's game piece
            name (str, optional): Name of the player (default is "bob")
            time_limit (float, optional): the time limit in (s)
        """
        super().__init__(piece_type, name)
        # Add any information you want to store about the player here
        self.depth = 3
        # self.json_additional_info = {}

    def compute_action(self, current_state: GameState, remaining_time: int = 1e9, **kwargs) -> Action:
        """
        Use the minimax algorithm to choose the best action based on the heuristic evaluation of game states.

        Args:
            current_state (GameState): The current game state.

        Returns:
            Action: The best action as determined by minimax.
        """
        possible_actions = possible_actions = current_state.generate_possible_heavy_actions()
        if not possible_actions:
            return None  # No valid move

        #best_action, best_value = None, float('-inf')
        best_action = next(possible_actions)
        best_value = best_action.get_next_game_state().scores[self.get_id()]

        for action in possible_actions:
            next_state = action.get_next_game_state()
            _, value = self.Fakeminimax(next_state, self.depth - 1, True, float('-inf'), float('inf'))

            if value > best_value:
                best_value = value
                best_action = action

        return best_action

    def Fakeminimax(self, state: GameState, depth: int, is_maximizing: bool, alpha: float, beta: float):
        if depth == 0 or not list(state.get_possible_heavy_actions()):
            print("depth is zero")
            return None, self.evaluate_state(state)

        if is_maximizing:
            return self.maxValue(state, depth, alpha, beta)
        else:
            return self.minValue(state, depth, alpha, beta)



    def maxValue(self, state: GameState, depth: int, alpha: float, beta: float):
        if depth == 0 or not list(state.get_possible_heavy_actions()):
            return None, self.evaluate_state(state)

        max_eval = float('-inf')
        best_action = None
        possible_actions = list(state.get_possible_heavy_actions())[:5]

        for action in possible_actions:
            next_state = action.get_next_game_state()
            _, eval = self.minValue(next_state, depth - 1, alpha, beta)

            if eval > max_eval:
                max_eval = eval
                best_action = action

            alpha = max(alpha, max_eval)
            if beta <= alpha:  # Alpha-beta pruning
                break

        return best_action, max_eval

    def minValue(self, state: GameState, depth: int, alpha: float, beta: float):
        if depth == 0 or not list(state.get_possible_heavy_actions()):
            return None, self.evaluate_state(state)

        min_eval = float('inf')
        best_action = None
        possible_actions = list(state.get_possible_heavy_actions())[:5]

        for action in possible_actions:
            next_state = action.get_next_game_state()
            _, eval = self.maxValue(next_state, depth - 1, alpha, beta)

            if eval < min_eval:
                min_eval = eval
                best_action = action

            beta = min(beta, min_eval)
            if beta <= alpha:  # Alpha-beta pruning
                break

        return best_action, min_eval

    def evaluate_state(self, state: GameState) -> float:
        player_id = self.get_id()
        opponent_id = state.get_next_player().get_id()

        player_score = state.scores.get(player_id, 0)
        opponent_score = state.scores.get(opponent_id, 0)

        return player_score-opponent_score  # Positive = good, negative = bad
