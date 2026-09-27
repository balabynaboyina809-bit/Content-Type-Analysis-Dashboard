# Netflix Content Type Analysis Dashboard

## Project Overview
This project analyzes the distribution of **Movies** and **TV Shows** available on Netflix.

It follows the requirements of **Task 2 (Easy) – Content Type Analysis Dashboard**:
1. Load the cleaned Netflix dataset.
2. Calculate the total number of Movies and TV Shows.
3. Create visualizations for content distribution.
4. Compare the proportions of Movies and TV Shows.
5. Summarize the key findings.

## Skills Used
- Python
- Pandas
- Matplotlib
- Seaborn
- Exploratory Data Analysis (EDA)
- Data Visualization

## Dataset
The Python script expects a cleaned Netflix dataset in CSV format.

By default, it looks for:
- `netflix_titles.csv`
- `netflix_cleaned.csv`
- `cleaned_netflix.csv`

You can also provide a CSV file path directly:

```bash
python netflix_content_analysis.py path/to/your_file.csv
```

The dataset should contain a column named `type` with values such as:
- `Movie`
- `TV Show`

## Installation

Install the required libraries:

```bash
pip install pandas matplotlib seaborn
```

## How to Run

Place the Python file and CSV dataset in the same folder, then run:

```bash
python netflix_content_analysis.py
```

Or specify the dataset:

```bash
python netflix_content_analysis.py netflix_titles.csv
```

## Output

The script:
- Displays the total number of Movies and TV Shows.
- Calculates their percentages.
- Prints a summary of the distribution.
- Creates a **bar chart** comparing Movies and TV Shows.
- Creates a **pie chart** showing their percentage distribution.
- Saves the charts in an `outputs` folder:
  - `content_type_bar_chart.png`
  - `content_type_pie_chart.png`

## Example Finding
The exact numbers depend on the dataset used. After execution, the script automatically reports which content type has the larger share and the percentage of each type.

## Project Structure

```text
Netflix-Content-Type-Analysis/
│
├── netflix_content_analysis.py
├── netflix_titles.csv
├── README.md
│
└── outputs/
    ├── content_type_bar_chart.png
    └── content_type_pie_chart.png
```

## Notes
- Missing values in the `type` column are excluded from the content-type analysis.
- The script validates that the required `type` column exists.
- The analysis is based only on the records present in the supplied dataset.

