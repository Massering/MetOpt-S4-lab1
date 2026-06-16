import math

from optimizers.optimizer import Optimizer
from util.path import Path


class GoldenSectionMethod(Optimizer):
    def minimize(self, f, a, b, eps, min_iterations=2, max_iterations=10000):
        phi = (1 + math.sqrt(5)) / 2
        path = []

        x1 = b - (b - a) / phi
        x2 = a + (b - a) / phi

        f1 = f(x1)
        f2 = f(x2)
        calls = 2
        k = 0

        while (b - a) > eps and k < max_iterations or k <= min_iterations:
            if f1 < f2:
                b = x2
                x2 = x1
                f2 = f1
                x1 = b - (b - a) / phi
                f1 = f(x1)
            else:
                a = x1
                x1 = x2
                f1 = f2
                x2 = a + (b - a) / phi
                f2 = f(x2)

            calls += 1
            path.append((a, b))
            k += 1

        return (a + b) / 2, Path(path, [], [], calls, k)
