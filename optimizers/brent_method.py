from scipy.optimize import minimize_scalar

from optimizers import Optimizer
from util import Path


class BrentMethod(Optimizer):
    def minimize(self, f, a, b, eps, min_iterations=2, max_iterations=10000):
        res = minimize_scalar(f, bracket=(a, b), tol=eps, method='brent')
        return res.x, Path([], [], [], res.nfev, res.nit)
