import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from optimizers import *

OUTPUT_DIR = "results"
os.makedirs(OUTPUT_DIR, exist_ok=True)

EPS_VALUES = [10 ** (-k) for k in range(1, 9)]

FUNCTIONS = {
    "Хорошая": lambda x: x ** 2,
    "Плато": lambda x: x ** 8,
    "Ассиметричная": lambda x: x ** 2 + np.exp(5 * (1 - x)),
    "Мультимодальная": lambda x: x ** 2 + np.sin(5 * x)
}

DICHOTOMY = 'Метод дихотомии'
GOLDEN_SECTION = 'Метод золотого сечения'
FIBONACCI = 'Метод Фибоначчи'
PARABOLIC = 'Метод парабол'
PASSIVE_SEARCH = 'Метод пассивного поиска'
EXPLORATION_AND_EXPLOITATION_SEARCH = 'Exploration & exploitation'
BRENT = 'brent'

METHODS = {
    DICHOTOMY: DichotomyMethod(),
    GOLDEN_SECTION: GoldenSectionMethod(),
    FIBONACCI: FibonacciMethod(),
    PARABOLIC: ParabolicMethod(),
    PASSIVE_SEARCH: PassiveSearchMethod(1000),
    EXPLORATION_AND_EXPLOITATION_SEARCH: ExplorationAndExploitationMethod(20),
    BRENT: BrentMethod()
}


def run_all():
    results = {}

    for fname, f in FUNCTIONS.items():
        results[fname] = {}

        interval_storage = {}

        for mname, method in METHODS.items():
            rows = []

            for eps in EPS_VALUES:
                x_min, hist = method.minimize(f, -2, 5, eps)

                rows.append({
                    "eps": eps,
                    "x_min": x_min,
                    "iterations": hist.iterations,
                    "calls": hist.func_calls
                })

                if eps == 1e-4:
                    interval_storage[mname] = hist.intervals
                    save_interval_plot(hist.intervals, fname, mname)

            df = pd.DataFrame(rows)
            results[fname][mname] = df

            save_table(df, fname, mname)
            plot_metrics(df, fname, mname)

        plot_interval_comparison(interval_storage, fname)

        create_summary_table(results[fname], fname)

    return results


def save_table(df, fname, mname):
    path = os.path.join(OUTPUT_DIR, f"table_{fname}_{mname}.csv")
    df.to_csv(path, index=False)


def create_summary_table(method_results, fname):
    rows = []

    for mname, df in method_results.items():
        best = df.iloc[-1]

        rows.append({
            "method": mname,
            "iterations": best["iterations"],
            "calls": best["calls"],
            "eps": best["eps"]
        })

    summary = pd.DataFrame(rows)
    summary = summary.sort_values("calls")

    summary.to_csv(os.path.join(OUTPUT_DIR, f"summary_{fname}.csv"), index=False)


def plot_metrics(df, fname, mname):
    plt.figure()

    plt.plot(df["eps"], df["iterations"], marker='o', label="Итерации")
    plt.plot(df["eps"], df["calls"], marker='s', label="Вызовы")

    plt.xscale("log")
    plt.gca().invert_xaxis()

    plt.xlabel("eps")
    plt.title(f"{fname} - {mname}")
    plt.legend()

    path = os.path.join(OUTPUT_DIR, f"metrics_{fname}_{mname}.png")
    plt.savefig(path)
    plt.close()


def save_interval_plot(intervals, fname, mname):
    if not intervals:
        return

    a_vals, b_vals = zip(*intervals)

    plt.figure()
    plt.plot(a_vals, label="a_k")
    plt.plot(b_vals, label="b_k")

    plt.xlabel("Итерации")
    plt.ylabel("Границы интервала")
    plt.title(f"{fname} - {mname}")
    plt.legend()

    path = os.path.join(OUTPUT_DIR, f"interval_{fname}_{mname}.png")
    plt.savefig(path)
    plt.close()


def plot_interval_comparison(interval_storage, fname):
    plt.figure()

    for mname, intervals in interval_storage.items():
        if len(intervals) < 2:
            continue

        widths = [b - a for a, b in intervals[:25]]
        while len(widths) < 25:
            widths.append(widths[-1])
        plt.plot(widths, label=mname)

    plt.xlabel("Итерации")
    plt.ylabel("Длина интервала")
    plt.title(f"Сравнение сходимости ({fname})")
    plt.legend()

    path = os.path.join(OUTPUT_DIR, f"interval_compare_{fname}.png")
    plt.savefig(path)
    plt.close()


if __name__ == "__main__":
    results = run_all()

    print(f"Результаты сохранены в /{OUTPUT_DIR}")
