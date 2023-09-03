import re

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

print(checkIsWord("screu"))