from classification.classify import *
from classification.categorize_text import *
from db.main import *

THRESHOLD = 20

def response(uid, text):
    negativity_score = calculate_score(text)
    topic = categorize_text(text)
    crossed_threshold = add_to_db(uid, topic, negativity_score, THRESHOLD)
    return crossed_threshold
