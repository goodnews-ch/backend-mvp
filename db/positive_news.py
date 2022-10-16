import logging
import os
import psycopg
from psycopg.errors import ProgrammingError
from datetime import date

from main import *

TOPICS = [
    "War",
    "COVID",
    "Entertainment",
    "Sports"
]

def init_goodnews():
    # Connect to CockroachDB
    connection = psycopg.connect(os.environ["DATABASE_URL"])

    init_statements = [
        # Clear out any existing data
        "DROP TABLE IF EXISTS Goodnews",
        # CREATE the users table
        "CREATE TABLE IF NOT EXISTS Goodnews (url STRING PRIMARY KEY, topic STRING)"
    ]

    for statement in init_statements:
        exec_statement(connection, statement)
    

    exec_statement(connection, "SELECT * FROM Users")
    # Close communication with the database
    connection.close()

def init_newspairs():
    # Connect to CockroachDB
    connection = psycopg.connect(os.environ["DATABASE_URL"])

    init_statements = [
        # Clear out any existing data
        "DROP TABLE IF EXISTS Newspairs",
        # CREATE the users table
        "CREATE TABLE IF NOT EXISTS Newspairs (url STRING PRIMARY KEY, topic STRING)"
    ]

    for statement in init_statements:
        exec_statement(connection, statement)
    

    exec_statement(connection, "SELECT * FROM Users")
    # Close communication with the database
    connection.close()


def init_userurls():
    # Connect to CockroachDB
    connection = psycopg.connect(os.environ["DATABASE_URL"])

    init_statements = [
        # Clear out any existing data
        "DROP TABLE IF EXISTS UserURLs",
        # CREATE the users table
        "CREATE TABLE IF NOT EXISTS UserURLs (user STRING, url STRING)"
    ]

    for statement in init_statements:
        exec_statement(connection, statement)
    

    exec_statement(connection, "SELECT * FROM UserURLs")
    # Close communication with the database
    connection.close()





def insert_news(url, topic):
    # Connect to CockroachDB
    connection = psycopg.connect(os.environ["DATABASE_URL"])

    today_date = str(date.today())
    query = "INSERT INTO Goodnews (uid, topic) VALUES ('{}', '{}')".format(url, topic)

    exec_statement(connection, query)

    insert_userURLs(url)

    exec_statement(connection, "SELECT * FROM Goodnews")
    # Close communication with the database
    connection.close()



def insert_userURLs(url):
    # Connect to CockroachDB
    connection = psycopg.connect(os.environ["DATABASE_URL"])

    all_users_query = "SELECT * FROM Goodnews WHERE url = '{}'".format(url)
    users = exec_statement(connection, all_users_query)[0]
    user_lst = [user[0] for user in users]


    for user in user_lst:
        query = "INSERT INTO userURLs (uid, url) VALUES ('{}', '{}')".format(user, url)
        exec_statement(connection, query)


    exec_statement(connection, "SELECT * FROM UserURLs")
    # Close communication with the database
    connection.close()

def find_goodnews(user, topic):
    # Connect to CockroachDB
    connection = psycopg.connect(os.environ["DATABASE_URL"])

    query = ""
    
    # Close communication with the database
    connection.close()