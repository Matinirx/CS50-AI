import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

# NONTERMINALS = """
# S -> NP VP | S Conj S
# NP -> Det N | Det Adj N | N | Det Adj N PP
# VP -> V | V NP | V NP PP | VP Conj VP
# PP -> P NP
# """

# NONTERMINALS = """
# S -> NP VP | VP | S Conj S | S P S
# NP -> N | Det N | Det NP | P NP | Adj NP | Adv NP | Conj NP | N NP | N Adv
# VP -> V | V NP | Adv VP | V Adv
# """

NONTERMINALS = """
S -> NP VP | NP VP Conj NP VP | NP VP P NP VP
VP -> V | V NP | V PP | Adv VP | VP Adv | VP  Conj VP
NP -> N | Det NP | AP NP | N PP | Conj NP | NP Adv
AP -> Adj | Adj AP | Adv AP
PP -> P NP
"""
grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """

    # Tokenize the sentence to into words
    words = nltk.word_tokenize(sentence.lower())

    # Filter out words that don't contain alphabetic character
    words = [w for w in words if any(char.isalpha() for char in w)]

    return words

def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """

    # List to hold the noun phrase chunks
    np_chunk = []

    # Check if a subtree is a valid noun phrase chunk
    def noun_phrase_chunk(st):
        # Check if there are any NP subtrees within this subtree
        return len([s for s in st.subtrees(lambda t: t.label() == "NP")]) == 1

    # Iterate through all subtrees labeled "NP"
    for st in tree.subtrees(lambda t: t.label() == "NP"):
        if  noun_phrase_chunk(st):
            np_chunk.append(st)

    return np_chunk

if __name__ == "__main__":
    main()
