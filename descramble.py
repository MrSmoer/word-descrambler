import re


def read_wordlist(lettercount):
    "opens a wordlist with the number of words"
    with open("wordlists/"+str(lettercount)+".txt", "r", encoding='ascii') as f:
        b = f.read()
        return re.split(r'[\n,|]', b)


wordlistnumbers = [1, 2, 5]
WORDLISTS = {}
for i in wordlistnumbers:
    WORDLISTS[i] = read_wordlist(i)

LETTERS = {
    "Diving Weight": ["weight", "d", "b", "t", "lead"], # l
    "Mug": ["mug", "cup"], # m e*m*ail
    "Hammer Head": ["hammer", "a", "iron"], # i
    "Reverse Mousetrap": ["trap", "mousetrap", "reverse"], # m
    "Lamp": ["lamp"], # l
    "Apple": ["apple"], # a
    "Egg": ["egg"], # e
    "Egg2": ["egg"], # e
    "Saw": ["saw", "tennon saw", "h"], # s *s*mell
    "Lawnmower": ["lawnmower", "mower", "engine", "spinny-thingy"], # e
    "Mallet": ["mallet", "hammerhead", "s"], # -> m
    "Icecream": ["icecream", "v-the brand of icecream?"], # -> i
    # "Cage": ["cage", "aviary", "birdcage"],
    "Money": ["money"], # -> m
}

predefined_pattern = ["e", "m", "a", "i", "l", " ", "m", "e", " ", "i", " ", "_", "_", "_", "_", "_"]


def clean_one_predefined(pat: list[str] | (list[tuple[str, int] | str]), duck_letters: dict[str, list[str]]):
    """ generates all possibilites for the letters to fulfill the given pattern, and appends them to the global precleaned_patterns
    this function is recursive
    a letter is dirty if it is predefined, but not predefined as a tuple -> just a string
    """
    unchosen_dirty_letters = 0
    for index_in_pattern, letter_to_replace in enumerate(pat):
        # loop only over the dirty letters in the current predefined pattern
        if letter_to_replace != ' ' and letter_to_replace != '_':
            if isinstance(letter_to_replace, tuple):
                continue
            unchosen_dirty_letters += 1
            # try every letter left in the current duckletters
            for duck_letter in duck_letters:
                subletters = duck_letters[duck_letter]

                # just take first letter of subletters, its the only relevant
                for index_in_subletters, subletter in enumerate(subletters):
                    cut_subletter = subletter[0]
                    if letter_to_replace in cut_subletter:
                        # copy current pattern for next depth
                        newLetters = duck_letters.copy()
                        newPattern = pat.copy()
                        # replace the letter_to_replace with the chosen tuple from duckletters
                        newPattern[index_in_pattern] = (duck_letter, index_in_subletters)
                        # remove the chosen  duckletter, it cannot be used twice
                        newLetters.pop(duck_letter)
                        clean_one_predefined(newPattern, newLetters)

    # ends recursion in deepest stage, if no unreplaced letters left in pattern 
    if unchosen_dirty_letters < 1:
        PRECLEANED_PATTERNS.append((pat, duck_letters))
        if len(PRECLEANED_PATTERNS) % 100000 == 0:
            print(f"{len(PRECLEANED_PATTERNS)}")  # f"asdf{len(PRECLEANED_PATTERNS)})


def render_pattern(pat: list[tuple[str, int]] | list[str]):
    """ build as string from a given pattern, a pattern being either a list of strings or a tuple
    the tuple would be containg the index of the duckwordword in the words and the index of the actual word in a duckword """
    result_str = ""
    for symbol_tuple in pat:
        if not isinstance(symbol_tuple, tuple):
            result_str += str(symbol_tuple)
            continue

        if symbol_tuple[1] is None:
            continue
        
        result_str += LETTERS[symbol_tuple[0]][symbol_tuple[1]][0]
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
    "checks if word could be in wordlist, returns false if already no possibility left"
    # this could be faster with biary search over sorted list
    wordlength = len(word)
    is_in_wordlist = False
    
    word = word.replace("_", ".")
    for s in WORDLISTS[wordlength]:
        if re.match(word, s) is not None:
            is_in_wordlist = True
    return is_in_wordlist


def begin_from_next_free_position(pattern: list[str] | (list[tuple[str, int] | str]), letters: dict[str, list[str]], skip=0):
    """ populates the free _ with the leftover letters 
        recursive function
    """
    # begin at index skip
    for i in range(len(pattern)-skip):
        k = i+skip
        if pattern[k] == "_":
            for n in letters:
                new_letters = letters.copy()
                new_letters.pop(n)
                for a in range(len(LETTERS[n])):
                    new_pattern = pattern.copy()
                    new_pattern[k] = (n, a)
                    s = render_pattern(new_pattern)
                    if is_all_words(s):
                        if len(pattern) <= k+1 or pattern[k+1] == " ":
                            # print(s)
                            POSSIBLE_SOULTIONS.add(s)
                            # print(newPattern)
                        
                        begin_from_next_free_position(new_pattern, new_letters, k)
            break
    

PRECLEANED_PATTERNS = []
POSSIBLE_SOULTIONS = set()

def main():
    letters = LETTERS.copy()
    for k in predefined_pattern:
        if k[0] in letters:
            letters.pop(k[0])
    print("Egg" in letters.keys())
    print(render_pattern(predefined_pattern))
    clean_one_predefined(predefined_pattern, letters)
    print("All possible patterns for your input computed ("+str(len(PRECLEANED_PATTERNS))+")")
    for p in PRECLEANED_PATTERNS:
        # breakpoint()
        begin_from_next_free_position(p[0], p[1])

        for p in POSSIBLE_SOULTIONS:
            print(p)
    
if __name__ == '__main__':
    main()