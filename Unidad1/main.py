import Operaciones

class Main:
    def __init__(self, cantidad_vectores, tamaño_vector, rango_numeros, num_padres):
        self.cantidad_vectores = cantidad_vectores
        self.tamaño_vector = tamaño_vector
        self.rango_numeros = rango_numeros
        self.num_padres = num_padres

    def ejecutar(self):
        vectores = [Operaciones.generar_vector(self.tamaño_vector, self.rango_numeros) for _ in range(self.cantidad_vectores)]
        padres = Operaciones.seleccion_padres_torneo(vectores, self.num_padres)

        for i, vector in enumerate(vectores, start=1):
            print(f"Vector {i}: {vector} - Valor objetivo: {Operaciones.calcular_valor_objetivo(vector)}")

        print("\nPadres seleccionados:")
        for i, padre in enumerate(padres, start=1):
            print(f"Padre {i}: {padre} - Valor objetivo: {Operaciones.calcular_valor_objetivo(padre)}")


if __name__ == '__main__':
    app = Main(cantidad_vectores=4, tamaño_vector=5, rango_numeros=(1, 100), num_padres=2)
    app.ejecutar()
