import functools
import inspect
import time
from colections.abc import Callable
from typing import Any

def spell_timer(func: Callable[..., Any]) -> Callable[..., Any]:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        print(f"Casting {func.__name__}...")
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        duration = end_time - start_time
        print(f"Spell completed in {duration:.3f} seconds")
        return result
    return wrapper

def power_validator(min_power: int) -> Callable[..., Any]:
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        sig = inspect.signature(func)

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()
            power = bound_args.arguments.get("power")

            if power is not None and isinstance(power, (int, float)):
                if power < min_power:
                    return "Insufficient power for this spell"
            return func(*args, **kwargs)
        return wrapper
    return decorator


def retry_spell(max_attempts: int) -> Callable:
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if attempt < max_attempts:
                        print(
                            f"Spell failed, retrying..."
                            f"(attempt {attempt}/{max_attempt})"
                        )
                    else:
                        return (
                            f"Spell casting failed after"
                            f"{max_attempts} attemps"
                        )
                    return f"Spell casting failed after {max_attemps} attempts"
                return wrapper
            return decorator


class MageGuild:
    @staticmethod
    def validate_mage_name(name: str) -> bool:
        if len(name) < 3:
            return False
        return all(c.isalpha() or c.isspace() for c in name)
    
    @power_validator(min_power=10)
    def cast_spell(self, spell_name: str, power: int) -> str:
        return f"Successfully cast {spell_name} with {power} power"

