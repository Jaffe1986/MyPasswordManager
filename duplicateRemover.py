class DuplicateRemover:

    def __init__(self, string):
        # create list to contain result
        self.result = []
        # create set() to track unique characters
        self.seen = set()
        self.string = string
        # check if char has already appeared
        for char in self.string:
            # if first appearance append to result
            if char not in self.seen:
                self.result.append(char)
                self.seen.add(char)
