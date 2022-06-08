class Utils:
    def findMatch(content, *inputMatrix):
        i = 0
        for value in inputMatrix:
            if (value == content):
                return i
            i += 1

        return -1