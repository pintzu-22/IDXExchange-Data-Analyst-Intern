from pathlib import Path
import pandas as pd
import re

# Set the folder that contains all CSV files
data_dir = Path("csv")

# Set the output folder for combined files
output_dir = Path("output")
output_dir.mkdir(exist_ok=True)


def print_section(title):
    """
    Print a clean section title.
    """
    print("\n" + "-" * 50)
    print(title)
    print("-" * 50)


def extract_year_month(file):
    """
    Extract year-month information from the file name.
    Example: CRMLSSold202403.csv -> 202403
    """
    match = re.search(r"(\d{6})", file.stem)
    return match.group(1) if match else None


def is_filled_file(file):
    """
    Check whether the file is a filled file.
    """
    return "_filled" in file.name.lower()


def select_files_by_month(files, label):
    """
    Select one file for each year-month.

    Logic:
    1. If both original and filled files exist for the same month,
       use the original file.
    2. If only the filled file exists for that month,
       use the filled file.
    """
    selected_files = {}

    for file in files:
        ym = extract_year_month(file)

        if ym is None:
            print(f"Warning: Cannot extract year-month from {label} file:", file.name)
            continue

        current_is_filled = is_filled_file(file)

        # If this month has not been selected yet, add the file
        if ym not in selected_files:
            selected_files[ym] = file

        else:
            existing_file = selected_files[ym]
            existing_is_filled = is_filled_file(existing_file)

            # If the existing selected file is filled,
            # but the current file is original, replace it
            if existing_is_filled and not current_is_filled:
                selected_files[ym] = file

            # If both are original or both are filled, keep the first one
            else:
                print(f"Warning: Duplicate {label} files for {ym}. Keeping:", selected_files[ym].name)
                print("Ignored:", file.name)

    return sorted(selected_files.values())


print("Current working folder:", Path.cwd())
print("CSV folder exists:", data_dir.exists())

# Stop the program if the csv folder does not exist
if not data_dir.exists():
    raise FileNotFoundError(
        "Cannot find csv folder. Make sure you run this code inside DA53_PROJECT "
        "and check whether your folder name is csv or CSV."
    )


# --------------------------------------------------
# 1. Find Sold and List files
# --------------------------------------------------

# Find all Sold and List files, including filled files
all_sold_files = sorted(data_dir.rglob("*Sold*.csv"))
all_list_files = sorted(data_dir.rglob("*List*.csv"))

# Select one file per month
# Original file is preferred, but filled file will be used if original is missing
sold_files = select_files_by_month(all_sold_files, "Sold")
list_files = select_files_by_month(all_list_files, "List")


print_section("1. File Count Check")

print("All Sold files found:", len(all_sold_files))
print("All List files found:", len(all_list_files))

print("Sold files selected:", len(sold_files))
print("List files selected:", len(list_files))

if len(sold_files) == 0:
    print("Warning: No Sold files found.")

if len(list_files) == 0:
    print("Warning: No List files found.")


print_section("2. File Name Check")

print("\nSold files selected:")
for f in sold_files:
    file_type = "filled" if is_filled_file(f) else "original"
    print(f"{f.name}  |  {file_type}")

print("\nList files selected:")
for f in list_files:
    file_type = "filled" if is_filled_file(f) else "original"
    print(f"{f.name}  |  {file_type}")


print_section("3. Year-Month Check")

sold_months = [extract_year_month(f) for f in sold_files]
list_months = [extract_year_month(f) for f in list_files]

print("Sold months count:", len(sold_months))
print("List months count:", len(list_months))

print("\nSold months:")
print(sold_months)

print("\nList months:")
print(list_months)

# Check if any selected file name does not contain year-month information
sold_no_month = [f.name for f in sold_files if extract_year_month(f) is None]
list_no_month = [f.name for f in list_files if extract_year_month(f) is None]

if sold_no_month:
    print("\nSold files without year-month:")
    print(sold_no_month)

if list_no_month:
    print("\nList files without year-month:")
    print(list_no_month)


# Compare year-month coverage between Sold and List files
sold_month_set = set(sold_months)
list_month_set = set(list_months)

print("\nMonths in Sold but not in List:")
print(sorted(sold_month_set - list_month_set))

print("\nMonths in List but not in Sold:")
print(sorted(list_month_set - sold_month_set))


def check_duplicate_months(files, label):
    """
    Check whether there are duplicate files for the same year-month.
    This check is done after file selection.
    """
    month_count = {}

    for file in files:
        ym = extract_year_month(file)
        month_count[ym] = month_count.get(ym, 0) + 1

    duplicates = {month: count for month, count in month_count.items() if count > 1}

    if duplicates:
        print(f"\nDuplicate year-months in selected {label} files:")
        print(duplicates)
    else:
        print(f"\nNo duplicate year-months in selected {label} files.")


check_duplicate_months(sold_files, "Sold")
check_duplicate_months(list_files, "List")


print_section("4. Row Count Check")


def check_row_counts(files, label):
    """
    Count the number of rows in each CSV file.
    Only the first column is loaded to make the check faster.
    """
    result = []

    for file in files:
        try:
            df = pd.read_csv(file, usecols=[0], low_memory=False)
            row_count = len(df)

            result.append({
                "file_name": file.name,
                "file_version": "filled" if is_filled_file(file) else "original",
                "year_month": extract_year_month(file),
                "rows": row_count
            })

        except Exception as e:
            result.append({
                "file_name": file.name,
                "file_version": "filled" if is_filled_file(file) else "original",
                "year_month": extract_year_month(file),
                "rows": "ERROR",
                "error": str(e)
            })

    row_df = pd.DataFrame(result)

    print(f"\n{label} row counts:")
    print(row_df.to_string(index=False))

    numeric_rows = pd.to_numeric(row_df["rows"], errors="coerce")

    print(f"\n{label} total rows:", numeric_rows.sum())
    print(f"{label} min rows:", numeric_rows.min())
    print(f"{label} max rows:", numeric_rows.max())

    empty_files = row_df[numeric_rows == 0]
    if len(empty_files) > 0:
        print(f"\nWarning: {label} has empty files:")
        print(empty_files["file_name"].to_list())

    return row_df


sold_row_check = check_row_counts(sold_files, "Sold")
list_row_check = check_row_counts(list_files, "List")


print_section("5. Column Consistency Check")


def check_columns(files, label):
    """
    Check whether all selected files have the same columns and column order.
    Filled files may have extra columns, such as latfilled and lonfilled.
    """
    if len(files) == 0:
        print(f"No {label} files found.")
        return {}

    columns_dict = {}

    for file in files:
        try:
            df = pd.read_csv(file, nrows=0)
            columns_dict[file.name] = list(df.columns)
        except Exception as e:
            print(f"Error reading columns from {file.name}: {e}")

    first_file = list(columns_dict.keys())[0]
    base_cols = columns_dict[first_file]

    print(f"\nChecking {label} columns...")
    print("Base file:", first_file)
    print("Base column count:", len(base_cols))

    all_same = True

    for file_name, cols in columns_dict.items():
        missing_cols = sorted(set(base_cols) - set(cols))
        extra_cols = sorted(set(cols) - set(base_cols))

        if missing_cols or extra_cols:
            all_same = False
            print("\nColumns different:", file_name)
            print("Column count:", len(cols))
            print("Missing columns:", missing_cols)
            print("Extra columns:", extra_cols)

        elif cols != base_cols:
            all_same = False
            print("\nSame columns but different order:", file_name)

    if all_same:
        print(f"All {label} files have the same columns and same order.")
    else:
        print(f"\nNote: Some {label} files have different columns.")
        print("This is okay if the differences come from filled files.")
        print("When combining files, missing columns will be filled with NaN.")

    return columns_dict


sold_columns = check_columns(sold_files, "Sold")
list_columns = check_columns(list_files, "List")


print_section("6. Required Column Check")

required_sold_cols = [
    "ListingKey",
    "ListingId",
    "CloseDate",
    "ClosePrice",
    "ListPrice",
    "City",
    "PostalCode",
    "Latitude",
    "Longitude",
    "PropertyType",
    "LivingArea",
    "BedroomsTotal",
    "BathroomsTotalInteger"
]

required_list_cols = [
    "ListingKey",
    "ListingId",
    "ListingContractDate",
    "ListPrice",
    "City",
    "PostalCode",
    "Latitude",
    "Longitude",
    "PropertyType",
    "LivingArea",
    "BedroomsTotal",
    "BathroomsTotalInteger"
]


def check_required_columns(files, required_cols, label):
    """
    Check whether each selected file contains the required columns for analysis.
    """
    print(f"\nChecking required columns for {label}...")

    all_good = True

    for file in files:
        df = pd.read_csv(file, nrows=0)
        cols = set(df.columns)
        missing = sorted(set(required_cols) - cols)

        if missing:
            all_good = False
            print(file.name, "missing:", missing)

    if all_good:
        print(f"All selected {label} files have required columns.")


check_required_columns(sold_files, required_sold_cols, "Sold")
check_required_columns(list_files, required_list_cols, "List")


print_section("7. Combine Files")


def combine_files(files, data_type):
    """
    Combine multiple CSV files into one DataFrame.
    Add source_file, year_month, data_type, and file_version columns for tracking.
    """
    all_dfs = []

    for file in files:
        print("Reading:", file.name)

        df = pd.read_csv(file, low_memory=False)

        # Add source information for tracking
        df["source_file"] = file.name
        df["year_month"] = extract_year_month(file)
        df["data_type"] = data_type
        df["file_version"] = "filled" if is_filled_file(file) else "original"

        all_dfs.append(df)

    if len(all_dfs) == 0:
        print(f"No files to combine for {data_type}.")
        return pd.DataFrame()

    combined_df = pd.concat(all_dfs, ignore_index=True, sort=False)

    return combined_df


sold_df = combine_files(sold_files, "sold")
list_df = combine_files(list_files, "list")

print("\nCombined sold shape:", sold_df.shape)
print("Combined list shape:", list_df.shape)

# Export combined Sold and List files separately
sold_output_path = output_dir / "combined_sold.csv"
list_output_path = output_dir / "combined_list.csv"

sold_df.to_csv(sold_output_path, index=False)
list_df.to_csv(list_output_path, index=False)

print("\nDone!")
print("Saved:", sold_output_path)
print("Saved:", list_output_path)