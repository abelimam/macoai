from typing import List
from games import Action, Observation, ForwardModel
from heuristics import Heuristic
from players import Player
from players.greedy_turn.greedy_turn_node import GreedyTurnNode
import math
import time

# Ali
class GreedyTurnPlayer(Player):
    def __init__(self, heuristic: Heuristic):
        super().__init__()
        self.heuristic = heuristic
        self.best_reward = -math.inf
        self.turn: List[Action] = []

    def think(self, observation: Observation, forward_model: ForwardModel, budget: float) -> None:
        self.turn.clear()
        self.best_reward = -math.inf
        start_time = time.time()
        root = GreedyTurnNode(observation, self.heuristic)
        self._run_search(root, forward_model, budget, start_time)

    def get_action(self, index: int) -> Action:
        if 0 <= index < len(self.turn):
            return self.turn[index]
        return None

    def _run_search(self, node: GreedyTurnNode, forward_model: ForwardModel, budget: float, start_time: float) -> None:
        if node.parent is not None:
            self.visited_states[node.get_observation()] += 1
            self.forward_model_visits += 1

        if time.time() - start_time > budget:
            return

        if forward_model.is_turn_finished(node.get_observation()):
            reward = self.heuristic.get_reward(node.get_observation())
            if reward > self.best_reward:
                self.best_reward = reward
                self.turn = node.get_path()
            return

        for child in node.extend(forward_model):
            self._run_search(child, forward_model, budget, start_time)

    def __str__(self) -> str:
        return "GreedyTurnPlayer"