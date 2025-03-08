import numpy as np

def calcMAE(valores_reales, valores_estimados):#Error Absoluto Medio (MAE)
    #Mide el error medio en las mismas unidades que los datos reales. Más bajo es mejor
    MAE = np.mean(np.abs(valores_reales - valores_estimados))
    return MAE


def calcMSE(valores_reales, valores_estimados):#Error Cuadrático Medio (MSE)
    #Penaliza más a los errores grandes
    MSE = np.mean((valores_reales - valores_estimados)** 2)
    return MSE

def calcRMSE(valores_reales, valores_estimados):#Raíz del Error Cuadratico Medio (RMSE)
    #Penaliza más a los errores grandes. Pone al error en las mismas unidades que los datos reales
    MSE = calcMSE(valores_reales, valores_estimados)
    RMSE = np.sqrt(MSE)
    return RMSE

def calcMAPE(valor_reales, valores_estimados):#Erro Porcentual Absoluto Medio (MAPE)
    #Mide el error en porcentaje. Facilita interpretación en terminos relativos
    MAPE = np.mean(np.abs((valor_reales - valores_estimados)/valor_reales)) * 100
    return MAPE

#1 promedio de errires
#2 da promedio de error, pero si no grandes positivos negativos. hace grande/exagera el valor
#3 los mismo, pero te lo da en las unidades que estas usando
#4 da porcentaje de error
