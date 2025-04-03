import math
from typing import List

from seahorse.game.heavy_action import HeavyAction

from player_divercite import PlayerDivercite
from seahorse.game.action import Action
from seahorse.game.game_state import GameState
import random
from game_state_divercite import GameStateDivercite

class MyPlayer(PlayerDivercite):
    """
    Player class with separated Minimax logic.

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
        # self.json_additional_info = {}
        self.early_move_threshold = 15  # Use MCTS for first 15 moves
        self.minimax_depth = 5
        self.mcts_iterations = 150
        self.move_count = 0

    def compute_action(self, current_state: GameStateDivercite , remaining_time: int = 1e9, **kwargs) -> Action:
        """
        Main method that uses Minimax to choose the best action.
        Returns only the Action object (not tuple).
        Args:
            current_state (GameState): The current game state.

        Returns:
            Action: The best action as determined.
        """
        possible_actions = list(current_state.generate_possible_heavy_actions())
        if not possible_actions:
            return None

        # Prune actions if too many
        if len(possible_actions) > 10:
            possible_actions = sorted(
                possible_actions,
                key=lambda action: self.evaluate_state(action.get_next_game_state()),
                reverse=True
            )[:40]

        is_early_game = self._is_early_game(current_state)

        if is_early_game:
            best_action = self.find_best_action_with_mcts(current_state, possible_actions)
        else:
            # Get only the action (ignore the float value)
            best_action, _ = self.find_best_action_with_minimax(current_state, possible_actions)

        self.move_count += 1
        return best_action  # Return just the Action object


    def _is_early_game(self, state: GameStateDivercite) -> bool:
        """Determine if we're in early game using available state information"""
        # Option 1: Use our move counter
        if hasattr(self, 'move_count'):
            return self.move_count < self.early_move_threshold

        # Option 2: Estimate based on board occupancy
        board = state.get_rep().get_env()
        return len(board) < (self.early_move_threshold * 2)  # Assuming 2 players


    def find_best_action_with_minimax(self, current_state, possible_actions) -> tuple[Action, float]:
        """
        Separated Minimax logic.
        """
        best_action = None
        best_value = float('-inf')

        for action in possible_actions:
            next_state = action.get_next_game_state()
            _, value = self.minimax(next_state, self.minimax_depth - 1, True, float('-inf'), float('inf'))

            if value > best_value:
                best_value = value
                best_action = action

        return best_action, best_value

    def minimax(self, state: GameState, depth: int, is_maximizing: bool, alpha: float, beta: float):
        if depth == 0 or not list(state.get_possible_heavy_actions()):
            return None, self.evaluate_state(state)

        if is_maximizing:
            return self.max_value(state, depth, alpha, beta)
        else:
            return self.min_value(state, depth, alpha, beta)

    def max_value(self, state: GameState, depth: int, alpha: float, beta: float):
        max_eval = float('-inf')
        best_action = None
        possible_actions = sorted(
            list(state.get_possible_heavy_actions())[:10],
            key=lambda action: self.evaluate_state(action.get_next_game_state()),
            reverse=True
        )

        for action in possible_actions:
            next_state = action.get_next_game_state()
            _, eval = self.minimax(next_state, depth - 1, False, alpha, beta)

            if eval > max_eval:
                max_eval = eval
                best_action = action

            alpha = max(alpha, eval)
            if beta <= alpha:
                break

        return best_action, max_eval

    def min_value(self, state: GameState, depth: int, alpha: float, beta: float):
        min_eval = float('inf')
        best_action = None
        possible_actions = sorted(
            list(state.get_possible_heavy_actions())[:5],
            key=lambda action: self.evaluate_state(action.get_next_game_state()),
            reverse=False
        )

        for action in possible_actions:
            next_state = action.get_next_game_state()
            _, eval = self.minimax(next_state, depth - 1, True, alpha, beta)

            if eval < min_eval:
                min_eval = eval
                best_action = action

            beta = min(beta, eval)
            if beta <= alpha:
                break

        return best_action, min_eval

    def evaluate_state(self, state: GameState) -> float:
        player_id = self.get_id()
        opponent_id = state.get_next_player().get_id()
        score_diff = state.scores.get(player_id, 0) - state.scores.get(opponent_id, 0)
        return score_diff

    def find_best_action_with_mcts(self, state: GameStateDivercite, actions: List[HeavyAction]) -> Action:
            """Simple MCTS implementation for early game"""
            action_stats = {action: {'wins': 0, 'plays': 0} for action in actions}

            for _ in range(self.mcts_iterations):
                # Selection - choose action with highest UCB1 score
                action = self.select_action_by_ucb(action_stats)

                # Simulation - play random game to completion
                # TODO: Use a more sophisticated simulation strategy, like greedy (implemented in greedy_player)??
                result = self.simulate_random_game(action.get_next_game_state())

                # Backpropagation - update statistics
                action_stats[action]['plays'] += 1
                action_stats[action]['wins'] += result

            # Return action with highest win rate
            return max(action_stats.items(), key=lambda x: x[1]['wins']/x[1]['plays'])[0]


    def select_action_by_ucb(self, action_stats):
        """UCB1 selection policy"""
        total_plays = sum(stats['plays'] for stats in action_stats.values())

        def ucb_score(action):
            if action_stats[action]['plays'] == 0:
                return float('inf')
            win_rate = action_stats[action]['wins'] / action_stats[action]['plays']
            exploration = math.sqrt(2 * math.log(total_plays) / action_stats[action]['plays'])
            return win_rate + exploration

        return max(action_stats.keys(), key=ucb_score)

    def simulate_random_game(self, state: GameStateDivercite)  -> float:
        """
        Mixed playout strategy with progressive transition based on game progression.
        """
        while not state.is_done():
            actions = list(state.generate_possible_heavy_actions())
            if not actions:
                break

            # Calculate game progression as a percentage (0.0 to 1.0)
            game_progress = state.get_step() / state.max_step
            # Random probability possible only for the first 10th of the game to add some randomness
            greedy_static_probability = 0.90
            # Adjust greedy probability based on game progression
            greedy_probability = game_progress + greedy_static_probability

            if random.random() < greedy_probability:
                # Greedy strategy: choose the action that maximizes the score
                best_action = max(
                    actions,
                    key=lambda action: action.get_next_game_state().scores[self.get_id()]
                )
            else:
                # Random strategy: choose a random action
                best_action = random.choice(actions)

            state = best_action.get_next_game_state()

        # Return the final score for the current player
        return state.scores[self.get_id()]