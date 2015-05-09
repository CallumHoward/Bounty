
# sort by digit
# if two numbers have equal first digits
# if two numbers with equal first digit and one doesn't have another digit

def biggestArrange(lista):
    stringList = [str(x) for x in lista]
    stringList.sort(reverse=True)
    return int("".join(stringList))

testList = [5,545,555,55,5454]
print biggestArrange(testList)
