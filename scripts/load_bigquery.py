"""Load sample CSV into BigQuery (requires GCP_PROJECT + ADC)."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from google.cloud import bigquery

from bq_config import CSV_PATH, DATASET_ID, TABLE_ID, gcp_project
from validate_csv import validate_csv


def main() -> None:
    project = gcp_project()
    if not project:
        raise SystemExit("Set GCP_PROJECT or GOOGLE_CLOUD_PROJECT")

    validate_csv()
    client = bigquery.Client(project=project)
    dataset_ref = bigquery.Dataset(f"{project}.{DATASET_ID}")
    dataset_ref.location = "US"
    client.create_dataset(dataset_ref, exists_ok=True)

    table_ref = f"{project}.{DATASET_ID}.{TABLE_ID}"
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        autodetect=True,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
    )
    with CSV_PATH.open("rb") as f:
        job = client.load_table_from_file(f, table_ref, job_config=job_config)
    job.result()
    table = client.get_table(table_ref)
    print(f"Loaded {table.num_rows} rows into {table_ref}")


if __name__ == "__main__":
    main()
