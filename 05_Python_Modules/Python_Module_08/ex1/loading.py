import sys
import importlib
from typing import Any
# try:
#     import pandas as pd

#     pandas_version = pd.__version__
#     print(f"f[OK] pandas {pandas_version}")

# except ImportError:
#     print(f"[ERROR] pandas is missing. Please install it.")


def check_dependencies() -> dict[str, Any]:
    print("LOADING STATUS: Loading programs...")
    print("Checking dependencies:")

    required_packages = ["pandas", "numpy", "matplotlib", "requests"]
    loaded_modules: dict[str, Any] = {}
    missing_packages = []

    for package in required_packages:
        try:
            module = importlib.import_module(package)

            version = getattr(module, "__version__", "unknown")
            print(f"[OK] {package} ({version})")

            loaded_modules[package] = module

        except ImportError:
            print(f"[ERROR] {package} is missing.")
            missing_packages.append(package)

    if missing_packages:
        print("\nCRITICAL ERROR: Missing required programs.")
        print("Install them using pip or poetry to enter the Matrix.")
        sys.exit(1)

    print("Data manipulation ready")
    print("Numerical computation ready")
    print("Network access ready")
    print("Visualization ready")

    return loaded_modules


def analyze_matrix_surge(modules: dict[str, Any]) -> None:
    """Simulate, process, and visualize Matrix power surges."""
    np = modules["numpy"]
    pd = modules["pandas"]

    plt = importlib.import_module("matplotlib.pyplot")

    print("Analyzing Matrix data...")
    print("Processing 100 data points...")

    time = np.linspace(0, 20, 1000)
    base_wave = np.sin(time)

    noise = np.random.normal(0, 0.5, 1000)
    power_levels = base_wave + noise

    df = pd.DataFrame({"Time": time, "Raw_Surge": power_levels})
    df["Smoothed_Surge"] = df["Raw_Surge"].rolling(window=50).mean()

    print("Generating visualization...")
    plt.figure(figsize=(10, 5))

    plt.plot(
        df["Time"], df["Raw_Surge"],
        color='lightgreen', alpha=0.5, label='Raw Zion Power'
        )
    plt.plot(
        df["Time"], df["Smoothed_Surge"],
        color='darkgreen', linewidth=2, label='Surge_Trend'
        )

    plt.title("Zion Mainframe Power Surge Analysis")
    plt.xlabel("Time Cycle")
    plt.ylabel("power Level")
    plt.legend()
    plt.grid(True, alpha=0.3)

    plt.savefig("matrix_analysis.png")

    print("Analysis complete!")
    print("Results saved to: matrix_analysis.png")


if __name__ == "__main__":

    matrix_modules = check_dependencies()
    analyze_matrix_surge(matrix_modules)
