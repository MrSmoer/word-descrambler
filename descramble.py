import re
import string
from unittest import skip


def read_wordlist(lettercount):
    "opens a wordlist with the number of words"
    with open("wordlists/"+str(lettercount)+".txt",
              "r", encoding='ascii') as f:
        b = f.read()
        return re.split(r'[\n,|]', b)


wordlistnumbers = [1, 2, 5]
WORDLISTS = {}
for i in wordlistnumbers:
    WORDLISTS[i] = read_wordlist(i)
""" email me i smell
   ex3
   mx3
   ax1
   ix2
   lx3
   sx1
"""


LETTERS = {
    "Diving Weight": ["weight", "d", "b", "t", "lead"],             # l 
    "Mug": ["mug", "cup"],                                          # m 2
    "Hammer Head": ["hammer", "a", "iron"],                         # i 4
    "Reverse Mousetrap": ["trap", "mousetrap", "reverse",  "lure"],  # m 6
    "Lamp": ["lamp"],                                               # l 5
    "Apple": ["apple"],                                             # a 3
    "Egg": ["egg"],                                                 # e 1
    "Egg2": ["egg"],                                                # e 7
    "Saw": ["saw", "tennon saw", "h"],                              # s
    "Lawnmower": ["lawnmower", "mower", "engine", "spinny-thingy"],  # l
    "Mallet": ["mallet", "hammerhead"],                             # m 
    "Icecream": ["icecream", "v-the brand of icecream?"],           # i 8
    # "Cage": ["cage", "aviary", "birdcage"],
    "Money": ["money"],                                             # m 
}

predefined_pattern = ["e", "m", "a", "i", "l", " ", "m", "e", " ", "i", " ",
                      "_", "_", "_", "_", "_"]


def clean_one_predefined(pat: list[str] | (list[tuple[str, int] | str]),
                         duck_letters: dict[str, list[str]],
                         pos=0):
    """ generates all possibilites for the letters to fulfill the given
    pattern, and appends them to the global precleaned_patterns
    this function is recursive
    a letter is dirty if it is predefined, but not predefined as
    a tuple -> just a string
    """
    if pos >= len(pat):
        return [pat]
    res = []
    if pat[pos][0] == ' ' or pat[pos][0] == '_':
        return clean_one_predefined(pat, duck_letters, pos + 1)
    for dl in duck_letters:
        for sl in duck_letters[dl]:
            if sl[0] == pat[pos][0]:
                new_duck_letters = duck_letters.copy()
                new_pat = pat.copy()
                del new_duck_letters[dl]
                new_pat[pos] = (pat[pos], dl)
                res.extend(clean_one_predefined(new_pat, new_duck_letters, pos + 1))
    return res



input_pattern = list(filter(lambda x: x[0] != ' ' and x[0] != '_', predefined_pattern))
res = clean_one_predefined(input_pattern, LETTERS)

res = list(map(lambda x: (list(map(lambda y: y[1], x))), res))
res = list(map(lambda x: [z for z in LETTERS.keys() if z not in x], res))
print(res)


def render_pattern(pat: list[tuple[str, int]] | list[str]):
    """ build as string from a given pattern, a pattern being either a list of
    strings or a tuple
    the tuple would be containg the index of the duckwordword in the words and
    the index of the actual word in a duckword """
    result_str = ""
    for symbol_tuple in pat:
        if symbol_tuple == "_" or symbol_tuple == " " or symbol_tuple == "a" or symbol_tuple == "b" or symbol_tuple == "c" or symbol_tuple == "d" or symbol_tuple == "e" or symbol_tuple == "f" or symbol_tuple == "g" or symbol_tuple == "h" or symbol_tuple == "i" or symbol_tuple == "j" or symbol_tuple == "k" or symbol_tuple == "l" or symbol_tuple == "m" or symbol_tuple == "n" or symbol_tuple == "o" or symbol_tuple == "p" or symbol_tuple == "q" or symbol_tuple == "r" or symbol_tuple == "s" or symbol_tuple == "t" or symbol_tuple == "u" or symbol_tuple == "v" or symbol_tuple == "w" or symbol_tuple == "x" or symbol_tuple == "y" or symbol_tuple == "z":
            result_str += str(symbol_tuple)
            continue

        if symbol_tuple[1] is None:
            continue
        # print(symbol_tuple)
        result_str += symbol_tuple[0]
    # print(result_str)
    return result_str


def is_all_words(s):
    "checks if a string s is made of words from the wordlists"
    words = s.split(" ")
    allwords = True
    for word in words:
        if word[0] == "_":
            break
        if not check_is_word(word):
            allwords = False
    return allwords


def check_is_word(word: str):
    """checks if word could be in wordlist, returns false if already no
    possibility left"""
    # this could be faster with biary search over sorted list
    wordlength = len(word)
    is_in_wordlist = False

    word = word.replace("_", ".")
    for s in WORDLISTS[wordlength]:
        if re.match(word, s) is not None:
            is_in_wordlist = True
    return is_in_wordlist


def begin_from_next_free_position(pattern: list[str] |
                                  (list[tuple[str, int] | str]),
                                  letters: dict[str, list[str]], skip=0):
    """ populates the free _ with the leftover letters
        recursive function
    """
    # print("a")
    # begin at index skip
    k = skip
    if k >= len(pattern):
        return
    if pattern[k] == "_":
        for n in letters:
            # print(n)
            new_letters = letters.copy()
            # print(new_letters)
            new_letters.remove(n)
            for w in LETTERS[n]:
                new_pattern = pattern.copy()
                new_pattern[k] = (w[0], n)
                s = render_pattern(new_pattern)
                if is_all_words(s):
                    if len(pattern) <= k+1 or pattern[k+1] == " ":
                        # print(s)
                        POSSIBLE_SOULTIONS.add(s)
                        # print(newPattern)

                    begin_from_next_free_position(new_pattern, new_letters,
                                                    k+1)
            # break
    else:
            begin_from_next_free_position(pattern, letters, k+1)


PRECLEANED_PATTERNS = []
POSSIBLE_SOULTIONS = set()


def main():
    letters = LETTERS.copy()
    print(predefined_pattern)
    print("ASDF")
    print(render_pattern(predefined_pattern))
    PRECLEANED_PATTERNS = clean_one_predefined(predefined_pattern, letters, 0)
    print(PRECLEANED_PATTERNS)
    print("All possible patterns for your input computed (" +
          str(len(PRECLEANED_PATTERNS))+")")
    for i, p in enumerate(PRECLEANED_PATTERNS):
        # breakpoint()
        # print(p)
        begin_from_next_free_position(p, res[i])
        print(f"[{i}/{len(PRECLEANED_PATTERNS)}]")
        for p in POSSIBLE_SOULTIONS:
            print(p)


if __name__ == '__main__':
    main()
