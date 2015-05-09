#!/usr/bin/env python

# problem2.py
# combines two lists
# Callum Howard 2015

def combine(listA, listB):
    for element in zip(listA, listB):
        yield element[0]
        yield element[1]

def combine2(listA, listB):
    i = 0;
    listC = []
    while (not (not listA[i] and not listB[i])):
        if (listA[i]):
            listC.append(listA[i])
        if (listB[i]):
            listC.append(listB[i])
        i += 1
    return listC

for item in combine(['a','b','c','d','e','f'], [1,2,3,4,5,6,7]):
    print item,

print combine2(['a','b','c','d','e','f'], [1,2,3,4,5,6,7])
