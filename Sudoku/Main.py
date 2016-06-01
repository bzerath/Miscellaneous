# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # Everything is UTF-8
from pprint import pprint

class Case:
    def __init__(self, value):
        self.possible = None

        if value == "" or value == "\n":
            self.value = " "
            self.possible = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        else:
            value = int(value)
            assert 1 <= value <= 9
            self.value = value

    def validate(self):
        assert len(self.possible) == 1
        self.value = self.possible[0]
        self.possible = None

    def __str__(self):
        return str(self.value)


class Grid:
    def __init__(self, file_path):
        self.grid = [0]*9
        lines = None
        with open(file_path, "r") as fichier:
            lines = fichier.readlines()
        for numline in xrange(len(lines)):
            line = lines[numline].split(";")
            self.grid[numline] = []
            for value in line:
                self.grid[numline].append(Case(value))

    def getColumn(self, numCol):
        return [line[numCol] for line in self.grid]

    def getLine(self, numLine):
        return self.grid[numLine]

    def getSquare(self, numCol, numLine):
        square = []
        minCol = int(numCol / 3) * 3
        minLine = int(numLine / 3) * 3
        for line in xrange(minLine, minLine + 3):
            square.extend(self.grid[line][minCol:minCol+3])
        return square

    def resolve(self):
        pass

    def faire_une_passe(self):
        encore_qqch_a_remplir = False
        for numLine in xrange(9):
            for numCol in xrange(9):
                case = self.grid[numLine][numCol]
                if case.value != " ":
                    continue
                else:
                    encore_qqch_a_remplir = True
                    ligne = self.getLine(numLine)
                    colonne = self.getColumn(numCol)
                    square = self.getSquare(numCol, numLine)

                    # Remove possible elements basing on the line
                    for element in [a for a in ligne if a.value != " "]:
                        if element.value in self.grid[numLine][numCol].possible:
                            self.grid[numLine][numCol].possible.remove(element.value)

                    # Remove possible elements basing on the column
                    for element in [a for a in colonne if a.value != " "]:
                        if element.value in self.grid[numLine][numCol].possible:
                            self.grid[numLine][numCol].possible.remove(element.value)

                    # Remove possible elements basing on the square
                    for element in [a for a in square if a.value != " "]:
                        if element.value in self.grid[numLine][numCol].possible:
                            self.grid[numLine][numCol].possible.remove(element.value)

                    if len(self.grid[numLine][numCol].possible) == 1:
                        self.grid[numLine][numCol].validate()
                        continue

                    # If we have not stopped, we can try something else
                    square_possibilities = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}
                    #for element in



        return encore_qqch_a_remplir

    def __str__(self):
        to_return = ""
        for ligne in self.grid:
            for case in ligne:
                to_return += str(case.value) + "\t"
            to_return += "\n"

        return to_return


if __name__ == "__main__":
    grid = Grid("grid4.csv")
    print(grid)
    print "0-------"

    vague = grid.faire_une_passe()
    print(grid)
    print "1-------"
    i = 2
    while (vague and i <= 100):
        vague = grid.faire_une_passe()
        print(grid)
        print "{i}-------".format(i=i)
        i += 1
    print grid.grid[8][7].possible




