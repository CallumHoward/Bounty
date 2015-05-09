#!/usr/bin/env python

# problem3.py
# find permutation with largest value
# Callum Howard 2015

def largestPerm(list):
    digits = []
    for item in list:
        for letter in str(item):
            digits.append(letter)
    return "".join(sorted(digits, reverse=True))

testList = [50, 2, 1, 9, 400]
print largestPerm(testList)
