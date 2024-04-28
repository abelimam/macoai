from typing import List
from games import Action, Observation, ForwardModel
from heuristics import Heuristic

# Ali
class GreedyTurnNode:
    def __init__(self, observation: Observation, heuristic: Heuristic, action: Action = None, parent: 'GreedyTurnNode' = None):
        self.observation = observation
        self.heuristic = heuristic
        self.action = action
        self.parent = parent
        self.children: List['GreedyTurnNode'] = []

    def extend(self, forward_model: ForwardModel) -> List['GreedyTurnNode']:
        actions = self.observation.get_actions()
        for action in actions:
            new_observation = self.observation.clone()
            forward_model.step(new_observation, action)
            child = GreedyTurnNode(new_observation, self.heuristic, action, self)
            self.children.append(child)
        return self.children

    def get_path(self) -> List[Action]:
        path = []
        node = self
        while node.parent is not None:
            path.insert(0, node.action)
            node = node.parent
        return path

    def get_observation(self) -> Observation:
        return self.observation