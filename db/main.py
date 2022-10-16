import logging
import os
import psycopg
from psycopg.errors import ProgrammingError
from datetime import date
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







"""

INITS


"""







def init_topics():
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

def init_date():
     # Connect to CockroachDB
    connection = psycopg.connect(os.environ["DATABASE_URL"])
    today_date = str(date.today())

    init_statements = [
        # Clear out any existing data
        "DROP TABLE IF EXISTS Date",
        # CREATE the messages table
        "CREATE TABLE IF NOT EXISTS Date (date STRING PRIMARY KEY)",
        # Insert the date of today
        "INSERT INTO Date (date) VALUES ('{}')".format(today_date)

    ]

    for statement in init_statements:
        exec_statement(connection, statement)
    

    exec_statement(connection, "SELECT * FROM Date")
    # Close communication with the database
    connection.close()



def check_reinitialize():
    stored_date = get_date()
    curr_date = str(date.today())

    if stored_date != curr_date:
        print("DIFF")
        init_topics()
        init_date()



"""



UPDATES



"""







def update_score(topic, score):

    check_reinitialize()

    # Connect to CockroachDB
    connection = psycopg.connect(os.environ["DATABASE_URL"])

    prev_score = get_score(topic)
    update_string = "UPDATE topics SET score = '{}' WHERE topic = '{}'".format(str(score + prev_score), topic)
    exec_statement(connection, update_string)
    exec_statement(connection, "SELECT * FROM topics")
    

    # Close communication with the database
    connection.close()


    







"""



GETS





"""





def get_score(topic):
    # Connect to CockroachDB
    connection = psycopg.connect(os.environ["DATABASE_URL"])

    query = "SELECT score FROM topics WHERE topic = '{}'".format(topic)
    score = exec_statement(connection, query)[0][0]

    connection.close()
    return score


def get_sum_scores():
    # Connect to CockroachDB
    connection = psycopg.connect(os.environ["DATABASE_URL"])

    query = "SELECT SUM(score) FROM topics"
    score = exec_statement(connection, query)[0][0]

    connection.close()
    return score


def get_saddest_topic():
    connection = psycopg.connect(os.environ["DATABASE_URL"])

    query = "SELECT topic FROM topics ORDER BY score DESC LIMIT 1"
    topic = exec_statement(connection, query)[0][0]

    connection.close()
    return topic




def get_date():
    connection = psycopg.connect(os.environ["DATABASE_URL"])

    query = "SELECT date FROM Date"
    date = exec_statement(connection, query)[0][0]

    connection.close()
    return date

