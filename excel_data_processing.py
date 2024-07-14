import pandas as pd
from datetime import datetime
import os


# Add a new expense
def add_expense(df, item, category, cost):
    new_expense = pd.DataFrame({"item": [item], "category": [category], "cost": [cost]})
    df = pd.concat([df, new_expense], ignore_index=True)
    #print(df)
    return df

# Create a Pandas dataframe from some data.
data = {
    "item": ["Rewe", "Schuhe", "Bäcker", "Restaurant"],
    "category": ["Lebensmittel", "Klamotten", "Lebensmittel", "Restaurant"],
    "cost": [122, 28., 3.55, 40],
}
df = pd.DataFrame(data)

# Order the columns if necessary.
df = df[["item", "category", "cost"]]

# Calculate total monthly expenses
monthly_total_expenses = df['cost'].sum()

# Dateipfad erstellen
file_path = os.path.join("Project", "test_excel_data_processing.xlsx")


# Write the dataframe data to XlsxWriter.
def write_to_excel(df, file_path, receipt_issue_month=None, receipt_issue_year=None):
    # Current month and year
    current_month = datetime.now().month
    current_year = datetime.now().year

    # Use the provided receipt_issue_month and receipt_issue_year or default to current month and year
    if receipt_issue_month is None:
        receipt_issue_month = current_month
    if receipt_issue_year is None:
        receipt_issue_year = current_year

    sheet_name = f"{receipt_issue_month}_{receipt_issue_year}"

    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter(file_path, engine="xlsxwriter")

    # Write the dataframe to the specified sheet, removing any existing data
    df.to_excel(writer, sheet_name=sheet_name, startrow=1, header=False, index=False)

    # Get the xlsxwriter workbook and worksheet objects.
    workbook = writer.book
    worksheet = writer.sheets[sheet_name]

    # Get the dimensions of the dataframe.
    max_row, max_col = df.shape

    # Create a list of column headers, to use in add_table().
    column_settings = [{"header": column} for column in df.columns]

    # Add the Excel table structure. Pandas will add the data.
    worksheet.add_table(0, 0, max_row, max_col - 1, {"columns": column_settings})

    # Make the columns wider for clarity.
    worksheet.set_column(0, max_col - 1, 12)

    # Gesamtausgaben hinzufügen
    worksheet.write(max_row + 2, 0, "Monthly total expenses:")
    worksheet.write(max_row + 2, 1, monthly_total_expenses)

    # Close the Pandas Excel writer and output the Excel file.
    writer._save()

# Test the excel function
df = add_expense(df, "Rewe", "Lebensmittel", 66.77)
write_to_excel(df, file_path, receipt_issue_month=2, receipt_issue_year=2024)