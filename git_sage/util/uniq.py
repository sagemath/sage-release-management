from __future__ import absolute_import, division, print_function, unicode_literals

from typing import Iterable, List, Set, TypeVar

T = TypeVar('T')


def uniq(iterable: Iterable[T]) -> List[T]:
    """
    Return unique items without changing order

    Given an iterable producing possibly duplicate items, this function returns the list of distinct
    items in the iterable, without changing their order. Only subsequent duplicates are removed.

    Args:
        iterable: iterable whose values are hashable
    Returns:
        list: elements of the collection with duplicates removed. The order is preserved, except
            that later duplicate elements are dropped.
    """
    result = []
    seen = set()  # type: Set[T]
    for item in iterable:
        if item in seen:
            continue
        result.append(item)
        seen.add(item)
    return result
