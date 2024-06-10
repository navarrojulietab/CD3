# -*- coding: utf-8 -*-
"""MiModulo.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/12gH5E3T8xXYu06Vq2dg3vB3yuwRJZhwN
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm, chi2
import statsmodels.api as sm

class ResumenNumerico:
  def __init__(self, datos):
    self.datos = np.array(datos)

  def calculo_de_media(self):
    media=np.mean(self.datos)
    return media

  def calculo_de_mediana(self, datos=None):
    mediana=np.median(self.datos)
    return mediana

  def calculo_de_desvio_estandar(self):
    media = self.calculo_de_media()
    diferencias =[]
    var = 0
    for i in self.datos:
      var += (media - i) ** 2 / len(ingresos)
    desvio_estandar = var ** 0.5

    return desvio_estandar

  def calculo_de_cuartiles(self):
    datos_ordenados = sorted(self.datos)
    if len(self.datos) % 4 != 0 :
      q1 = datos_ordenados[len(self.datos)//4-1]
      q2 = self.calculo_de_mediana()
      q3 = datos_ordenados[len(self.datos)*3//4-1]
    else:
      q1 = (datos_ordenados[len(self.datos)//4-1] + datos_ordenados[len(self.datos)//4])//2
      q2 = self.calculo_de_mediana()
      q3 = (datos_ordenados[len(self.datos)*3//4-1] + datos_ordenados[len(self.datos)*3//4])//2

    return [q1, q2, q3]

  def generacion_resumen_numerico(self):
  res_num = {
        'Media': self.calculo_de_media(),
        'Mediana': self.calculo_de_mediana(),
        'Desvio': self.calculo_de_desvio_estandar(),
        'Cuartiles': self.calculo_de_cuartiles(),
        'Mínimo': min(self.datos),
        'Máximo': max(self.datos)
        }

  return res_num

  def muestra_resumen(self):
    res_num = self.generacion_resumen_numerico()
    for estad,valor in res_num.items():
      print(f'{estad}:{np.round(valor,3)}')

class ResumenGrafico:
  def __init__ (self, datos=None, x=None):
    if datos is not None:
            self.datos = np.array(datos)
    self.x = x
  def evaluacion_histograma(self, h, x):
    # Devuelve una estimación del valor del histograma en x
    self.x = x
    minimo = min(self.x)
    maximo = max(self.x)
    intervalos = np.arange(minimo, maximo + h, h)  # Se ajusta el último valor del rango para incluir el máximo
    f_abs = np.zeros(len(intervalos) - 1)
    for dato in self.datos:
      for j in range(len(intervalos) - 1):
        if dato >= intervalos[j] and dato < intervalos[j + 1]:
          f_abs[j] += 1
          break  # Salir del bucle interno una vez que se encuentra el intervalo adecuado
    f_rel = f_abs / len(self.datos)
    estim_hist = f_rel / h
    estimaciones = []
    for punto in x:
            # Encontrar el índice del intervalo correspondiente en la grilla
        indice = int((punto - minimo) / h)
        if indice >= 0 and indice < len(estim_hist):
                # Agregar la estimación del histograma para este punto en la grilla
          estimaciones.append(estim_hist[indice])
        else:
          estimaciones.append(0)  # Si el punto está fuera de los límites, se asume una estimación de 0
    return estimaciones

  def kernel_gaussiano(self, x):
        self.x = x
        valor_kernel_gaussiano = (1/np.sqrt(2*np.pi))*np.exp(-0.5*self.x**2)
        return valor_kernel_gaussiano

  def kernel_uniforme(self, x):
        self.x = x
        valor_kernel_uniforme = 1*((self.x>-0.5)&(self.x<0.5))
        return valor_kernel_uniforme

  def kernel_cuadratico(self, x):
        xx = 0.75*(1-x**2)
        valor_kernel_cuadratico = xx*((x>-1)&(x<1))
        return valor_kernel_cuadratico

  def kernel_triangular(self, x):
        xmas = (1+x) * ((x > -1)&(x<0))
        xmen = (1-x) * ((x > 0)&(x < 1))
        valor_kernel_triangular = xmas+xmen
        return valor_kernel_triangular

  def mi_densidad(self, x,data,h, kernel):
        # x: Puntos en los que se evaluará la densidad
        # data: Datos
        # h: Ancho de la ventana (bandwidth)
        n = len(data)
        densidad_estimada = []
        for valor_x in x:
          contribuciones_kernel = []
          for dato in data:
            if kernel == "gaussiano":
              contribuciones_kernel.append(self.kernel_gaussiano((dato - valor_x) / h)) #paso uno a uno los datos
            elif kernel == "uniforme":
              contribuciones_kernel.append(self.kernel_uniforme((dato - valor_x) / h)) #paso uno a uno los datos
            elif kernel == "cuadratico":
              contribuciones_kernel.append(self.kernel_cuadratico((dato - valor_x) / h)) #paso uno a uno los datos
            elif kernel == "triangular":
              contribuciones_kernel.append(self.kernel_triangular((dato - valor_x) / h)) #paso uno a uno los datos

          suma_contribuciones = np.sum(contribuciones_kernel)
          densidad_estimada.append(suma_contribuciones / (n * h))
        return densidad_estimada

class GeneradoraDeDatos():
    def __init__(self, N):
        self.N = N

    def generar_datos_dist_norm(self, media, desvio):
      return np.random.normal(loc=media, scale=desvio, size = self.N)

    def pdf_norm(self,x, media, desvio): #curva teorica normal
      return norm.pdf(x, media, desvio)

    def r_BS(self):
        u = np.random.uniform(size=(self.N,))
        y = u.copy()
        ind = np.where(u > 0.5)[0]
        y[ind] = np.random.normal(0, 1, size=len(ind))
        for j in range(5):
            ind = np.where((u > j * 0.1) & (u <= (j+1) * 0.1))[0]
            y[ind] = np.random.normal(j/2 - 1, 1/10, size=len(ind))
            self.y = y
        return y

    def teorica_BS(self,x, media, desvio):
      contribucion_estandar = norm.pdf(x, loc=media, scale = desvio) / 2  #termino 1: densidad de una normal teorica(ver)
      contribucion_adicional = 0  # Inicializar la variable antes del bucle for
      for j in range(5):
        media_adicional = (j/2)-1
        desvio_adicional = 1/10
        contribucion_adicional += norm.pdf(x,loc=media_adicional ,scale=desvio_adicional)

      contribucion_adicional *= (1/10)

      fBS_x = contribucion_estandar + contribucion_adicional
      return fBS_x



class Cualitativas():
  def __innit__(self,datos=None):
    if datos is not None:
      self.datos = np.array(datos)
  def test(self, val_obs, prob,alfa):
    n = sum(val_obs)
    val_esp = [p*n for p in prob]
    resta = [val_obs[i]-val_esp[i] for i in range(len(val_obs))]
    X_obs = sum(resta[i]**2/val_esp[i] for i in range(len(val_esp)))
    gf = len(prob)-1
    X_teo = chi2.ppf(1-alfa,gf)
    p_valor = 1- chi2.cdf(X_obs,gf)
    print('Estadistico observado:',X_obs)
    print('Estadistico teorico:',X_teo)
    print('p valor:',p_valor)
    if p_valor > alfa and X_obs < X_teo:
      print('No hay evidencia suficiente para rechazar la hipótesis nula')
    elif p_valor <= alfa and X_obs >= X_teo:
      print('Hay evidencia suficiente para rechazar la hipótesis nula')
    else:
      print('Hay un error, no hay congruencia entre los resultados obtenidos')