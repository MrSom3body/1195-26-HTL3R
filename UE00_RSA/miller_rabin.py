__author__ = "Karun Sandhu"

from random import randint


def is_prime_miller_rabin(n: int, k: int) -> bool:
    """
    Perform the Miller–Rabin probabilistic primality test.

    :param n: odd integer greater than 3 to test for primality
    :param k: number of rounds to perform (higher = more confidence)
    :return: True if "probably prime", False if "composite"

    >>> is_prime_miller_rabin(4, 5)
    False
    >>> is_prime_miller_rabin(89, 5)  # 89 is prime
    True
    >>> is_prime_miller_rabin(91, 5)  # 91 = 7 * 13
    False
    >>> is_prime_miller_rabin(7919, 10)  # a larger known prime
    True
    >>> is_prime_miller_rabin(10000, 8)  # even composite
    False
    """
    if n <= 3:
        raise ValueError("n must be greater than 3")

    if k <= 0:
        raise ValueError("k must be at least 1")

    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1

    for _ in range(k):
        a = randint(2, n - 2)
        x = pow(a, d, n)

        if x == 1 or x == n - 1:
            continue

        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
            if x == 1:
                return False
        else:
            return False

    return True


if __name__ == "__main__":
    import doctest

    doctest.testmod()
