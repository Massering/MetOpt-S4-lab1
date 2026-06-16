from optimizers import *
from calculations import *


def run_experiments():
    eps_values = [10 ** (-k) for k in range(2, 9)]

    results = {}

    for func_name, func in FUNCTIONS.items():
        print(f"\nFunction: {func_name}")
        results[func_name] = {}
        for method_name, method in METHODS.items():
            print(f"  Method: {method_name}")
            results[func_name][method_name] = []
            for eps in eps_values:
                x_min, hist = method.minimize(func, -2, 5, eps)
                results[func_name][method_name].append({
                    "eps": eps,
                    "x_min": x_min,
                    "iterations": hist.iterations,
                    "calls": hist.func_calls
                })

    return results


results = run_experiments()
for f_name, methods in results.items():
    print(f"\nFunction: {f_name}")
    for m_name, res in methods.items():
        print(f"  Method: {m_name}")
        for r in res:
            print(r)
