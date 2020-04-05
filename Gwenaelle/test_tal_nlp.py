"""
--> A faire au préalable dans la console -->

    pip install spacy
    python -m spacy download fr_core_news_sm

"""

import spacy

nlp_tool = spacy.load("fr_core_news_sm")

sentence_to_test = "Lorsqu'il a demandé qui avait cassé la fenêtre, " \
                   "tous les garçons ont pris un air innocent."

analysis = nlp_tool(sentence_to_test)

for word_found in analysis:
    word_type = word_found.pos_
    print(word_found, word_type)



