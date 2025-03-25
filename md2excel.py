import pandas as pd
import io

def markdown_to_excel(md_file: str, excel_file: str):
    """Convert a Markdown table from a file to an Excel file."""
    with open(md_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Remove header separator (---) and empty lines
    table_lines = [line.strip() for line in lines if "---" not in line and line.strip()]

    # Convert list back to a single string for StringIO
    table_text = "\n".join(table_lines)

    # Use io.StringIO instead of pandas.compat.StringIO
    df = pd.read_csv(io.StringIO(table_text), sep="|", skipinitialspace=True)

    # Drop empty first and last columns (caused by leading/trailing '|')
    df = df.iloc[:, 1:-1]

    # Clean column names
    df.columns = [col.strip() for col in df.columns]

    # Strip whitespace from all data
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    # Save to Excel
    df.to_excel(excel_file, index=False, engine='openpyxl')

    print(f"Excel file saved: {excel_file}")

# Example Usage
markdown_to_excel("table.md", "table.xlsx")
