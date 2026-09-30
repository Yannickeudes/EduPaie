import sqlite3

connection = sqlite3.connect("database/edupaie.db")

with open("database/schema.sql", "r", encoding="utf-8") as file:
    schema = file.read()

connection.executescript(schema)

connection.close()