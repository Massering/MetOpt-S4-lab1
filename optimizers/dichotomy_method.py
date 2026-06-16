from optimizers.optimizer import Optimizer
from util.path import Path


class DichotomyMethod(Optimizer):
    def minimize(self, f, a, b, eps, min_iterations=2, max_iterations=10000):
        path = []
        calls = 0
        k = 0

        while (b - a) > eps and k < max_iterations or k <= min_iterations:
            delta = eps * (b - a) / 10

            x1 = (a + b) / 2 - delta
            x2 = (a + b) / 2 + delta

            f1 = f(x1)
            f2 = f(x2)
            calls += 2

            if f1 < f2:
                b = x2
            else:
                a = x1

            path.append((a, b))
            k += 1

        x_min = (a + b) / 2
        return x_min, Path(path, [], [], calls, k)
