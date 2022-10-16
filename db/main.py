import logging
import os
import psycopg
from psycopg.errors import ProgrammingError
from datetime import date

TOPICS = [
    "War",
    "COVID",
    "Entertainment",
    "Sports"
]


def add_to_db(uid, topic, score, threshold):

    # Is uid in Users
    if is_new_user(uid):
        spin_up_user(uid)

    # Call update_score(uid, topic, score)
    update_score(uid, topic, score)

    # STDOUT
    print("Negativity Score: ", str(score))
    print("{}'s most negative topic is '{}'".format(uid, get_saddest_topic(uid)))
    print("CURRENT STANDING: ", str(get_sum_scores(uid)), "/", str(threshold))
    # Return whether the threshold is crossed
    return get_sum_scores(uid) >= threshold



"""
SPIN UP RESOURCES
"""

def spin_up_resources():
    init_date()
    init_topics()
    init_users()


def spin_up_user(uid):
    add_user_to_users(uid)
    add_user_to_topics(uid)
    add_user_to_date(uid)


"""
NEW USER ADDITIONS
"""

def add_user_to_users(uid):
    # Connect to CockroachDB
    connection = psycopg.connect(os.environ["DATABASE_URL"])

    query = "INSERT INTO Users (uid) VALUES ('{}')".format(uid)

    exec_statement(connection, query)

    exec_statement(connection, "SELECT * FROM Users")
    # Close communication with the database
    connection.close()




def add_user_to_topics(uid):
    # Connect to CockroachDB
    connection = psycopg.connect(os.environ["DATABASE_URL"])

    for topic in TOPICS:
        params = "'{}', '{}', '0'".format(uid, topic)
        insert_string = "INSERT INTO topics (uid, topic, score) VALUES ({})".format(params)
        exec_statement(connection, insert_string)

    exec_statement(connection, "SELECT * FROM Topics")
    # Close communication with the database
    connection.close()


def add_user_to_date(uid):
    # Connect to CockroachDB
    connection = psycopg.connect(os.environ["DATABASE_URL"])

    today_date = str(date.today())
    query = "INSERT INTO Date (uid, date) VALUES ('{}', '{}')".format(uid, today_date)

    exec_statement(connection, query)

    exec_statement(connection, "SELECT * FROM Date")
    # Close communication with the database
    connection.close()




"""
INITS

"""

# SCHEMA: (uid: user id)
def init_users():
    # Connect to CockroachDB
    connection = psycopg.connect(os.environ["DATABASE_URL"])
    today_date = str(date.today())

    init_statements = [
        # Clear out any existing data
        "DROP TABLE IF EXISTS Users",
        # CREATE the users table
        "CREATE TABLE IF NOT EXISTS Users (uid STRING PRIMARY KEY)"
    ]

    for statement in init_statements:
        exec_statement(connection, statement)
    

    exec_statement(connection, "SELECT * FROM Users")
    # Close communication with the database
    connection.close()


# SCHEMA: (pkey, uid, topic, score)
def init_topics():
     # Connect to CockroachDB
    connection = psycopg.connect(os.environ["DATABASE_URL"])

    init_statements = [
        # Clear out any existing data
        "DROP TABLE IF EXISTS topics",
        # CREATE the messages table
        "CREATE TABLE IF NOT EXISTS topics (uid STRING, topic STRING, score FLOAT)",
    ]

    for statement in init_statements:
        exec_statement(connection, statement)

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
        "CREATE TABLE IF NOT EXISTS Date (uid STRING PRIMARY KEY, date STRING)"
    ]

    for statement in init_statements:
        exec_statement(connection, statement)
    

    exec_statement(connection, "SELECT * FROM Date")
    # Close communication with the database
    connection.close()


def check_reinitialize(uid):
    stored_date = get_date(uid)
    curr_date = str(date.today())

    if stored_date != curr_date:
        reset_user_topics(uid)
        reset_user_date(uid)


def reset_user_topics(uid):
    # Connect to CockroachDB
    connection = psycopg.connect(os.environ["DATABASE_URL"])

    for topic in TOPICS:
        update_string = "UPDATE topics SET score = '{}' WHERE topic = '{}' AND user = '{}'".format(str(0), topic, uid)
        exec_statement(connection, update_string)

    exec_statement(connection, "SELECT * FROM Topics")
    # Close communication with the database
    connection.close()


def reset_user_date(uid):
    # Connect to CockroachDB
    connection = psycopg.connect(os.environ["DATABASE_URL"])

    today_date = str(date.today())
    query = "UPDATE Date (date) VALUES ('{}') WHERE user = '{}'".format(today_date, uid)

    exec_statement(connection, query)

    exec_statement(connection, "SELECT * FROM Date")
    # Close communication with the database
    connection.close()




"""
UPDATES
"""

def update_score(uid, topic, score):

    check_reinitialize(uid)

    # Connect to CockroachDB
    connection = psycopg.connect(os.environ["DATABASE_URL"])

    prev_score = get_score(uid, topic)
    update_string = "UPDATE topics SET score = '{}' WHERE topic = '{}' AND uid = '{}'".format(str(score + prev_score), topic, uid)
    exec_statement(connection, update_string)
    exec_statement(connection, "SELECT * FROM topics")
    

    # Close communication with the database
    connection.close()


    
"""
GETS
"""

def get_score(uid, topic):
    # Connect to CockroachDB
    connection = psycopg.connect(os.environ["DATABASE_URL"])

    query = "SELECT score FROM topics WHERE topic = '{}' AND uid = '{}'".format(topic, uid)
    score = exec_statement(connection, query)[0][0]

    connection.close()
    return score


def get_sum_scores(uid):
    # Connect to CockroachDB
    connection = psycopg.connect(os.environ["DATABASE_URL"])

    query = "SELECT SUM(score) FROM topics WHERE uid = '{}'".format(uid)
    score = exec_statement(connection, query)[0][0]

    connection.close()
    return score


def get_saddest_topic(uid):
    connection = psycopg.connect(os.environ["DATABASE_URL"])

    query = "SELECT topic FROM topics WHERE uid = '{}' ORDER BY score DESC LIMIT 1".format(uid)
    
    topic = exec_statement(connection, query)[0][0]

    connection.close()
    return topic


def get_date(uid):
    connection = psycopg.connect(os.environ["DATABASE_URL"])

    query = "SELECT date FROM Date WHERE uid = '{}'".format(uid)
    date = exec_statement(connection, query)[0][0]

    connection.close()
    return date


def is_new_user(uid):
    connection = psycopg.connect(os.environ["DATABASE_URL"])

    query = "SELECT COUNT(*) FROM Users WHERE uid = '{}'".format(uid)
    user_bool = exec_statement(connection, query)[0][0]

    connection.close()

    return 1 - user_bool



"""
EXECUTION OF QUERY
"""

def exec_statement(conn, stmt):
    try:
        with conn.cursor() as cur:
            cur.execute(stmt)
            res = cur.fetchall()
            conn.commit()
            return res
    except ProgrammingError:
        return
