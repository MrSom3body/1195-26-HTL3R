__author__ = "Karun Sandhu"



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
            inv = pow(x, -1, n)
            result = my_pow(inv, -b, n)
    elif b % 2 == 0:
        half_pow = my_pow(x, b // 2, n)
        result = half_pow * half_pow
    else:
        half_pow = my_pow(x, (b - 1) // 2, n)
        result = half_pow * half_pow * x
    return result % n if n is not None else result


if __name__ == "__main__":
    import doctest

    doctest.testmod()
