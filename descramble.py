import re


def readWordlist(i):
    with open("wordlists/"+str(i)+".txt","r") as f:
                    b=f.read()
                    return re.split(r'[\n,|]',b)

wordlistnumbers=[1,2,5]
WORDLISTS={}
for i in wordlistnumbers:
    WORDLISTS[i]=readWordlist(i)

LETTERS={
    "Lamp":["l","s"],
    "Egg": ["e"],
    "Egg2":["e"],
    "Cage":["c","a"],
    "Mallet":["m","h","r"],
    "Icecream":["i","v"],
    "Mug":["m","c"],
    "Apple":["a"],
    "Hammer Head":["h","a","i"],
    "Diving Weight":["w","d","l"],
    "Reverse Mousetrap":["t","m","r"],
    "Saw":["t","s","h"],
    "Lawnmower":["l","e","s"]
}

pattern=["e","m","a","i","l"," ", "m","_"," ", "_", " ", "_", "_", "_", "_","_"]


def cleanOnePredefined(pattern:list, letters:dict[str, list[str]]):
    countOfDirty=0
    for k in range(len(pattern)):
        if pattern[k] != ' ' and pattern[k] !='_' and not isinstance(pattern[k], tuple):
                countOfDirty+=1
                for key in letters:
                    if pattern[k] in letters[key]:
                        index = letters[key].index(pattern[k])
                        newLetters=letters.copy()
                        newPattern=pattern.copy()
                        newPattern[k]=(key,index)
                        newLetters.pop(key)
                        cleanOnePredefined(newPattern, newLetters)
    if countOfDirty < 1:
        precleanedPatterns.append((pattern,letters))


def renderPattern(pattern:list[(str,int)]):
    s=""
    
    for k in pattern:
        if not isinstance(k, tuple) :
            s+=str(k)
            continue

        if k[1]==None:
            continue
        
        s+=LETTERS[k[0]][k[1]]
    return s

def isAllWords(s):
    words=s.split(" ")
    allwords=True
    for word in words:
        if word[0]=="_":
            break
        if not checkIsWord(word):
            allwords=False
    return allwords

def checkIsWord(word:str):
    l=len(word)
    isInside=False
    
    word = word.replace("_",".")
    for s in WORDLISTS[l]:
        if re.match(word,s) != None:
            isInside=True
    return isInside

def beginFromNextFreePosition(pattern, letters, skip=0):
    #nextFree=0
    for i in range(len(pattern)-skip):
        k=i+skip
        if pattern[k] == "_":
            for n in letters:
                newLetters = letters.copy()
                letter=newLetters.pop(n)
                for a in range(len(LETTERS[n])):
                    newPattern=pattern.copy()
                    newPattern[k]=(n,a)
                    s = renderPattern(newPattern)
                    if isAllWords(s):
                        if len(pattern)<=k+1 or pattern[k+1]==" ":
                            print(s)
                            #print(newPattern)
                        
                        beginFromNextFreePosition(newPattern,newLetters, k)
                
            break
    




precleanedPatterns=[]
def main():
    letters=LETTERS.copy()
    for k in pattern:
        if k[0] in letters:
            letters.pop(k[0])
    print("Egg" in letters.keys())
    
    cleanOnePredefined(pattern, letters)
    print("All possible patterns for your input computed ("+str(len(precleanedPatterns))+")")
    for p in precleanedPatterns:
        beginFromNextFreePosition(p[0],p[1])

    

if __name__=='__main__':
    main()