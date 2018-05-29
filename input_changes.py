import os
import sys
import time


class Leaf:
    """Class for creating a tree from the given vocabulary with letters as leafs"""
    def __init__(self):
        self.word = None
        self.children = {}

    def insert(self, word):
        """Inserts given word in the tree by creating additional leafs for each letter"""
        node = self
        for letter in word:
            if letter not in node.children:
                node.children[letter] = Leaf()

            node = node.children[letter]

        node.word = word


class DistanceSearch:
    """Class with methods for searching a word in a tree"""
    def __init__(self):
        self.is_found = False

    def search(self, word, distance, root):
        """For each letter in the tree recursively traverses the tree until a word within the given distance is found"""

        current_row = range(len(word)+1)

        for letter in root.children:
            if not self.is_found:
                self.search_leaf(root.children[letter], letter, word, current_row, distance)

        return self.is_found

    def search_leaf(self, leaf, letter, word, previous_row, distance):
        """Recursively searches the tree within given distance
           Distance calculations take place in the last two rows of the distance matrix
           After the last row is computed it is used """
        columns = len(word) + 1
        current_row = [previous_row[0] + 1]

        for column in range(1, columns):
            insert = current_row[column-1] + 1
            delete = previous_row[column] + 1

            if word[column-1] != letter:
                replace = previous_row[column-1] + 1
            else:
                replace = previous_row[column-1]

            current_row.append(min(insert, delete, replace))

        # return if a word within given distance is found
        if current_row[-1] == distance and leaf.word is not None:
            self.is_found = True
            return

        # if minimum row value is less than the current search distance continue recursively searching
        if min(current_row) <= distance:
            for letter in leaf.children:
                if not self.is_found:
                    self.search_leaf(leaf.children[letter], letter, word, current_row, distance)


def main():
    # start = time.time()

    if len(sys.argv) > 1:
        test_file = sys.argv[1]
    else:
        test_file = "187"

    vocabulary_file = "vocabulary.txt"

    if not os.path.exists(test_file):
        print("Input file %s doesn't exist" % test_file)
        sys.exit(1)

    if not os.path.exists(vocabulary_file):
        print("Vocabulary file %s doesn't exist" % vocabulary_file)
        sys.exit(1)

    try:
        with open(test_file) as input_file:
            words = input_file.read().rstrip().upper().split()
    except IOError as error:
        print("Error opening input file: ", str(error))
        sys.exit(1)

    try:
        with open("vocabulary.txt") as vocabulary:
            test_words = vocabulary.read().rstrip().split("\n")
    except IOError as error:
        print("Error opening vocabulary file: ", str(error))
        sys.exit(1)

    root = Leaf()
    pathfinder = DistanceSearch()

    # Fills the tree with words from vocabulary
    for word in test_words:
        root.insert(word)

    # counter for all changes in the input
    total = 0

    # Traverses the tree and increases distance if no words were found
    for word in words:
        if word in test_words:
            continue
        else:
            distance = 1
            pathfinder.is_found = False
            while not pathfinder.search(word, distance, root):
                # increase distance and attempt the search again until a word within distance is found
                distance += 1

            total += distance

    # end = time.time()

    print(total, "\n")

    # runtime = end - start
    # print("Runtime: ", runtime)


if __name__ == "__main__":
    main()
