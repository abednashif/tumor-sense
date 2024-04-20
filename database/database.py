import sqlalchemy as sa
from sqlalchemy.sql import text

connection_uri = sa.engine.url.URL(
    "mssql+pyodbc",
    username="sa",
    password="pass_1234",
    host="127.0.0.1",
    database="TumorSense",
    port=1433,
    query={
        "driver": "ODBC Driver 17 for SQL Server",
        "ApplicationIntent": "ReadOnly",
    },
)


engine = sa.create_engine(connection_uri)


def execute_query(query, **params):
    """
    Execute any SQL query safely with parameterized inputs.

    Args:
        query (str): The SQL query to execute.
        **params: Optional keyword arguments for parameter values.

    Returns:
        list: A list containing the fetched data.
    """
    with engine.connect() as con:
        sql = text(query)
        res = con.execute(sql, **params)
        return [row for row in res]


def get_all_data(table_name):
    """
    Retrieve all rows from a specified table.

    Args:
        table_name (str): The name of the table.

    Returns:
        list: A list containing the fetched data.
    """
    query = f"SELECT * FROM {table_name}"
    return execute_query(query)

