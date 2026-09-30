"""Read, clean, and upload the lab's mock CSV data to MySQL."""

import logging
import os
from pathlib import Path

import mysql.connector
import pandas as pd

LOGGER = logging.getLogger(__name__)
EXPECTED_COLUMNS = ["id", "group", "full_name", "email", "age", "signup_date"]


def read_data(filename: str | Path) -> pd.DataFrame:
    """Read a CSV file from *filename* and return its rows as a DataFrame."""
    path = Path(filename)
    LOGGER.info("Reading data from %s", path)
    data = pd.read_csv(path)
    LOGGER.info("Read %d rows", len(data))
    return data


def clean_data(data: pd.DataFrame) -> pd.DataFrame:
    """Remove incomplete rows, normalize text, and cast columns for upload."""
    missing_columns = sorted(set(EXPECTED_COLUMNS) - set(data.columns))
    if missing_columns:
        raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")

    LOGGER.info("Cleaning %d rows", len(data))
    cleaned = data.loc[:, EXPECTED_COLUMNS].dropna().copy()

    # Normalize text fields after missing values have been removed.
    for column in ("group", "full_name", "email"):
        cleaned[column] = cleaned[column].astype("string").str.strip()

    # Empty strings are also missing data, so remove those rows.
    cleaned = cleaned[(cleaned[["group", "full_name", "email"]] != "").all(axis=1)]
    cleaned["id"] = pd.to_numeric(cleaned["id"], errors="raise").astype("int64")
    cleaned["age"] = pd.to_numeric(cleaned["age"], errors="raise").astype("int64")
    cleaned["signup_date"] = pd.to_datetime(cleaned["signup_date"], errors="raise")

    if cleaned["id"].duplicated().any():
        raise ValueError("The id column contains duplicate values")

    cleaned.reset_index(drop=True, inplace=True)
    LOGGER.info("Cleaning complete: %d rows remain", len(cleaned))
    return cleaned


def _connection_config() -> dict[str, str | int]:
    """Build a MySQL connection configuration from environment variables."""
    required = ("DBHOST", "DBNAME", "DBUSER", "DBPASS")
    missing = [name for name in required if not os.getenv(name)]
    if missing:
        raise RuntimeError(
            "Missing database environment variables: " + ", ".join(missing)
        )

    return {
        "host": os.environ["DBHOST"],
        "port": int(os.getenv("DBPORT", "3306")),
        "database": os.environ["DBNAME"],
        "user": os.environ["DBUSER"],
        "password": os.environ["DBPASS"],
    }


def load_data(data: pd.DataFrame, table: str) -> None:
    """Create the ``mock`` table and safely upsert all rows from *data*."""
    # This lab always writes to one known table. Rejecting other names prevents
    # untrusted SQL identifiers from being interpolated into a query.
    if table != "mock":
        raise ValueError("This loader only accepts the table name 'mock'")

    create_query = """
        CREATE TABLE IF NOT EXISTS mock (
            id BIGINT PRIMARY KEY,
            `group` VARCHAR(50) NOT NULL,
            full_name VARCHAR(100) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age INT NOT NULL,
            signup_date DATE NOT NULL
        )
    """
    insert_query = """
        INSERT INTO mock (id, `group`, full_name, email, age, signup_date)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            `group` = VALUES(`group`),
            full_name = VALUES(full_name),
            email = VALUES(email),
            age = VALUES(age),
            signup_date = VALUES(signup_date)
    """

    connection = None
    cursor = None
    try:
        LOGGER.info("Connecting to MySQL")
        connection = mysql.connector.connect(**_connection_config())
        cursor = connection.cursor()
        cursor.execute(create_query)

        # Convert pandas timestamps to ordinary date values for the connector.
        upload_data = data.copy()
        upload_data["signup_date"] = upload_data["signup_date"].dt.date
        rows = list(upload_data[EXPECTED_COLUMNS].itertuples(index=False, name=None))
        for row in rows:
            cursor.execute(insert_query, row)
        connection.commit()
        LOGGER.info("Uploaded %d rows to mock", len(rows))
    except mysql.connector.Error:
        if connection is not None:
            connection.rollback()
        LOGGER.exception("MySQL upload failed")
        raise
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def main() -> None:
    """Run the read-clean-load pipeline for ``MOCK_DATA.csv``."""
    project_root = Path(__file__).resolve().parents[2]
    data = read_data(project_root / "MOCK_DATA.csv")
    cleaned = clean_data(data)
    load_data(cleaned, "mock")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    main()
