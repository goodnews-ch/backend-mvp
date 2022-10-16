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
    if get_sum_scores(uid) >= threshold:
        news = find_goodnews(uid, topic)
        print("The suggested article is '{}'".format(news))
        return (True, news)
    return (False, "")



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
    add_user_to_news(uid)


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

def add_user_to_news(uid):
    # Connect to CockroachDB
    connection = psycopg.connect(os.environ["DATABASE_URL"])

    all_news_query = "SELECT url FROM Goodnews"
    all_urls = exec_statement(connection, all_news_query)

    urls = [item[0] for item in all_urls]
    print(urls)
    print(len(urls))


    for url in urls:
        query = "INSERT INTO userurls (uid, url) VALUES ('{}', '{}')".format(uid, url)
        exec_statement(connection, query)


    print(exec_statement(connection, "SELECT * FROM userurls"))
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
    

    exec_statement(connection, "SELECT * FROM Goodnews")
    # Close communication with the database
    connection.close()


def init_userurls():
    # Connect to CockroachDB
    connection = psycopg.connect(os.environ["DATABASE_URL"])

    init_statements = [
        # Clear out any existing data
        "DROP TABLE IF EXISTS userurls",
        # CREATE the users table
        "CREATE TABLE IF NOT EXISTS userurls (uid STRING, url STRING)"
    ]

    for statement in init_statements:
        exec_statement(connection, statement)
    

    exec_statement(connection, "SELECT * FROM userurls")
    # Close communication with the database
    connection.close()





def insert_news(url, topic):
    # Connect to CockroachDB
    connection = psycopg.connect(os.environ["DATABASE_URL"])

    query = "INSERT INTO Goodnews (url, topic) VALUES ('{}', '{}')".format(url, topic)

    exec_statement(connection, query)

    insert_userURLs(url)

    exec_statement(connection, "SELECT * FROM Goodnews")
    # Close communication with the database
    connection.close()



def insert_userURLs(url):
    # Connect to CockroachDB
    connection = psycopg.connect(os.environ["DATABASE_URL"])

    all_users_query = "SELECT * FROM Users"
    
    users = exec_statement(connection, all_users_query)


    user_lst = [user[0] for user in users]


    for user in user_lst:
        print(exec_statement(connection, "SELECT * FROM userurls"))
        query = "INSERT INTO userurls (uid, url) VALUES ('{}', '{}')".format(user, url)
        exec_statement(connection, query)


    exec_statement(connection, "SELECT * FROM userurls")
    # Close communication with the database
    connection.close()

def find_goodnews(user, topic):
    # Connect to CockroachDB
    connection = psycopg.connect(os.environ["DATABASE_URL"])

    query = "SELECT * FROM Goodnews"
    url = exec_statement(connection, query)
    print(url)

    query = "SELECT * FROM Goodnews AS g NATURAL JOIN userurls AS u WHERE g.topic = '{}' AND u.uid = '{}' LIMIT 1".format(topic, user)
    url = exec_statement(connection, query)[0][0]

    # query = "DELETE FROM userurls WHERE uid = '{}' AND url = '{}';".format(user, url)
    
    # Close communication with the database
    connection.close()

    return url


def load_news():
    insert_news("https://justgivemepositivenews.com/home/vaccines-effective-against-new-omicron-subvariants-who-chief-says/", "COVID")
    insert_news("https://www.bbc.com/news/health-63247997", "COVID")
    insert_news("https://www.unhcr.org/en-us/news/stories/2022/5/6284d6bc4/ukrainian-refugees-find-warm-welcome-neighbouring-moldova.html", "War")
    insert_news("https://www.goodgoodgood.co/articles/ukraine-good-news", "War")
    insert_news("https://www.usatoday.com/story/sports/ncaaf/bigten/2022/10/16/michigan-football-penn-state-blake-corum-donovan-edwards/10517247002/", "Entertainment")
    insert_news("https://goodcelebrity.com/2019/01/28/michael-jordan-make-a-wish-30-years/", "Entertainment")

def reset():
    spin_up_resources()
    init_goodnews()
    init_userurls()
    load_news()

reset()