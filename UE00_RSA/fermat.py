__author__ = "Karun Sandhu"

from collections import Counter


def fermat(p: int) -> Counter:
    """
    Gets a Counter object with all fermat results of a number p.

    :param p: the number p
    :return: the Counter object

    >>> c = fermat(9); c.most_common()
    [(1, 2), (4, 2), (0, 2), (7, 2)]
    >>> c = fermat(15); c.most_common()
    [(1, 4), (4, 4), (9, 2), (10, 2), (6, 2)]
    """
    if p < 2:
        raise ValueError("p must be greater than 1")
    fermat_list: list[int] = []
    for a in range(1, p):
        fermat_list.append(pow(a, p - 1, p))

    return Counter(fermat_list)


def print_fermat(p: int) -> None:
    """
    Prints all possible fermat of a number p

    :param p: the number p

    >>> print_fermat(2)
    2 -> 100 % -> res[1]=1, len(res)=1 - [(1, 1)]
    >>> print_fermat(9)
    9 ->  25 % -> res[1]=2, len(res)=4 - [(1, 2), (4, 2), (0, 2), (7, 2)]
    """
    res = fermat(p)
    percent = int((res[1] / res.total()) * 100)
    output = f"{p} -> {percent:3d} % -> res[1]={res[1]}, len(res)={len(res)} - {list(res.items())}"
    print(output)


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    for i in [2, 3, 5, 7, 11, 997, 9, 15, 21]:
        print_fermat(i)

    for i in range(551, 570):
        print_fermat(i)

    for i in [6601, 8911]:
        print_fermat(i)
