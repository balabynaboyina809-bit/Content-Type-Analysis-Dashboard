from pathlib import Path
import sys

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# -----------------------------
# Configuration
# -----------------------------
DEFAULT_FILES = [
    "Dataset_NotGiven_Empty.csv",
    "netflix_cleaned.csv",
    "cleaned_netflix.csv",
]

OUTPUT_DIR = Path("outputs")


def find_dataset() -> Path:
    """Find a dataset from a command-line argument or common filenames."""
    if len(sys.argv) > 1:
        path = Path(sys.argv[1])
        if not path.exists():
            raise FileNotFoundError(f"Dataset not found: {path}")
        return path

    for filename in DEFAULT_FILES:
        path = Path(filename)
        if path.exists():
            return path

    # Fallback: find any CSV in the current directory.
    csv_files = list(Path(".").glob("*.csv"))
    if len(csv_files) == 1:
        return csv_files[0]

    raise FileNotFoundError(
        "No dataset found. Put your CSV in this folder or run:\n"
        "python netflix_content_analysis.py path/to/your_dataset.csv"
    )


def load_data(file_path: Path) -> pd.DataFrame:
    """Load the Netflix CSV dataset."""
    df = pd.read_csv(file_path)

    # Make column matching slightly more robust.
    df.columns = df.columns.str.strip()

    if "type" not in df.columns:
        # Try to locate the column without relying on capitalization.
        type_column = next(
            (col for col in df.columns if col.lower() == "type"),
            None
        )
        if type_column is None:
            raise ValueError(
                "The dataset must contain a 'type' column with values "
                "'Movie' and/or 'TV Show'."
            )
        df = df.rename(columns={type_column: "type"})

    return df


def analyze_content_type(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate counts and percentages for Movies and TV Shows."""
    content = df["type"].dropna().astype(str).str.strip()

    counts = content.value_counts()

    # Keep the two expected Netflix content types first.
    preferred_order = ["Movie", "TV Show"]
    ordered_types = [x for x in preferred_order if x in counts.index]
    ordered_types += [x for x in counts.index if x not in ordered_types]

    result = pd.DataFrame({
        "content_type": ordered_types,
        "count": [counts[x] for x in ordered_types],
    })

    result["percentage"] = (
        result["count"] / result["count"].sum() * 100
    )

    return result


def print_summary(summary: pd.DataFrame, total_rows: int) -> None:
    """Print analysis results and key findings."""
    analyzed_total = int(summary["count"].sum())

    print("\n" + "=" * 55)
    print("NETFLIX CONTENT TYPE ANALYSIS")
    print("=" * 55)
    print(f"Total dataset rows       : {total_rows:,}")
    print(f"Rows used for type check : {analyzed_total:,}")
    print()

    print("Content distribution:")
    for _, row in summary.iterrows():
        print(
            f"  {row['content_type']:<10} "
            f"{int(row['count']):>6,} "
            f"({row['percentage']:.2f}%)"
        )

    if not summary.empty:
        largest = summary.loc[summary["count"].idxmax()]
        print("\nKey finding:")
        print(
            f"  {largest['content_type']} has the largest share of the "
            f"content in this dataset ({largest['percentage']:.2f}%)."
        )

    print("=" * 55 + "\n")


def create_bar_chart(summary: pd.DataFrame) -> None:
    """Create and save a bar chart."""
    OUTPUT_DIR.mkdir(exist_ok=True)

    plt.figure(figsize=(9, 6))
    ax = sns.barplot(
        data=summary,
        x="content_type",
        y="count",
        errorbar=None
    )

    ax.set_title("Netflix Content Type Distribution", fontsize=16, fontweight="bold")
    ax.set_xlabel("Content Type", fontsize=12)
    ax.set_ylabel("Number of Titles", fontsize=12)

    for container in ax.containers:
        ax.bar_label(container, fmt="%.0f", padding=3)

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "content_type_bar_chart.png", dpi=300)
    plt.show()
    plt.close()


def create_pie_chart(summary: pd.DataFrame) -> None:
    """Create and save a pie chart."""
    OUTPUT_DIR.mkdir(exist_ok=True)

    plt.figure(figsize=(8, 8))

    labels = summary["content_type"].tolist()
    values = summary["count"].tolist()

    plt.pie(
        values,
        labels=labels,
        autopct="%1.1f%%",
        startangle=90
    )

    plt.title(
        "Netflix Movies vs TV Shows",
        fontsize=16,
        fontweight="bold"
    )

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "content_type_pie_chart.png", dpi=300)
    plt.show()
    plt.close()


def main() -> None:
    """Run the complete analysis."""
    try:
        dataset_path = find_dataset()
        print(f"Loading dataset: {dataset_path}")

        df = load_data(dataset_path)
        summary = analyze_content_type(df)

        if summary.empty:
            raise ValueError(
                "No usable values were found in the 'type' column."
            )

        print_summary(summary, len(df))

        create_bar_chart(summary)
        create_pie_chart(summary)

        # Save the summary table as a CSV for easy reporting.
        OUTPUT_DIR.mkdir(exist_ok=True)
        summary.to_csv(
            OUTPUT_DIR / "content_type_summary.csv",
            index=False
        )

        print("Analysis completed successfully.")
        print(f"Output files are available in: {OUTPUT_DIR.resolve()}")

    except Exception as exc:
        print(f"\nError: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()

