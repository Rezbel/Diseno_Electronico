import matplotlib.pyplot as plt

archivo = open("datos.csv")
contenido = archivo.readline()
archivo.close()

datos=[]

for i in contenido:
    datos.append(int(i))

print(datos)
plt.boxplot(datos)
plt.title("Boxplot Basico")
plt.show()