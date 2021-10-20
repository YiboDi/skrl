from typing import Union

import torch
from torch.distributions import Normal

from . import Noise


class OrnsteinUhlenbeckNoise(Noise):
    def __init__(self, theta: float, sigma: float, base_scale: float, mean: float = 0, std: float = 1, device: str = "cuda:0") -> None:
        """
        Ornstein Uhlenbeck noise

        Parameters
        ----------
        theta: float
            Factor to apply to internal state
        sigma: float
            Factor to apply to the normal distribution
        base_scale: float
            Factor to apply to returned noise
        mean: float, optional
            Mean of the normal distribution (default: 0.0)
        std: float, optional
            Standard deviation of the normal distribution (default: 1.0)
        device: str, optional
            Device on which a torch tensor is or will be allocated (default: "cuda:0")
        """
        super().__init__(device)

        self.theta = theta
        self.sigma = sigma
        self.base_scale = base_scale

        self.state = 0

        self.distribution = Normal(mean, std)
        
    def sample(self, shape: Union[tuple[int], list[int], torch.Size]) -> torch.Tensor:
        gaussian_sample = self.distribution.sample(shape).to(self.device)
        self.state += -self.state * self.theta + self.sigma * gaussian_sample
        
        return self.base_scale * self.state
