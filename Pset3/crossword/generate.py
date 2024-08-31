import sys

from crossword import *
from collections import deque

class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for d in self.domains.keys():
            rm_w = []
            for w in self.domains[d]:
                if len(w) != d.length:
                    rm_w.append(w)
            for w in rm_w:
                self.domains[d].remove(w)
    

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revised = False
        ovr = self.crossword.overlaps[x, y]

        if ovr is None:
            return False
        
        x_ovr, y_ovr = ovr

        for w_x in set(self.domains[x]):
            satisfied = any(
                w_x[x_ovr] == w_y[y_ovr]
                for w_y in self.domains[y]
            )
            if not satisfied:
                self.domains[x].remove(w_x)
                revised = True

        return revised
    
    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """

        # Enforces arc consistency on the CSP
        if arcs is None:
            q = deque((x, y) for x in self.domains.keys() for y in self.crossword.neighbors(x))
        else:
            q = deque(arcs)

        while q:
            x, y = q.popleft()
            if self.revise(x, y):
                if len(self.domains[x]) == 0:
                    return False
                for z in self.crossword.neighbors(x):
                    if z != y:
                        q.append((z, x))
        return True
        
        # if arcs is None:
        #     q = []
        #     for x in self.domains.keys():
        #         for y in self.domains.keys():
        #             if x != y:
        #                 q.append((x, y)) 

        # else:
        #     q = []
        #     for a in arcs:
        #         q.append(a)

        # while q:
        #     arc = self.dequeue(q)
        #     if (arc is not None):
        #         x = arc[0]
        #         y = arc[1]
        #         if self.revise(x, y):
        #             if (len(self.domains[x]) == 0):
        #                 return False
        #             for z in self.crossword.neighbors(x):
        #                 if z != y:
        #                     q.append((z, x))
        #     else:
        #         break
        # return True
    
    # Extracts an arc from the queue 'q'
    def dequeue(self, q):
        for x, y in q:
            q.remove((x, y))
            return (x, y)
    
    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        for d in self.domains.keys():
            if d not in assignment.keys():
                return False
            else:
                if assignment[d] is None:
                    return False
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """

        # Check for duplicate words 
        vals = []
        for k, v in assignment.items():
            if (v in vals):
                return False
            else:
                vals.append(v)

            if (k.length != len(v)):
                return False
            
            # Check for overlaps with neighbors
            n_cells = self.crossword.neighbors(k)
            for n in n_cells:
                ovr = self.crossword.overlaps[k, n]
                if n in assignment:
                    if assignment[n][ovr[1]] != v[ovr[0]]:
                        return False
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        def count_ruled_out(word, var, assignment):
            """
            Count how many values in the neighbors' domains are ruled out
            by assigning the word to the variable.
            """
            count = 0
            for neighbor in self.crossword.neighbors(var):
                if neighbor in assignment:
                    continue
                overlap = self.crossword.overlaps[var, neighbor]
                if overlap is None:
                    continue
                i, j = overlap
                for neighbor_word in self.domains[neighbor]:
                    if word[i] != neighbor_word[j]:
                        count += 1
            return count

        # Sort the domain values by the number of ruled out values
        return sorted(self.domains[var], key=lambda word: count_ruled_out(word, var, assignment))
    
    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        deg. If there is a tie, any of the tied variables are acceptable
        return values.
        """

        # Keep track of number of neighbors 
        deg = 0
        # Store the minimum number of remaining values
        val = 10000
        
        # Iterate oevr all variables 
        for i in self.domains.keys():
            # Skip already assigned variables
            if i in assignment:
                continue
            else:
                # Check for minimum remaining values
                if val > len(self.domains[i]):
                    val = len(self.domains[i])
                    var = i
                    if self.crossword.neighbors(i) is None:
                        deg = 0
                    else:
                        deg = len(self.crossword.neighbors(i))
                # Handle tie-breaking with degree heuristic
                elif val == len(self.domains[i]):
                    if self.crossword.neighbors(i) is not None:
                        if deg < len(self.crossword.neighbors(i)):
                            val = len(self.domains[i])
                            var = i
                            deg = len(self.crossword.neighbors(i))
                        else:
                            var = i
                            val = len(self.domains[i])
                            deg = 0    
        return var        

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """

        if self.assignment_complete(assignment):
            return assignment
        
        # An unassigned variable
        var = self.select_unassigned_variable(assignment)

        # Iterate over possible values for the variable
        for value in self.order_domain_values(var, assignment):
            assignment[var] = value
            if self.consistent(assignment):
                # Recursive backtracking 
                result = self.backtrack(assignment)
                if result is not None:
                    return result   
            assignment.pop(var)
        return None            

def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
