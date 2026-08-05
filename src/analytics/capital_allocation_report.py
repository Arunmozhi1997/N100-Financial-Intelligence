import sqlite3
import pandas as pd

DB_PATH = "db/nifty100.db"

conn = sqlite3.connect(DB_PATH)

df = pd.read_excel("output/cashflow_intelligence.xlsx")

conn.close()

print(df.head())
print()
print("Rows :", len(df))

# ------------------------------------------
# Latest Year Distribution
# ------------------------------------------

latest_year = df["year"].max()

latest_df = df[df["year"] == latest_year]

distribution = (
    latest_df["capital_allocation_label"]
    .value_counts()
    .reset_index()
)

distribution.columns = [
    "capital_allocation_pattern",
    "company_count",
]

print("\nLatest Year :", latest_year)
print()
print(distribution)



distribution.to_csv(
    "output/capital_allocation_distribution.csv",
    index=False,
)

print()
print("Saved -> output/capital_allocation_distribution.csv")

# ------------------------------------------
# Pattern Changes
# ------------------------------------------

df = df.sort_values(
    ["company_id", "year"]
)

changes = []

for company, group in df.groupby("company_id"):

    group = group.sort_values("year")

    previous_pattern = None

    for _, row in group.iterrows():

        current_pattern = row["capital_allocation_label"]

        if (
            previous_pattern is not None
            and previous_pattern != current_pattern
        ):

            changes.append(
                {
                    "company_id": company,
                    "year": row["year"],
                    "previous_pattern": previous_pattern,
                    "current_pattern": current_pattern,
                }
            )

        previous_pattern = current_pattern

changes_df = pd.DataFrame(changes)

changes_df.to_csv(
    "output/pattern_changes.csv",
    index=False,
)

print()
print("Pattern Changes :", len(changes_df))
print()
print(changes_df.head(10))
print()
print("Saved -> output/pattern_changes.csv")