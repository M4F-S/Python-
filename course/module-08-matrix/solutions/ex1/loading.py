import importlib
import sys

OPTIONAL_DEPS: list[tuple[str, str]] = [
    ("pandas", "Data manipulation"),
    ("numpy", "Numerical computation"),
    ("matplotlib", "Visualization"),
]


def _version(name: str) -> str | None:
    try:
        mod = importlib.import_module(name)
    except ImportError:
        return None
    return getattr(mod, "__version__", "unknown")


def main() -> None:
    print("LOADING STATUS: Loading programs...")
    print()
    print("Checking dependencies:")

    available: dict[str, str] = {}
    missing: list[str] = []
    for name, description in OPTIONAL_DEPS:
        ver = _version(name)
        if ver is None:
            missing.append(name)
            print(f"[MISSING] {name} - {description} not available")
        else:
            available[name] = ver
            print(f"[OK] {name} ({ver}) - {description} ready")

    if missing:
        print()
        print("Some programs failed to load.")
        print("Install with pip:    pip install -r requirements.txt")
        print("Install with Poetry: poetry install")
        sys.exit(1)

    print()
    print("Analyzing Matrix data...")

    # Imports are deferred until we're sure the deps are available.
    import numpy as np  # noqa: E402
    import pandas as pd  # noqa: E402
    import matplotlib
    matplotlib.use("Agg")  # no-display backend for CI/headless runs
    import matplotlib.pyplot as plt  # noqa: E402

    rng = np.random.default_rng(seed=42)
    n_points = 1000
    data = pd.DataFrame(
        {
            "t": np.arange(n_points),
            "signal": rng.normal(0.0, 1.0, n_points).cumsum(),
        }
    )

    print(f"Processing {n_points} data points...")
    print("Generating visualization...")

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(data["t"], data["signal"], linewidth=0.8)
    ax.set_title("Matrix Data")
    ax.set_xlabel("t")
    ax.set_ylabel("signal")
    fig.tight_layout()
    out_path = "matrix_analysis.png"
    fig.savefig(out_path)
    plt.close(fig)

    print()
    print("Analysis complete!")
    print(f"Results saved to: {out_path}")


if __name__ == "__main__":
    main()
