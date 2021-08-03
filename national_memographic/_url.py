"""
Utility functions for working with URLs.
"""


def join(base: str, path: str) -> str:
    """
    A very naive implementation of URL path concatenation that suffices for
    most use-cases and doesn't suffer from Python's native urljoin function's
    problems.

    :param base: the base URL.
    :param path: a path segment to concatenate the base URL with.
    :return: the concatenated result.
    """

    return base + path
