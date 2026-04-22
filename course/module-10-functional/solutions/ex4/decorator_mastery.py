import time
from collections.abc import Callable
from functools import wraps
from typing import Any


def spell_timer(func: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        print(f"Casting {func.__name__}...")
        t0 = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - t0
        print(f"Spell completed in {elapsed:.3f} seconds")
        return result

    return wrapper


def power_validator(
    min_power: int,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(power: int, *args: Any, **kwargs: Any) -> Any:
            if power < min_power:
                return "Insufficient power for this spell"
            return func(power, *args, **kwargs)

        return wrapper

    return decorator


def retry_spell(
    max_attempts: int,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if attempt < max_attempts:
                        print(
                            f"Spell failed, retrying... "
                            f"(attempt {attempt}/{max_attempts})"
                        )
            return (
                f"Spell casting failed after {max_attempts} attempts"
            )

        return wrapper

    return decorator


class MageGuild:
    @staticmethod
    def validate_mage_name(name: str) -> bool:
        if len(name) < 3:
            return False
        return all(c.isalpha() or c == " " for c in name)

    @staticmethod
    @power_validator(min_power=10)
    def _cast_impl(power: int, spell_name: str) -> str:
        return f"Successfully cast {spell_name} with {power} power"

    def cast_spell(self, spell_name: str, power: int) -> str:
        return self._cast_impl(power, spell_name)


@spell_timer
def fireball() -> str:
    time.sleep(0.1)
    return "Fireball cast!"


@retry_spell(max_attempts=3)
def _flaky_spell() -> str:
    raise RuntimeError("boom")


@retry_spell(max_attempts=3)
def _stubborn_spell() -> str:
    return "Waaaaaaagh spelled !"


if __name__ == "__main__":
    print("Testing spell timer...")
    result = fireball()
    print(f"Result: {result}")

    print()
    print("Testing retrying spell...")
    print(_flaky_spell())
    print(_stubborn_spell())

    print()
    print("Testing MageGuild...")
    print(MageGuild.validate_mage_name("Alex"))
    print(MageGuild.validate_mage_name("A1"))
    guild = MageGuild()
    print(guild.cast_spell("Lightning", 15))
    print(guild.cast_spell("Lightning", 5))
