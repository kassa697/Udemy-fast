import sqlite3
from typing import Any

from .schemas import ShipmentCreate, ShipmentUpdate


class Database:
    def connect_to_db(self):
        # Make connection with database
        self.conn = sqlite3.connect("sqlite.db", check_same_thread=False)
        # Get cursor to execute queries and fetch data
        self.cur = self.conn.cursor()
        print("connected to sqlite.db ...")

    def create_table(self):
        # Create a table with columns
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS shipment (
                id INTEGER PRIMARY KEY,
                content TEXT,
                weight REAL,
                status TEXT
            )
        """)

    def create(self, shipment: ShipmentCreate) -> int:
        # Insert values in the table
        self.cur.execute(
            """
            INSERT INTO shipment (content, weight, status)
            VALUES (:content, :weight, :status)
        """,
            {
                **shipment.model_dump(),
                "status": "placed",
            },
        )
        # Commit the change to the database
        self.conn.commit()

        return self.cur.lastrowid

    def get(self, id: int) -> dict[str, Any] | None:
        self.cur.execute(
            """
            SELECT * FROM shipment
            WHERE id = ?
        """,
            (id,),
        )
        row = self.cur.fetchone()

        return (
            {
                "id": row[0],
                "content": row[1],
                "weight": row[2],
                "status": row[3],
            }
            if row
            else None
        )

    def update(self, id: int, shipment: ShipmentUpdate) -> dict[str, Any]:
        self.cur.execute(
            """
            UPDATE shipment SET status = :status
            WHERE id = :id
        """,
            {"id": id, **shipment.model_dump()},
        )
        self.conn.commit()

        return self.get(id)

    def delete(self, id: int):
        self.cur.execute(
            """
            DELETE FROM shipment
            WHERE id = ?
        """,
            (id,),
        )
        self.conn.commit()

    def close(self):
        print("...connection closed")
        self.conn.close()
