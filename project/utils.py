from typing import Sized


N_COUNTRIES_WORLD = 195
N_COUNTRIES_AMERICAS = 35


def len_as_expected(list: Sized, expected: int, tolerance=0.1):
    expected_range = range(
        int(expected * (1.0 - tolerance)),
        int(expected * (1.0 + tolerance)) + 1,
    )
    return len(list) in expected_range
