
def sumFor (list):
    sum = 0
    for i in list:
        sum = sum + i

    return sum

def sumWhile (list):
    sum = 0
    i = 0
    while (i < len(list)):
        sum = sum + list[i]
        i = i + 1

    return sum

def sumRecursion (list):
    if (len(list) == 1):
        return list[0]
    else:
        return list[0] + sumRecursion(list[1:])

ooft = [1,2,3,4]

print sumFor(ooft)
print sumWhile(ooft)
print sumRecursion(ooft)

