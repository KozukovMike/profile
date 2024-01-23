import datetime

from sqlalchemy import MetaData, String, Integer, TIMESTAMP, Table, Column, JSON, ForeignKey


metadata = MetaData()


roles = Table(
    "roles",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("permissions", JSON)
)

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String, nullable=False),
    Column("username", String, nullable=False),
    Column("password", String, nullable=False),
    Column("role_id", Integer, ForeignKey("roles.id"))
)
