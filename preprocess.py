import re
import spacy

nlp = spacy.load('en_core_web_sm')

def replace_synonyms(text, synonyms):
    for word, replacement in synonyms.items():
        text = re.sub(r'\b' + word + r'\b', replacement, text, flags=re.IGNORECASE)
    return text

def preprocess_text(text, synonyms):
    text = text.lower()
    text = replace_synonyms(text, synonyms)
    doc = nlp(text)
    lemmatized_text = ' '.join([token.lemma_ for token in doc])
    return lemmatized_text
