__author__ = "Karun Sandhu"


import math
from UE00_RSA.miller_rabin import generate_prime
from random import SystemRandom


def generate_keys(
    number_of_bits: int,
) -> tuple[tuple[int, int, int], tuple[int, int, int]]:
    """
    Generates a pair of RSA keys.

    :param number_of_bits: The desired bit length of the modulus n.
    :return: A tuple containing the public key (e, n, number_of_bits) and the private key (d, n, number_of_bits).

    >>> public, private = generate_keys(256)
    >>> e, n, _ = public
    >>> d, _, _ = private
    >>> test_values = [
    ...     0,
    ...     1,
    ...     42,
    ...     123456,
    ...     2**16,
    ...     2**128 - 1,
    ...     n - 1,
    ... ]

    >>> for x in test_values:
    ...     c = pow(x, e, n)
    ...     y = pow(c, d, n)
    ...     assert x == y, f"Round‑trip failed for {x}"
    """
    while True:
        p = generate_prime(number_of_bits // 2)
        q = generate_prime(number_of_bits // 2)
        n = p * q
        if p != q and n.bit_length() >= number_of_bits:
            break

    phi = (p - 1) * (q - 1)

    while True:
        e = SystemRandom().randint(phi**2, phi**8)
        if math.gcd(e, phi) == 1:
            break

    d = pow(e, -1, phi)

    return (e, n, number_of_bits), (d, n, number_of_bits)


if __name__ == "__main__":
    import doctest

    _ = doctest.testmod()
