import duckdb
from pathlib import Path

# Connect to DuckDB database file
db_path = Path("data/olist.duckdb")
db_path.parent.mkdir(parents=True, exist_ok=True)
con = duckdb.connect(db_path.as_posix())

print("Loading Olist CSVs into DuckDB with header=True...")
for f in sorted(Path("data/raw").glob("*.csv")):
    name = f.stem.replace("olist_", "").replace("_dataset", "")
    con.execute(f"CREATE OR REPLACE TABLE {name} AS SELECT * FROM read_csv_auto('{f.as_posix()}', header=True)")
    cols = [c[0] for c in con.execute(f"DESCRIBE {name}").fetchall()]
    n = con.execute(f"SELECT COUNT(*) FROM {name}").fetchone()[0]
    print(f"{name:32} | {n:9,} rows | {cols}")

print("\nAll tables loaded successfully into data/olist.duckdb with exact schema.")
con.close()
