#!/usr/bin/env python

# problem1.py
# Write three functions that compute the sum of the numbers in a given list using
# a for-loop,
# a while-loop and
# recursion
#
# Callum Howard 2015

def sumFor(list):
    return sum(item for item in list)

def sumWhile(list):
    i = 0
    sum = 0;
    while (i < len(list)):
        sum += list[i]
        i += 1;
    return sum

def sumRecursion(list):
    # base case
    if (len(list) <= 0):
        return 0
    else:
        return list[0] + sumRecursion(list[1:])


testList = [1,2,3,4,6,8,99,0,1]
print sumFor(testList)
print sumWhile(testList)
print sumRecursion(testList)
