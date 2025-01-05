from typing import Sized

CHUNK_SIZE = 1024 * 8
YES = ("yes", "true", "1")
WESTERN_HEMISPHERE = (-180, -90, 0, 90)
N_COUNTRIES_WORLD = 195
COUNTRY_CLASS = "Admin-0 country"
DEPENDENCY_CLASS = "Admin-0 dependency"
AMERICAN_CONTINENTS = ["North America", "South America"]
AMERICAN_COUNTRIES = [
    "ARG",
    "ATG",
    "BHS",
    "BLZ",
    "BOL",
    "BRA",
    "BRB",
    "CAN",
    "CHL",
    "COL",
    "CRI",
    "CUB",
    "DMA",
    "DOM",
    "ECU",
    "GRD",
    "GTM",
    "GUY",
    "HND",
    "HTI",
    "JAM",
    "KNA",
    "LCA",
    "MEX",
    "NIC",
    "PAN",
    "PER",
    "PRY",
    "SLV",
    "SUR",
    "TTO",
    "URY",
    "USA",
    "VCT",
    "VEN",
]


def len_as_expected(list: Sized, expected: int, tolerance=0.1):
    expected_range = range(
        int(expected * (1.0 - tolerance)),
        int(expected * (1.0 + tolerance)) + 1,
    )
    return len(list) in expected_range
