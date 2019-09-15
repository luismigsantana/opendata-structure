from skiplistlist import SkiplistList

lista = SkiplistList() 

for i in range(100):
	lista.add(i, i)

print(lista)
print("Altura: ", lista.h) #Será a maior altura possivel, se não for a mesma que a altura na nova lista ou da antiga-modificada algo deu errado
segunda = lista.truncate(50)
print("Segunda lista:", segunda, " de altura: ", segunda.h, " e tamanho: ", segunda.n)
print("Antiga Lista: ",lista, " de altura: ", lista.h, " e tamanho: ", lista.n)


	