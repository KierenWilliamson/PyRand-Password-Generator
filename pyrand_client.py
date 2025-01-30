import random
import pyrand_exceptions as passExcept


class Password:
    # list that will contain the randomized characters pulled from the HashTable
    _charList = list()
    # HashTable containing the allowed characters and their corresponding numeric keys
    _CHAR_HASH = {0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9',
                  10: 'a', 11: 'b', 12: 'c', 13: 'd', 14: 'e', 15: 'f', 16: 'g', 17: 'h', 18: 'i', 19: 'j',
                  20: 'k', 21: 'l', 22: 'm', 23: 'n', 24: 'o', 25: 'p', 26: 'q', 27: 'r', 28: 's', 29: 't',
                  30: 'u', 31: 'v', 32: 'w', 33: 'x', 34: 'y', 35: 'z',
                  36: '!', 37: '@', 38: '#', 39: '$', 40: '%', 41: '^', 42: '&', 43: '*'}

    def __init__(self, word_length, min_nums, min_syms, capital_bool=False, lower_bool=False):
        self.wordLength = word_length
        self.minNums = min_nums
        self.minSyms = min_syms
        self.capitalBool = capital_bool
        self.lowerBool = lower_bool
        self.pointer = word_length - 1
        self.numCapitals = 0
        self.numLowers = 0
        self.pass_phrase = ""

        self.load_password()

    def get_capitals(self):
        for i in range(0, self.numCapitals):
            self._charList.append(self._CHAR_HASH[random.randint(10, 35)].upper())

    def get_lowers(self):
        for i in range(0, self.numLowers):
            self._charList.append(self._CHAR_HASH[random.randint(10, 35)])

# loads the character list with characters based on the given boolean values and number of symbols and numbers
    def load_password(self):
        self._charList.clear()
        rand_num = random.randint(0, (self.wordLength - self.minNums - self.minSyms))

        if self.capitalBool and self.lowerBool:
            self.numCapitals = rand_num
            self.numLowers = self.wordLength - self.numCapitals
            self.get_capitals()
            self.get_lowers()
        elif self.capitalBool:
            self.numCapitals = self.wordLength - self.minNums - self.minSyms
            self.get_capitals()
        elif self.lowerBool:
            self.numLowers = self.wordLength - self.minNums - self.minSyms
            self.get_lowers()

        for i in range(0, self.minNums):
            self._charList.append(self._CHAR_HASH[random.randint(0, 9)])

        for i in range(0, self.minSyms):
            self._charList.append(self._CHAR_HASH[random.randint(36, 43)])

# randomizes the character list using a Fisher-Yates shuffle algorithm
    def randomize(self):
        # if the requested length is longer then the available characters, the custom exception is raised
        try:
            if (self.pointer == 0) or (len(self._charList) == 0):
                return
            else:
                rand_swap = random.randint(0, self.pointer)
                tmp_elem = self._charList[rand_swap]
                self._charList[rand_swap] = self._charList[self.pointer]
                self._charList[self.pointer] = tmp_elem
                self.pointer -= 1
                return self.randomize()
        except IndexError:
            raise passExcept.LengthError

# converts and returns the contents of the character list into a string
    def parse_password(self):
        for i in self._charList:
            self.pass_phrase += i

        return self.pass_phrase
