from optimizers.optimizer import Optimizer
from util.path import Path


class FibonacciMethod(Optimizer):
    def minimize(self, f, a, b, eps, min_iterations=2, max_iterations=10000):
        fib = [1, 1]
        while fib[-1] < (b - a) / eps and len(fib) < max_iterations:
            fib.append(fib[-1] + fib[-2])

        n = len(fib)
        path = []

        x1 = a + fib[n - 3] / fib[n - 1] * (b - a)
        x2 = a + fib[n - 2] / fib[n - 1] * (b - a)

        f1 = f(x1)
        f2 = f(x2)
        calls = 2

        k = 1
        for k in range(1, n - 1):
            if k >= max_iterations:
                break
            if f1 < f2:
                b = x2
                x2 = x1
                f2 = f1
                x1 = a + fib[n - k - 3] / fib[n - k - 1] * (b - a)
                f1 = f(x1)
            else:
                a = x1
                x1 = x2
                f1 = f2
                x2 = a + fib[n - k - 2] / fib[n - k - 1] * (b - a)
                f2 = f(x2)

            calls += 1
            path.append((a, b))

        return (a + b) / 2, Path(path, [], [], calls, k)
