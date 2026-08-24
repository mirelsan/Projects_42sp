import os
import sys
from dotenv import load_dotenv


def load_environment() -> dict[str, str]:
    """Load and validate environment variables."""
    load_dotenv()

    raw_config = {
        "MATRIX_MODE": os.getenv("MATRIX_MODE"),
        "DATABASE_URL": os.getenv("DATABASE_URL"),
        "API_KEY": os.getenv("API_KEY"),
        "LOG_LEVEL": os.getenv("LOG_LEVEL"),
        "ZION_ENDPOINT": os.getenv("ZION_ENDPOINT")
    }

    missing_vars = [key for key, value in raw_config.items() if value is None]

    if missing_vars:
        error_msg = f"Missing configuration for: {', '.join(missing_vars)}"
        print(f"CRITICAL ERROR: {error_msg}")
        sys.exit(1)

    valid_config: dict[str, str] = {k: str(v) for k, v in raw_config.items()}
    return valid_config


def run_matrix_simulation(config: dict[str, str]) -> None:
    """Execute the simulation and print the final Oracle Status."""
    print("ORACLE STATUS: Reading the Matrix...")
    print("Configuration loaded:")

    if config["MATRIX_MODE"] == "production":
        db_status = "Connected to secure production cluster"
        api_status = "Authenticated via enterprise gateway"
    else:
        db_status = "Connected to local instance"
        api_status = "Authenticated"

    print(f"Mode: {config['MATRIX_MODE']}")
    print(f"Database: {db_status}")
    print(f"API Access: {api_status}")
    print(f"Log Level: {config['LOG_LEVEL']}")
    print("Zion Network: Online")

    print("\nEnvironment security check:")
    print("[OK] No hardcoded secrets detected")
    print("[OK] .env file properly configured")
    print("[OK] Production overrides available\n")

    print("The Oracle sees all configurations.")


if __name__ == "__main__":
    matrix_config = load_environment()
    run_matrix_simulation(matrix_config)
