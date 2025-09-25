__author__ = "Karun Sandhu"

from random import getrandbits, randint

from UE00_RSA import PRIMES


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


def is_prime(n: int) -> bool:
    """
    Determines whether a given number is prime.

    This function first checks if the number is in a predefined list of small prime numbers (PRIMES).
    If the number is not in the list, it uses the Miller-Rabin primality test to determine primality.

    :param n: the number to check for primality.
    :return: True if the number is prime, False otherwise.

    >>> is_prime(2)
    True
    >>> is_prime(69)
    False
    >>> is_prime(97)
    True
    """
    if n <= PRIMES[-1]:
        return n in PRIMES
    else:
        return is_prime_miller_rabin(n, k=200)


def _get_candidate(bits: int) -> int:
    candidate = getrandbits(bits)
    candidate |= 1 << (bits - 1)
    candidate |= 1
    return candidate


def generate_prime(bits: int) -> int:
    """
    Generates a prime number with a certain number of bits.

    :param bits: number of bits
    :return: a prime number with the given number of bits

    >>> generate_prime(2) in [2, 3]
    True
    >>> generate_prime(3) in [5, 7]
    True
    >>> generate_prime(4) in [11, 13, 17, 19]
    True
    """
    assert bits >= 2, "Number of bits must be at least 2"
    candidate = _get_candidate(bits)
    while not is_prime(candidate):
        candidate = _get_candidate(bits)
    return candidate


if __name__ == "__main__":
    import doctest

    doctest.testmod()
