from typing import List, Tuple
from dataclasses import dataclass


@dataclass
class Path:
    intervals: List[Tuple[float, float]]
    points: List[float]
    values: List[float]
    func_calls: int
    iterations: int
