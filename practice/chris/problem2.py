# take note that each list can be of different lengths

def alternateConcat(lista, listb):
    if (not lista and not listb):
        return []
    elif (lista and not listb):
        return lista
    elif (not lista and listb):
        return listb
    else:
        returnList = [lista[0],listb[0]]
        returnList = returnList + (alternateConcat(lista[1:],listb[1:]))
        return returnList

list1=['never','give','up']
list2=['gonna','you']
print alternateConcat(list1, list2)
