from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    
    # A is either a Knave or a Knight, not both
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),

    # If A is a Knight, the sentence is true
    Implication(AKnight, And(AKnight, AKnave)),

    # If A is a kvave, the sentence is false
    Implication(AKnave, Not(And(AKnight, AKnave))),
   
)


# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(

    # A is either a Knave or a Knight, not both
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))),
    Implication(AKnight, And(AKnave, BKnave)),
    Implication(AKnave, Not(And(AKnave, BKnave)))    
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    
    # A is either a Knave or a Knight, not both
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))),

    # If A is a Knight then, A and B are both the same kind
    Implication(AKnight, Or(And(AKnight, BKnight), And(AKnave, BKnave))),

    # If A is a Knave, his sentence is false
    Implication(AKnave, Not(Or(And(AKnight, BKnight), And(AKnave, BKnave)))),

    # If B is a Knight, A and B are not the same
    Implication(BKnight, Or(And(AKnight, BKnave), And(AKnave, BKnight))),

    # If B is a Knave, his sentence is false
    Implication(BKnave, Not(Or(And(AKnight, BKnave), And(AKnave, BKnight)))),

)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    
    # A is either a Knave or a Knight, not both.
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))),
    And(Or(CKnight, CKnave), Not(And(CKnight, CKnave))),

    # If B is a Knight, A said 'I'm a Knave', and C is a Knave
    Implication(BKnight, CKnave),
    Implication(BKnight, And(
        # A then said 'I'm a Knave', A might be a Knave or a Knight
        Implication(AKnight, AKnave),
        Implication(AKnave, Not(AKnave)),
    )),
    
    # If B is a Knave, A said 'I'm a Knight' C is not a Knave
    Implication(BKnave, Not(CKnave)),
    Implication(BKnave, And(
        # A then said 'I'm a Knight', A might a Knave or a Knight
        Implication(AKnight, AKnight),
        Implication(AKnave, Not(AKnight))

    )),
    
    # If C is a Knight, then A is a Knight
    Implication(CKnight, AKnight),
    #If C is a Knave, then A is not a Knight
    Implication(CKnave, Not(AKnight))  

)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
