from optimizers.optimizer import Optimizer
from util.path import Path


class ParabolicMethod(Optimizer):
    def minimize(self, f, a, b, eps, min_iterations=5, max_iterations=10000):
        x1, x2, x3 = a, (a + b) / 2, b
        f1, f2, f3 = f(x1), f(x2), f(x3)

        calls = 3
        path = []
        k = 0

        while abs(x3 - x1) > eps and k < max_iterations or k <= min_iterations:
            numerator = (x2 - x1) ** 2 * (f2 - f3) - (x2 - x3) ** 2 * (f2 - f1)
            denominator = (x2 - x1) * (f2 - f3) - (x2 - x3) * (f2 - f1)
            k += 1

            if denominator == 0:
                path.append((x2, x2))
                break

            u = x2 - 0.5 * numerator / denominator
            fu = f(u)
            calls += 1

            if u < x2:
                if fu < f2:
                    x3, f3 = x2, f2
                    x2, f2 = u, fu
                else:
                    x1, f1 = u, fu
            else:
                if fu < f2:
                    x1, f1 = x2, f2
                    x2, f2 = u, fu
                else:
                    x3, f3 = u, fu

            path.append((x1, x3))

        return x2, Path(path, [], [], calls, k)
