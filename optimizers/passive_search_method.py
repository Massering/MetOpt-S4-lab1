import numpy as np

from optimizers.optimizer import Optimizer
from util.path import Path


class PassiveSearchMethod(Optimizer):
    def __init__(self, n: int = 1000):
        self.n = n

    def minimize(self, f, a, b, eps, min_iterations=2, max_iterations=10000):
        xs = np.linspace(a, b, self.n)
        values = [f(x) for x in xs]
        idx = int(np.argmin(values))
        return xs[idx], Path(
            intervals=[],
            points=list(xs),
            values=values,
            func_calls=self.n,
            iterations=1
        )
