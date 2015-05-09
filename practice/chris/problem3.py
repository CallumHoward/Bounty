
def fibonacci():
    lista = [0,1]
    i = 2
    while (i < 100):
        lista.append(lista[-2] + lista[-1])
        i+=1

    return lista

print fibonacci()
