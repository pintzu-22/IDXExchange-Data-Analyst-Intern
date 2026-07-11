import pandas as pd
from pathlib import Path


DATA_DIR = Path("output")

combined_sold = pd.read_csv(DATA_DIR / "combined_sold.csv")
combined_list = pd.read_csv(DATA_DIR / "combined_list.csv")


def add_mortgage_rates(
    combined_sold,
    combined_list,
    output_dir=Path("output")
):
    """
    Fetch national 30-year fixed mortgage rates from FRED,
    convert weekly rates to monthly averages,
    merge rates onto combined sold and listings datasets,
    and save enriched CSV files.
    """

    output_dir.mkdir(exist_ok=True)

    print("\n" + "-" * 50)
    print("Mortgage Rate Enrichment")
    print("-" * 50)

    # Step 1: Fetch mortgage rate data from FRED
    url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=MORTGAGE30US"

    mortgage = pd.read_csv(
        url,
        parse_dates=["observation_date"]
    )

    mortgage.columns = ["date", "rate_30yr_fixed"]

    # Step 2: Resample weekly rates to monthly averages
    mortgage["year_month"] = mortgage["date"].dt.to_period("M")

    mortgage_monthly = (
        mortgage.groupby("year_month")["rate_30yr_fixed"]
        .mean()
        .reset_index()
    )

    print("Mortgage monthly rate preview:")
    print(mortgage_monthly.head())

    # Step 3: Create year_month key for sold data using CloseDate
    combined_sold = combined_sold.copy()
    combined_sold["CloseDate"] = pd.to_datetime(
        combined_sold["CloseDate"],
        errors="coerce"
    )

    combined_sold["year_month"] = combined_sold["CloseDate"].dt.to_period("M")

    # Step 4: Create year_month key for listings data
    combined_list = combined_list.copy()

    if "ListingContractDate" in combined_list.columns:
        listing_date_col = "ListingContractDate"
    elif "ListDate" in combined_list.columns:
        listing_date_col = "ListDate"
    elif "OnMarketDate" in combined_list.columns:
        listing_date_col = "OnMarketDate"
    else:
        raise ValueError(
            "No valid listing date column found. "
            "Expected ListingContractDate, ListDate, or OnMarketDate."
        )

    print("Using listing date column:", listing_date_col)

    combined_list[listing_date_col] = pd.to_datetime(
        combined_list[listing_date_col],
        errors="coerce"
    )

    combined_list["year_month"] = combined_list[listing_date_col].dt.to_period("M")

    # Step 5: Merge mortgage rates onto both datasets
    print("Before sold merge:", len(combined_sold))

    combined_sold_with_rates = combined_sold.merge(
        mortgage_monthly,
        on="year_month",
        how="left"
    )

    print("After sold merge:", len(combined_sold_with_rates))


    print("Before list merge:", len(combined_list))
    combined_list_with_rates = combined_list.merge(
        mortgage_monthly,
        on="year_month",
        how="left"
    )
    print("After list merge:", len(combined_list_with_rates))

    # Step 6: Validate merge
    sold_null_rates = combined_sold_with_rates["rate_30yr_fixed"].isna().sum()
    list_null_rates = combined_list_with_rates["rate_30yr_fixed"].isna().sum()

    print("\nValidation check:")
    print("Sold rows with missing mortgage rate:", sold_null_rates)
    print("Listing rows with missing mortgage rate:", list_null_rates)

    if sold_null_rates == 0 and list_null_rates == 0:
        print("Mortgage rate merge validation passed. No missing rates found.")
    else:
        print("Warning: Some rows have missing mortgage rates.")
        print("Check date ranges or missing date values.")

    # Step 7: Preview
    print("\nSold preview:")
    print(
        combined_sold_with_rates[
            ["CloseDate", "year_month", "ClosePrice", "rate_30yr_fixed"]
        ].head()
    )

    print("\nListings preview:")
    preview_cols = [listing_date_col, "year_month", "ListPrice", "rate_30yr_fixed"]
    preview_cols = [col for col in preview_cols if col in combined_list_with_rates.columns]

    print(combined_list_with_rates[preview_cols].head())

    # Step 8: Filter to Residential property type only
    combined_sold_residential_with_rates = combined_sold_with_rates[
        combined_sold_with_rates["PropertyType"]
        .astype(str)
        .str.strip()
        .str.lower()
        .eq("residential")
    ].copy()

    combined_list_residential_with_rates = combined_list_with_rates[
        combined_list_with_rates["PropertyType"]
        .astype(str)
        .str.strip()
        .str.lower()
        .eq("residential")
    ].copy()

    print("\nResidential filter validation:")
    print("Sold full rows:", len(combined_sold_with_rates))
    print("Sold residential rows:", len(combined_sold_residential_with_rates))

    print("List full rows:", len(combined_list_with_rates))
    print("List residential rows:", len(combined_list_residential_with_rates))

    print("\nMissing mortgage rates after residential filter:")
    print(
        "Sold residential missing rates:",
        combined_sold_residential_with_rates["rate_30yr_fixed"].isna().sum()
    )
    print(
        "List residential missing rates:",
        combined_list_residential_with_rates["rate_30yr_fixed"].isna().sum()
    )

    # Step 9: Save outputs
    sold_output_path = output_dir / "combined_sold_with_mortgage_rates.csv"
    list_output_path = output_dir / "combined_list_with_mortgage_rates.csv"

    sold_residential_output_path = output_dir / "combined_sold_residential_with_mortgage_rates.csv"
    list_residential_output_path = output_dir / "combined_list_residential_with_mortgage_rates.csv"


    combined_sold_with_rates.to_csv(sold_output_path, index=False)
    combined_list_with_rates.to_csv(list_output_path, index=False)

    combined_sold_residential_with_rates.to_csv(
        sold_residential_output_path,
        index=False
    )

    combined_list_residential_with_rates.to_csv(
        list_residential_output_path,
        index=False
    )


    print("\nSaved enriched datasets:")
    print(sold_output_path)
    print(list_output_path)

    print("\nSaved residential enriched datasets:")
    print(sold_residential_output_path)
    print(list_residential_output_path)


    return (
        combined_sold_with_rates,
        combined_list_with_rates,
        combined_sold_residential_with_rates,
        combined_list_residential_with_rates
    )


# Run the helper function to fetch the Mortgage rate

(
    combined_sold_with_rates,
    combined_list_with_rates,
    combined_sold_residential_with_rates,
    combined_list_residential_with_rates
) = add_mortgage_rates(
    combined_sold=combined_sold,
    combined_list=combined_list,
    output_dir=DATA_DIR
)

# Check before and after add mortgage rates columns and rows
# Without filter to property_type = esidential

sold_all = pd.read_csv("output/combined_sold.csv")
list_all = pd.read_csv("output/combined_list.csv")
sold_with_rate = pd.read_csv("output/combined_sold_with_mortgage_rates.csv")
list_with_rate = pd.read_csv("output/combined_list_with_mortgage_rates.csv")

print(sold_all.shape)
print(sold_with_rate.shape)
print(list_all.shape)
print(list_with_rate.shape)

# The result is
# (665521, 88)
# (665521, 89)
# (941744, 88)
# (941744, 89)


# Check before and after add mortgage rates columns and rows
# Filter to property_type = residential

sold_resid_all = pd.read_csv("output/combined_sold_residential.csv")
list_resid_all = pd.read_csv("output/combined_list_residential.csv")
sold_resid_with_rate = pd.read_csv("output/combined_sold_residential_with_mortgage_rates.csv")
list_resid_with_rate = pd.read_csv("output/combined_list_residential_with_mortgage_rates.csv")

print(sold_resid_all.shape)
print(sold_resid_with_rate.shape)
print(list_resid_all.shape)
print(list_resid_with_rate.shape)

# The result is
# (448033, 88)
# (448033, 89)
# (615739, 88)
# (615739, 89)