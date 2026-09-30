"""Run parameterized filters and grouped counts against the mock table."""

import logging
import os
import re
from typing import Any

import mysql.connector

LOGGER = logging.getLogger(__name__)
ALLOWED_COLUMNS = {"id", "group", "full_name", "email", "age", "signup_date"}
SAFE_IDENTIFIER = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


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


def _validated_column(column: str) -> str:
    """Return an allowed SQL column name or reject unsafe input."""
    if column not in ALLOWED_COLUMNS or not SAFE_IDENTIFIER.fullmatch(column):
        raise ValueError(f"Unsupported group-by column: {column!r}")
    return column


def get_data_by_group(value: str) -> list[dict[str, Any]]:
    """Return all mock rows whose ``group`` column equals *value*."""
    query = """
        SELECT id, `group`, full_name, email, age, signup_date
        FROM mock
        WHERE `group` = %s
        ORDER BY id
    """
    connection = None
    cursor = None
    try:
        LOGGER.info("Querying rows in group %r", value)
        connection = mysql.connector.connect(**_connection_config())
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, (value,))
        rows = cursor.fetchall()
        LOGGER.info("Retrieved %d matching rows", len(rows))
        return rows
    except mysql.connector.Error:
        LOGGER.exception("Group filter query failed")
        raise
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def plot_counts(groupby: str) -> list[tuple[Any, int]]:
    """Return row counts grouped by a validated mock-table column."""
    column = _validated_column(groupby)
    # MySQL cannot parameterize identifiers. The strict allowlist above makes
    # quoting this user-selected column safe.
    query = (
        f"SELECT `{column}`, COUNT(*) AS row_count "
        f"FROM mock GROUP BY `{column}` ORDER BY row_count DESC, `{column}`"
    )

    connection = None
    cursor = None
    try:
        LOGGER.info("Counting rows grouped by %s", column)
        connection = mysql.connector.connect(**_connection_config())
        cursor = connection.cursor()
        cursor.execute(query)
        counts = cursor.fetchall()
        LOGGER.info("Retrieved %d grouped counts", len(counts))
        return counts
    except mysql.connector.Error:
        LOGGER.exception("Grouped count query failed")
        raise
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def main() -> None:
    """Demonstrate the group filter and grouped-count functions."""
    selected_group = os.getenv("MOCK_GROUP", "Engineering")

    print(f"Rows in group {selected_group!r}:")
    for row in get_data_by_group(selected_group):
        print(row)

    print("\nCounts by group:")
    for group_name, count in plot_counts("group"):
        print(f"{group_name}: {count}")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    main()
