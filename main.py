# Semantics Analyzer Application #

# My project idea is to create an English semantics analyzer application that takes in paragraphs and displays the following analysis:
# * Word counts by adjectives, nouns, verbs, prepositions
# * A cumulative positivity, negativity and neutrality of all the sentences as a percentage
# * Top 5 used nouns and their usage as a percentage of all words in the paragraph\

import spacy
from textblob import TextBlob

nlp = spacy.load("en_core_web_sm")


def analyze_paragraph(paragraph_):
    doc = nlp(paragraph_)

    prepositions, nouns, adjectives, adverbs, determinants, verbs, punctuations, interjections, numerals, particles, others, symbols = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    nouns_density = dict()

    # Iterate through each token in the document
    for token in doc:
        pos = token.pos_  # part-of-speech tag

        if pos in ("ADP", "CCONJ", "SCONJ", "CONJ"):  # Prepositions
            prepositions += 1
        elif pos in ("NOUN", "PRON", "PROPN"):  # Nouns, Pronouns and proper nouns
            nouns += 1
            if pos != "PRON":
                text = token.text.lower()
                if text in nouns_density:
                    nouns_density[text] = nouns_density[text] + 1
                else:
                    nouns_density[text] = 1
        elif pos == "ADJ":  # Adjectives
            adjectives += 1
        elif pos == "ADV":  # Adverbs
            adverbs += 1
        elif pos == "DET":  # Determinants
            determinants += 1
        elif pos in ("VERB", "AUX"):  # verbs and auxiliary verbs
            verbs += 1
        elif pos == "PUNCT":  # punctuations
            punctuations += 1
        elif pos == "INTJ":  # interjections
            interjections += 1
        elif pos == "NUM":  # numerals like 2017, XII, seventy-seven
            numerals += 1
        elif pos == "PART":
            particles += 1
        elif pos == "X":  # Others are words that are identifiable by the language model
            others += 1
        elif pos == "SYM":  # =, +, -, :=, etc...
            symbols += 1

    characters = 0
    for character in 'abcdefghijklmnopqrstuvwxyz':  # English numerals
        characters += paragraph_.count(character) + paragraph_.count(character.upper())

    # Polarity and Subjectivity:
    polarity, subjectivity, sentences_num = 0, 0, 0
    for sent in doc.sents:
        sentences_num += 1
        blob = TextBlob(sent.text)
        polarity += blob.polarity * (len(sent.text) / len(paragraph_))
        subjectivity += blob.subjectivity * (len(sent.text) / len(paragraph_))

    dict_ = {
        "Prepositions": prepositions,
        "Nouns": nouns,
        "Adjectives": adjectives,
        "Adverbs": adverbs,
        "Determinants": determinants,
        "Verbs": verbs,
        "Numerals": numerals,
        "Other Words": others,
        "Word Count": nouns + adjectives + adverbs + verbs + prepositions + interjections + numerals + others + determinants,
        "Alphabetical Characters": characters,
        "Number of Sentences": sentences_num
    }
    sorted_nouns_density = dict(sorted(nouns_density.items(), key=lambda item: item[1], reverse=True))
    analysis_ = [{key: value for key, value in dict_.items() if value != 0}, sorted_nouns_density, [polarity, subjectivity]]

    return analysis_


paragraph = ""

input_type = input("Do you want the text to be taken from the Console or from a File (C/F)? ")

if input_type.upper() == "C":
    while True:
        paragraph = paragraph + input("Keep writing your text, to quit the writing process, type '\\': ")
        if paragraph.endswith('\\'):  # The paragraph has to end with '\'
            paragraph = paragraph[:-1]
            break
elif input_type.upper() == "F":
    # for Example: "C:\Users\HasanAmk\Desktop\Uni\test1.txt"
    path = input("Write the full path of the text file: ")
    f = open(path, "r")
    paragraph = f.read()
    f.close()

analysis = analyze_paragraph(paragraph)

print("\n\n\n..:SEMANTICS ANALYSIS REPORT:..\n\n")

keys = list(analysis[0].keys())
is_new_row = False
for i in range(0, len(keys), 1):
    print(f"\t{keys[i]} : {analysis[0][keys[i]]}", end="\n" if is_new_row else "\t")
    is_new_row = not is_new_row


print("\n\n.:NOUNS DENSITY:.\n\tTop 5 used nouns:")

nouns_ = list(analysis[1].keys())
for i in range(0, 5):
    print(f"\t\t{nouns_[i]} : {analysis[1][nouns_[i]]}")


polarity_percent = analysis[2][0] * 100  # positivity or negativity percent
is_negative = polarity_percent < 0
polarity_percent = abs(polarity_percent)
neutrality_percent = 100.0 - polarity_percent

print("\n\n.:POLARITY & SUBJECTIVITY:.")
if -1 <= analysis[2][0] <= -0.76:
    print("\tThe text is VERY NEGATIVE")
elif -0.75 <= analysis[2][0] <= -0.25:
    print("\tThe text is NEGATIVE")
elif -0.24 <= analysis[2][0] <= 0.24:
    print("\tThe text is NEUTRAL")
elif 0.25 <= analysis[2][0] <= 0.75:
    print("\tThe text is POSITIVE")
else:
    print("\tThe text is VERY POSITIVE")

if neutrality_percent != 0.0:
    print(f"\tNeutrality: {neutrality_percent:.2f} %")

if is_negative:
    print(f"\tNegativity: {polarity_percent:.2f} %")
else:
    print(f"\tPositivity: {polarity_percent:.2f} %")

print("")
if 0.0 <= analysis[2][1] <= 0.25:
    print("\tThe text is VERY OBJECTIVE")
elif 0.26 <= analysis[2][1] <= 0.5:
    print("\tThe text is OBJECTIVE")
elif 0.51 <= analysis[2][1] <= 0.75:
    print("\tThe text is SUBJECTIVE")
else:
    print("\tThe text is VERY SUBJECTIVE")

is_obj = analysis[2][1] <= 0.5  # is objective
subjectivity_percent = abs(analysis[2][1] - 0.5) * 200
if is_obj:
    print(f"\tObjectivity: {subjectivity_percent:.2f} %")
else:
    print(f"\tSubjectivity: {subjectivity_percent:.2f} %")
