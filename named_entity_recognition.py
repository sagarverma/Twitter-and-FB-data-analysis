import nltk, re, pprint

def extract_entities(text):
    for sent in nltk.sent_tokenize(text):
        for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
            if hasattr(chunk, 'node'):
                print chunk.node, ' '.join(c[0] for c in chunk.leaves())

extract_entities("Six quintessentials without which India cannot become a super power - The Economic Times on Mobile https://t.co/KcoeqvzE1s")
