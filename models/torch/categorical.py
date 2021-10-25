from __future__ import annotations
from typing import Union, Tuple

import gym
import torch
from torch.distributions import Categorical

from . import Model


class CategoricalModel(Model):
    def __init__(self, observation_space: Union[int, tuple[int], gym.Space, None] = None, action_space: Union[int, tuple[int], gym.Space, None] = None, device: str = "cuda:0") -> None:
        """
        Categorical model (Stochastic)

        # TODO: describe internal properties

        https://spinningup.openai.com/en/latest/spinningup/rl_intro.html#stochastic-policies
        """
        super().__init__(observation_space=observation_space, action_space=action_space, device=device)

        self.use_unnormalized_log_probabilities = True

    def act(self, states, taken_actions=None, inference=False):
        # map from states/observations to normalized probabilities or unnormalized log probabilities
        # unnormalized log probabilities
        if self.use_unnormalized_log_probabilities:
            logits = self.compute(states, taken_actions)
            distribution = Categorical(logits=logits)
        # normalized probabilities
        else:
            probs = self.compute(states, taken_actions)
            distribution = Categorical(probs=probs)
        
        # actions and log of the probability density function
        actions = distribution.sample()
        log_prob = distribution.log_prob(actions)

        return actions, log_prob, torch.Tensor()
