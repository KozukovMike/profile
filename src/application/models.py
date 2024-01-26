import datetime

from sqlalchemy import MetaData, String, Integer, TIMESTAMP, Table, Column, JSON, ForeignKey, Boolean


metadata = MetaData()


application = Table(
    "application",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("linkedin", String, nullable=False),
    Column("email", String,  nullable=False),
)
