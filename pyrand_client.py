import random

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
        self.numLetters = self.wordLength - self.minNums - self.minSyms
        self.numCapitals = 0
        self.numLowercase = 0
        self.pass_phrase = ""
        self.load_password()

    def set_num_capitals(self):
        if self.capitalBool and self.lowerBool:
            self.numCapitals = random.randint(0, self.numLetters)
        elif self.capitalBool:
            self.numCapitals = self.numLetters

    def get_num_capitals(self):
        return self.numCapitals

    def set_num_lowercase(self):
        if self.capitalBool and self.lowerBool:
            self.numLowercase = self.wordLength - self.get_num_capitals()
        elif self.lowerBool:
            self.numLowercase = self.numLetters

    def get_num_lowercase(self):
        return self.numLowercase

    def set_capitals(self):
        for i in range(0, self.numCapitals):
            self._charList.append(self._CHAR_HASH[random.randint(10, 35)].upper())

    def set_lowercase(self):
        for i in range(0, self.numLowercase):
            self._charList.append(self._CHAR_HASH[random.randint(10, 35)])

    def set_min_syms(self):
        for i in range(0, self.minSyms):
            self._charList.append(self._CHAR_HASH[random.randint(36, 43)])

    def set_min_nums(self):
        for i in range(0, self.minNums):
            self._charList.append(self._CHAR_HASH[random.randint(0, 9)])

# loads the character list with characters based on the given boolean values and number of symbols and numbers
    def load_password(self):
        self._charList.clear()
        self.set_num_capitals()
        self.set_num_lowercase()        
        self.set_capitals()
        self.set_lowercase()
        self.set_min_nums()
        self.set_min_syms()

# converts and returns the contents of the character list into a string
    def parse_password(self):
        random.shuffle(self._charList)
        for i in self._charList:
            self.pass_phrase += i

        return self.pass_phrase
