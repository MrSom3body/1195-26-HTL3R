__author__ = "Karun Sandhu"

import csv
import json
import math
import timeit
from math import gcd, isclose
from pprint import pprint


def my_pow(x: int, b: int, n: int | None = None) -> float:
    """
    Computes x raised to the power of b using recursion and exponentiation by squaring.

    :param x: The base number.
    :param b: The exponent (can be a positive or negative integer).
    :return: The result of x raised to the power of b.

    >>> pow(2, 0)
    1
    >>> pow(2, 3)
    8
    >>> pow(2, -1)
    0.5
    >>> pow(3, 4)
    81
    >>> pow(5, -2)
    0.04
    """
    if b == 0:
        result = 1
    elif b < 0:
        if n is None:
            result = 1 / my_pow(x, -b)
        else:
            if gcd(x, n) != 1:
                raise ValueError(
                    "No modular inverse exists for given base and modulus."
                )
            inv = my_pow(x, -1, n)
            result = my_pow(int(inv), -b, n)
    elif b % 2 == 0:
        half_pow = my_pow(x, b // 2, n)
        result = half_pow * half_pow
    else:
        half_pow = my_pow(x, (b - 1) // 2, n)
        result = half_pow * half_pow * x
    return result % n if n is not None else result


def digit_count(num: int) -> int:
    """Return the number of digits in an integer without converting it to a string."""
    if num == 0:
        return 1
    return int(math.log10(abs(num))) + 1


def benchmark_to_csv(filename="benchmark_results.csv"):
    tests = [
        (2, 0, None),
        (2, 3, None),
        (5, -2, None),
        (7, 4, None),
        (2, 20, None),
        (3, 100, 13),
        (10, 0, 7),
        (3, 200, 17),
        (5, -3, None),
        (2, 1000, None),
        (5, 10_000, None),
        (7, 200_000, None),
        (3, 123_456, 17),
        (11, 1_000_000, None),
    ]

    with open(filename, "w", newline="") as csvfile:
        fieldnames = [
            "expression",
            "correct",
            "my_pow_digits",
            "pow_digits",
            "my_pow_time",
            "pow_time",
            "speed_ratio",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for x, b, n in tests:
            expr = f"{x}^{b}" + (f" mod {n}" if n is not None else "")

            builtin = pow(x, b, n) if n is not None and b >= 0 else pow(x, b)
            custom = my_pow(x, b, n)

            # correctness check (allow float tolerance)
            correct = (
                isclose(builtin, custom, rel_tol=1e-9)
                if isinstance(builtin, float)
                else builtin == custom
            )

            # time both functions (5 runs each)
            my_time = timeit.timeit(lambda: my_pow(x, b, n), number=5)
            py_time = timeit.timeit(
                lambda: pow(x, b, n) if n is not None and b >= 0 else pow(x, b),
                number=5,
            )

            # store digit counts safely
            my_digits = digit_count(custom) if isinstance(custom, int) else None
            pow_digits = digit_count(builtin) if isinstance(builtin, int) else None

            writer.writerow(
                {
                    "expression": expr,
                    "correct": correct,
                    "my_pow_digits": my_digits,
                    "pow_digits": pow_digits,
                    "my_pow_time": round(my_time, 6),
                    "pow_time": round(py_time, 6),
                    "speed_ratio": round(my_time / py_time, 2) if py_time > 0 else None,
                }
            )

    print(f"✅ Benchmark results written to {filename}")


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    benchmark_to_csv()
