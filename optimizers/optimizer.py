from typing import Callable, Tuple

from util.path import Path


class Optimizer:
    def minimize(self, f: Callable[[float], float], a: float, b: float, eps: float) -> Tuple[float, Path]:
        raise NotImplementedError
