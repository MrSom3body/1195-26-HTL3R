from collections import deque
from functools import cache
from typing import TypeAlias

my_coins = [1, 200, 2, 100, 5, 50, 10, 20]
deep_list = [1, [2, 3], [4, [5, 6]], 7, [8, [9, [[10]]]]]
graph = {
    "A1": ["B2", "C3"],
    "B2": ["D4", "E5", "F6"],
    "C3": ["E5", "G7"],
    "D4": ["H8"],
    "E5": ["H8", "I9"],
    "F6": ["I9"],
    "G7": ["J0"],
    "H8": ["K1"],
    "I9": ["K1", "L2"],
    "J0": ["L2"],
    "K1": ["M3"],
    "L2": ["M3"],
    "M3": [],
}
graph_large = {
    "A1": ["B2", "C3", "D4"],
    "B2": ["E5", "F6", "G7"],
    "C3": ["F6", "H8"],
    "D4": ["I9", "J0"],
    "E5": ["K1", "L2"],
    "F6": ["L2", "M3", "C3"],
    "G7": ["M3", "N4"],
    "H8": ["N4", "O5"],
    "I9": ["O5", "P6"],
    "J0": ["P6", "Q7"],
    "K1": ["R8"],
    "L2": ["R8", "S9"],
    "M3": ["S9", "T0"],
    "N4": ["T0", "U1"],
    "O5": ["U1", "V2"],
    "P6": ["V2", "W3"],
    "Q7": ["W3", "X4"],
    "R8": ["Y5"],
    "S9": ["Y5", "Z6"],
    "T0": ["Z6", "A7"],
    "U1": ["A7", "B8"],
    "V2": ["B8", "C9"],
    "W3": ["C9", "D0"],
    "X4": ["D0", "E1"],
    "Y5": ["F2"],
    "Z6": ["F2", "G3"],
    "A7": ["G3", "H4"],
    "B8": ["H4", "I5"],
    "C9": ["I5", "J6"],
    "D0": ["J6", "K7"],
    "E1": ["K7", "L8"],
    "F2": ["L8", "M9"],
    "G3": ["M9"],
    "H4": [],
    "I5": [],
    "J6": [],
    "K7": [],
    "L8": [],
    "M9": [],
}
graph_no_path = {
    "A1": ["B2", "C3"],
    "B2": ["D4"],
    "C3": ["E5"],
    "D4": ["F6"],
    "E5": ["B2"],
    "F6": ["C3"],
    "G7": [],
}


NestedIntList: TypeAlias = int | list["NestedIntList"]


@cache
def muenzen(total: int, index: int) -> int:
    """
    Calculates the number of ways to form ``total`` using ``my_coins``.

    Uses recursion with memoization. Ideally, ``my_coins`` should be sorted descendingly for optimization.

    :param total: The target amount to reach.
    :param index: The current index in ``my_coins`` being considered.
    :return: The number of possible combinations.
    """
    if total == 0:
        return 1

    if total < 0 or index >= len(my_coins):
        return 0

    use_coin = muenzen(total - my_coins[index], index)
    skip_coin = muenzen(total, index + 1)

    return use_coin + skip_coin


def max_depth(l: list[NestedIntList]) -> int:
    """
    Determines the maximum nesting depth of a list recursively.

    :param l: An arbitrarily nested list of integers.
    :return: The maximum depth
    """
    max = 0
    for item in l:
        if isinstance(item, list):
            if max_depth(item) > max:
                max = max_depth(item)
    return max + 1


def deep_sum(l: list[NestedIntList]) -> int:
    """
    Calculates the sum of all integers in a nested list recursively.

    :param l: An arbitrarily nested list of integers.
    :return: The sum of all elements.
    """
    sum = 0
    for item in l:
        if isinstance(item, list):
            sum += deep_sum(item)
        elif isinstance(item, int):
            sum += item
    return sum


def deep_sum_with_max_depth(l: list[NestedIntList]) -> tuple[int, int]:
    """
    Computes both the sum and the maximum depth in a single pass.

    :param myList: An arbitrarily nested list of integers.
    :return: A tuple containing ``(sum, max_depth)``.
    """
    sum = 0
    depth = 0
    for item in l:
        if isinstance(item, list):
            sub_sum, sub_depth = deep_sum_with_max_depth(item)
            sum += sub_sum
            if sub_depth > depth:
                depth = sub_depth
        elif isinstance(item, int):
            sum += item
    return (sum, depth + 1)


def min_path_length(graph: dict[str, list[str]], start: str, end: str) -> int:
    """
    Finds the shortest path length between two nodes using BFS.

    :param graph: Adjacency list representation of the graph.
    :param start: The identifier of the start node.
    :param end: The identifier of the end node.
    :return: The number of steps to reach ``end``, or -1 if no path exists.
    """
    queue: deque[tuple[str, int]] = deque([(start, 0)])
    visited: set[str] = {start}

    while queue:
        current_node, distance = queue.popleft()

        for neighbor in graph.get(current_node, []):
            if neighbor == end:
                return distance + 1

            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, distance + 1))

    return -1


if __name__ == "__main__":
    print("muenzen(400, 0):", muenzen(400, 0))
    print("deep_sum(deep_list):", deep_sum(deep_list))
    print("max_depth(deep_list):", max_depth(deep_list))
    print("max_depth([]):", max_depth([]))
    print("deep_sum_with_max_depth(deep_list):", deep_sum_with_max_depth(deep_list))
    print("deep_sum_with_max_depth([]):", deep_sum_with_max_depth([]))
    print('min_path_length(graph, "A1", "M3"):', min_path_length(graph, "A1", "M3"))
    print(
        'min_path_length(graph_large, "A1", "M3"):',
        min_path_length(graph_large, "A1", "M9"),
    )
    print(
        'min_path_length(graph_no_path, "A1", "M3"):',
        min_path_length(graph_no_path, "A1", "G7"),
    )
