import logging
import os
import psycopg
from psycopg.errors import ProgrammingError

TOPICS = [
    "WAR",
    "COVID",
    "CLIMATE CHANGE"
]

def exec_statement(conn, stmt):
    try:
        with conn.cursor() as cur:
            cur.execute(stmt)
            res = cur.fetchall()
            conn.commit()
            print(res)
            return res
    except ProgrammingError:
        return

def init():
    print("TEST")
     # Connect to CockroachDB
    connection = psycopg.connect(os.environ["DATABASE_URL"])

    init_statements = [
        # Clear out any existing data
        "DROP TABLE IF EXISTS topics",
        # CREATE the messages table
        "CREATE TABLE IF NOT EXISTS topics (topic STRING PRIMARY KEY, score FLOAT)",
    ]

    for statement in init_statements:
        exec_statement(connection, statement)

    for topic in TOPICS:
        params = "'{}', '0'".format(topic)
        insert_string = "INSERT INTO topics (topic, score) VALUES ({})".format(params)
        exec_statement(connection, insert_string)

    exec_statement(connection, "SELECT * FROM topics")
    # Close communication with the database
    connection.close()

def get_score(topic):
    # Connect to CockroachDB
    connection = psycopg.connect(os.environ["DATABASE_URL"])

    query = "SELECT score FROM topics WHERE topic = '{}'".format(topic)
    score = exec_statement(connection, query)[0][0]

    connection.close()
    return score


def update(topic, score):

    # Connect to CockroachDB
    connection = psycopg.connect(os.environ["DATABASE_URL"])

    prev_score = get_score(topic)
    update_string = "UPDATE topics SET score = '{}' WHERE topic = '{}'".format(str(score + prev_score), topic)
    exec_statement(connection, update_string)
    exec_statement(connection, "SELECT * FROM topics")
    

    # Close communication with the database
    connection.close()
# init()
update("WAR", 15)