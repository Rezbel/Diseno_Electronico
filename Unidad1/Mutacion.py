import random
import Operaciones as opt

if __name__ == "__main__":
    minv = 0
    maxv = 100
    rm = 50
    Vo = []

    obj = opt.SumadeCuadrados(minv, maxv, Vo)
    pop = obj.Poblacion(10, 6)
    promedio = float("inf")
    rangoLimite = random.randint(0, 5)

    print("Límite de paro:", rangoLimite)

    while promedio > rangoLimite:
        print("\nPoblación:")
        for indv in pop:
            print(indv)

        padres = obj.ObtenerPadres(10, pop)
        print("\nPadres:")
        for padre in padres:
            print(padre)

        descendencia = obj.cruzaEnunPunto(padres)
        print("\nHijos antes de mutación:")
        for hijo in descendencia:
            print(hijo)

        mutacionDes = [
            [random.randint(minv, maxv) if random.randint(0, 100) > rm else gen for gen in hijo]
            for hijo in descendencia
        ]

        print("\nHijos después de mutación:")
        for hijo in mutacionDes:
            print(hijo)

        seleccion = obj.seleccionAmbiental(mutacionDes, padres, 10)
        print("\nSelección:")
        for seleccionados in seleccion:
            print(seleccionados)

        pop = seleccion
        promedio = obj.promedioVO()
        Vo.clear()
