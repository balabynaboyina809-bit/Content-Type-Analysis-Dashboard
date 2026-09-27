from pathlib import Path
import sys

import pandas as pd
import matplotlib.pyplot as plt


# --------------------------------
# Configuration
# --------------------------------
DEFAULT_FILES = [
    "Dataset_NotGiven_Empty.csv",
    "netflix_cleaned.csv",
    "cleaned_netflix.csv",
]

OUTPUT_DIR = Path("outputs")


# --------------------------------
# Find Dataset
# --------------------------------
def find_dataset():
    if len(sys.argv) > 1:
        path = Path(sys.argv[1])

        if not path.exists():
            raise FileNotFoundError(f"Dataset not found: {path}")

        return path

    for filename in DEFAULT_FILES:
        path = Path(filename)

        if path.exists():
            return path

    csv_files = list(Path(".").glob("*.csv"))

    if len(csv_files) == 1:
        return csv_files[0]

    raise FileNotFoundError(
        "No dataset found. Please put Dataset.csv in the project folder."
    )


# --------------------------------
# Load Dataset
# --------------------------------
def load_data(file_path):

    print(f"Loading dataset: {file_path}")

    df = pd.read_csv(file_path)

    df.columns = df.columns.str.strip()

    if "type" not in df.columns:

        type_column = None

        for column in df.columns:
            if column.lower() == "type":
                type_column = column
                break

        if type_column is None:
            raise ValueError(
                "The dataset does not contain a 'type' column."
            )

        df.rename(columns={type_column: "type"}, inplace=True)

    return df


# --------------------------------
# Analyze Movies and TV Shows
# --------------------------------
def analyze_content(df):

    content = (
        df["type"]
        .dropna()
        .astype(str)
        .str.strip()
    )

    counts = content.value_counts()

    summary = pd.DataFrame({
        "Content Type": counts.index,
        "Count": counts.values
    })

    summary["Percentage"] = (
        summary["Count"]
        / summary["Count"].sum()
        * 100
    )

    return summary


# --------------------------------
# Print Results
# --------------------------------
def print_results(summary, total_rows):

    print()
    print("=" * 55)
    print("       NETFLIX CONTENT TYPE ANALYSIS")
    print("=" * 55)

    print(f"Total dataset rows: {total_rows:,}")
    print()

    print("Content Distribution:")
    print("-" * 55)

    for _, row in summary.iterrows():

        print(
            f"{row['Content Type']:<15}"
            f"{int(row['Count']):>8,}"
            f"     {row['Percentage']:.2f}%"
        )

    print("-" * 55)

    largest = summary.loc[summary["Count"].idxmax()]

    print()
    print("Key Finding:")
    print(
        f"{largest['Content Type']} has the largest share "
        f"({largest['Percentage']:.2f}%)."
    )

    print("=" * 55)
    print()


# --------------------------------
# BAR CHART
# --------------------------------
def create_bar_chart(summary):

    OUTPUT_DIR.mkdir(exist_ok=True)

    plt.close("all")

    fig, ax = plt.subplots(figsize=(9, 6))

    bars = ax.bar(
        summary["Content Type"],
        summary["Count"]
    )

    ax.set_title(
        "Netflix Content Type Distribution",
        fontsize=16,
        fontweight="bold"
    )

    ax.set_xlabel("Content Type")
    ax.set_ylabel("Number of Titles")

    # Add numbers above bars
    for bar in bars:

        height = bar.get_height()

        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height,
            f"{int(height):,}",
            ha="center",
            va="bottom"
        )

    fig.tight_layout()

    output_file = OUTPUT_DIR / "content_type_bar_chart.png"

    fig.savefig(
        output_file,
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()

    plt.close(fig)

    print(f"Bar chart saved: {output_file}")


# --------------------------------
# PIE CHART
# --------------------------------
def create_pie_chart(summary):

    OUTPUT_DIR.mkdir(exist_ok=True)

    plt.close("all")

    fig, ax = plt.subplots(figsize=(8, 8))

    values = summary["Count"].tolist()
    labels = summary["Content Type"].tolist()

    ax.pie(
        values,
        labels=labels,
        autopct="%1.1f%%",
        startangle=90
    )

    ax.set_title(
        "Netflix Movies vs TV Shows",
        fontsize=16,
        fontweight="bold"
    )

    # Make sure the pie is circular
    ax.axis("equal")

    fig.tight_layout()

    output_file = OUTPUT_DIR / "content_type_pie_chart.png"

    fig.savefig(
        output_file,
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()

    plt.close(fig)

    print(f"Pie chart saved: {output_file}")


# --------------------------------
# Main Program
# --------------------------------
def main():

    try:

        # Find dataset
        dataset_path = find_dataset()

        # Load dataset
        df = load_data(dataset_path)

        # Analyze data
        summary = analyze_content(df)

        if summary.empty:
            raise ValueError(
                "No data found in the 'type' column."
            )

        # Print results
        print_results(
            summary,
            len(df)
        )

        # Create charts
        create_bar_chart(summary)

        create_pie_chart(summary)

        # Save summary
        OUTPUT_DIR.mkdir(exist_ok=True)

        summary.to_csv(
            OUTPUT_DIR / "content_type_summary.csv",
            index=False
        )

        print()
        print("Analysis completed successfully!")
        print()
        print(
            f"Files saved in: {OUTPUT_DIR.resolve()}"
        )

    except Exception as error:

        print()
        print("ERROR:")
        print(error)

        sys.exit(1)


# --------------------------------
# Run Program
# --------------------------------
if __name__ == "__main__":
    main()
