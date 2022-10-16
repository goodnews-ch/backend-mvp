import cohere 
from cohere.classify import Example 
co = cohere.Client('3Gadb4V5oKd2YIwc6rz7Oxw6LOYFTxFSbg0nxy7k')

def categorize_text(text_input):
    response = co.classify(
        model='99b88c18-5e7c-49f6-ab8c-cc57cdebb7a3-ft',
        inputs=[text_input]
    )
    print("The text's classification was '{}'".format(response.classifications[0].prediction))
    return response.classifications[0].prediction


