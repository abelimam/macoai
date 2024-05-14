from collections import defaultdict
from typing import List, Optional, Tuple
from games import Action, Observation, ForwardModel
from heuristics import Heuristic
import math
import random
import sys
import numpy as np

class MontecarloTreeSearchNode:
    def __init__(self, observation: 'Observation', heuristic: 'Heuristic', action: 'Action', parent: 'MontecarloTreeSearchNode' = None):
        """Node class for the tree used in Montecarlo Tree Search."""
        self.observation = observation
        self.heuristic = heuristic
        self.action = action
        self.parent = parent
        self.children: List['MontecarloTreeSearchNode'] = []
        self.visits = 0
        self.reward = 0

# region Methods
    def visit(self, reward: float) -> None:
        """Visits the `Node` by adding to the visit count and adding the reward to the total reward."""
        self.visits += 1
        self.reward += reward

    def add_child(self, child: 'MontecarloTreeSearchNode') -> None:
        """Adds a child to the `Node` child list."""
        self.children.append(child)

    def extend(self, forward_model: 'ForwardModel', visited: defaultdict) -> int:
        """Extends the `Node` by generating a child for each possible action"""
        actions = self.observation.get_actions()
        for action in actions:
            new_observation = self.observation.clone()
            forward_model.step(new_observation, action)
            visited[new_observation] += 1
            self.children.append(MontecarloTreeSearchNode(new_observation, self.heuristic, action, self))
        return len(actions)

    def rollout(self, forward_model: 'ForwardModel', visited: defaultdict) -> Tuple[float, int]:
        """Performs a random rollout from the `Node` and returns the reward."""
        new_observation = self.observation.clone()
        fm_visits = 0
        while not forward_model.is_terminal(new_observation) and not forward_model.is_turn_finished(new_observation):
            action = new_observation.get_random_action()
            forward_model.step(new_observation, action)
            visited[new_observation] += 1
            fm_visits += 1
        
        return self.heuristic.get_reward(new_observation), fm_visits
    
    def full_rollout(self, forward_model: 'ForwardModel', visited: defaultdict) -> Tuple[float, int]:
        """Performs a full rollout from the `Node` and returns the reward."""
        new_observation = self.observation.clone()
        fm_visits = 0
        while not forward_model.is_terminal(new_observation):
            while not forward_model.is_turn_finished(new_observation):
                action = new_observation.get_random_action()
                forward_model.step(new_observation, action)
                visited[new_observation] += 1
                fm_visits += 1
            forward_model.on_turn_ended(new_observation)
        reward = self.heuristic.get_reward(new_observation)
        return reward, fm_visits
    
    def get_best_action(self, observation: 'Observation', forward_model: 'ForwardModel', visited: defaultdict) -> Tuple['Action', int]:
        """Returns the best action from the `Node` by average reward."""
        best_action = None
        best_reward = -math.inf
        fm_visits = 0
        for roll_action in observation.get_actions():
            current_observation = observation.clone()
            forward_model.step(current_observation, roll_action)
            visited[current_observation] += 1
            fm_visits += 1
            reward = self.heuristic.get_reward(current_observation)
            if reward > best_reward:
                best_reward = reward
                best_action = roll_action

        return best_action, fm_visits
    
    def deterministic_rollout(self, forward_model: 'ForwardModel', visited: defaultdict) -> Tuple[float, int]:
        """Performs a deterministic rollout from the `Node` and returns the reward."""
        new_observation = self.observation.clone()
        fm_visits = 0
        while not forward_model.is_terminal(new_observation):
            while not forward_model.is_turn_finished(new_observation):
                action = new_observation.get_random_action()
                forward_model.step(new_observation, action)
                visited[new_observation] += 1
                fm_visits += 1
            forward_model.on_turn_ended(new_observation)
        reward = self.heuristic.get_reward(new_observation)
        return reward, fm_visits
    
    def reward_children(self) -> None:
        """Rewards all children of the `Node` by the reward of the `Node`."""
        for child in self.children:
            reward = child.heuristic.get_reward(child.observation)
            child.reward += reward

    def backpropagate(self, reward: float) -> None:
        """Backpropagates the reward to the `Node` and its parents."""
        self.visit(reward)
        parent = self.parent
        while parent is not None:
            parent.visit(reward)
            parent = parent.parent
# endregion

# region Getters
    def get_action(self) -> 'Action':
        """Returns the `ASMACAG.Game.Action.Action` of the `Node`."""
        return self.action

    def get_average_reward(self) -> np.float64:
        """Returns the average reward of the `Node`"""
        return np.float64(self.reward / self.visits if self.visits > 0 else -math.inf)

    def get_best_child_by_average(self) -> Optional['MontecarloTreeSearchNode']:
        """Returns the best child of the `Node` by average reward."""
        if len(self.children) == 0:
            return None
        best_child = self.children[0]
        best_average_reward = best_child.get_average_reward()
        
        for child in self.children:
            if child.get_average_reward() > best_average_reward:
                best_child = child
                best_average_reward = child.get_average_reward()
        return best_child

    def get_best_child_by_ucb(self, c_value: float) -> 'MontecarloTreeSearchNode':
        """Returns the child of the `Node` with the highest UCB value."""
        best_child = self.children[0]
        best_ucb = -math.inf
        
        for child in self.children:
            epsilon = random.random() / 1000
            if c_value == 0:
                ucb = child.get_average_reward()
            elif child.visits != 0:
                ucb = child.get_average_reward() + c_value * math.sqrt(math.log(self.visits) / child.visits) + epsilon
            else:
                ucb = sys.float_info.max - epsilon
            if ucb > best_ucb:
                best_child = child
                best_ucb = ucb
        return best_child

    def get_random_child(self) -> 'MontecarloTreeSearchNode':
        """Returns a random child of the `Node`."""
        return random.choice(self.children)

    def get_amount_of_children(self) -> int:
        """Returns the amount of children of the `Node`."""
        return len(self.children)

    def get_is_unvisited(self) -> bool:
        """Returns whether the `Node` is unvisited."""
        return self.visits == 0

    def get_is_terminal(self, forward_model: 'ForwardModel') -> bool:
        """Returns whether the `Node` is terminal (as in the game is over or the turn is finished)."""
        return forward_model.is_terminal(self.observation) \
            or forward_model.is_turn_finished(self.observation)
# endregion