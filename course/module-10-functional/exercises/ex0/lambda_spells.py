"""Exercise 0 - Lambda Sanctum.

Authorized helpers: map, filter, sorted, min, max, round, sum, len.
Use lambdas, not named functions, for the short transformations below.
"""


def artifact_sorter(artifacts: list[dict]) -> list[dict]:
    # TODO: sorted(..., key=lambda a: a["power"], reverse=True)
    raise NotImplementedError


def power_filter(mages: list[dict], min_power: int) -> list[dict]:
    # TODO: filter(...) with a lambda, wrapped in list(...)
    raise NotImplementedError


def spell_transformer(spells: list[str]) -> list[str]:
    # TODO: map(...) that prefixes and suffixes each spell name
    raise NotImplementedError


def mage_stats(mages: list[dict]) -> dict:
    # TODO: return {"max_power": ..., "min_power": ..., "avg_power": ...}
    raise NotImplementedError


if __name__ == "__main__":
    # TODO: exercise each function with sample data matching the PDF.
    pass
