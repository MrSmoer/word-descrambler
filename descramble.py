import re

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
    #"Diving Weight":["w","d","l"],
    #"Reverse Mousetrap":["t","m","r"],
    #"Saw":["t","s","h"],
    "Lawnmower":["l","e","s"]
}
LETTERS={
    "Lamp":["a","b"],
    "Cage":["s","d","e"],
    "Egg": ["m"],
    "Saw":["t","s","h"],
    "Egg2":["e"],
}
print(len(LETTERS))
pattern=["e","m","a","i","l"," ", "m","_"," ", "_", " ", "_", "_"]#, "_", "_","_"]
pattern=["m","_"," ","_","_"]

def beginFromNextFreePosition(currPattern:list, currLetters:dict[str, list[str]],skipto:int):
    # TODO skipping properly

    k=0
    for c in range(len(currPattern)-skipto+1):
        k=c+skipto
        if k==len(currPattern):
            decideOnLetter(currPattern,currLetters, skipto)
            return 
                #decideOnLetter(currPattern,currLetters,0)
            
        if currPattern[k]==" ":
            #TODO check if las word is word
            continue
        if currPattern[k]!="_":
            #print("next free is "+str(k))
            continue
        

        for n in currLetters:
            newLetters = currLetters.copy()
            letter=newLetters.pop(n)
            newPattern=currPattern.copy()
            newPattern[k]=(n,None)
            if decideOnLetter(newPattern,newLetters,k,limit=1):
                beginFromNextFreePosition(newPattern,newLetters,skipto=k)
            else:
                continue
            
        break
        #print(free)
    #print("exit one up")

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

def decideOnLetter(pattern:list, letters:dict[str, list[str]],skipto,limit=-1):
    
    countOfNotDecided=0
    k=0
    ret = False
    for h in range(len(pattern)-skipto):
        k=h+skipto
        if pattern[k]==' ' or pattern[k]=="_":
            continue
        if pattern[k][1]!=None:
            continue

        countOfNotDecided+=1
    
        for n in range(len(LETTERS[pattern[k][0]])):
            newPattern:list[(str,int)]=pattern.copy()
            newPattern[k]=(newPattern[k][0],n)
            if (k<len(newPattern)-1 and newPattern[k+1]==" " and not renderPattern(newPattern)) or k>=len(newPattern)-1:
                continue
                #i=1
            ret = decideOnLetter(newPattern, letters,k)
        break

    if countOfNotDecided<1 or (h == limit and ret):
        return renderPattern(pattern)
    return ret


def renderPattern(pattern:list[(str,int)]):
    s=""
    
    for k in pattern:
        if not isinstance(k, tuple) :
            s+=str(k)
            continue

        if k[1]==None:
                return True
        s+=LETTERS[k[0]][k[1]]
    allwords=isAllWords(s)
    
    print(s)

    return allwords
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
    with open("wordlists/"+str(l)+".txt","r") as f:
        b=f.read()
        lis=re.split(r'[\n,|]',b)
        word = word.replace("_",".")
        for s in lis:
            if re.match(word,s) != None:
                isInside=True
    return isInside

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
        beginFromNextFreePosition(p[0],p[1],0)

    

if __name__=='__main__':
    main()