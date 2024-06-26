# -*- coding: utf-8 -*-
"""MiModulo.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/12gH5E3T8xXYu06Vq2dg3vB3yuwRJZhwN
"""
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
import pandas as pd
from scipy.stats import norm, chi2
from sklearn.metrics import confusion_matrix, roc_curve, roc_auc_score
import random

class ResumenNumerico:
    """
    Una clase para calcular estadísticas descriptivas de un conjunto de datos numéricos.

    Atributos:
    datos (numpy.ndarray): Un arreglo numpy que contiene solo datos numéricos.
    """

    def __init__(self, datos):
        """
        Inicializa la clase ResumenNumerico con un DataFrame y convierte los datos numéricos a un arreglo numpy.

        Args:
        datos (pandas.DataFrame): Un DataFrame que contiene los datos.
        """
        self.datos = datos.select_dtypes(include=np.number).to_numpy()

    def calculo_de_media(self):
        """
        Calcula la media de los datos.

        Returns:
        float: La media de los datos.
        """
        media = np.mean(self.datos)
        return media

    def calculo_de_mediana(self):
        """
        Calcula la mediana de los datos.

        Returns:
        float: La mediana de los datos.
        """
        mediana = np.median(self.datos)
        return mediana

    def calculo_de_desvio_estandar(self):
        """
        Calcula el desvío estándar de los datos.

        Returns:
        float: El desvío estándar de los datos.
        """
        var = np.var(self.datos)
        desvio_estandar = var ** 0.5
        return desvio_estandar

    def calculo_de_cuartiles(self):
        """
        Calcula los cuartiles de los datos por columna.

        Returns:
        list: Una lista de listas donde cada sublista contiene los cuartiles [Q1, Q2, Q3] de una columna.
        """
        cuartiles_por_columna = []
        for i in range(self.datos.shape[1]):
            datos_ordenados = sorted(self.datos[:, i])  # Ordenar los datos de la columna actual
            if len(datos_ordenados) % 4 != 0:
                q1 = datos_ordenados[len(datos_ordenados) // 4 - 1]
                q2 = np.median(datos_ordenados)  # Usar np.median directamente en los datos ordenados
                q3 = datos_ordenados[len(datos_ordenados) * 3 // 4 - 1]
            else:
                q1 = (datos_ordenados[len(datos_ordenados) // 4 - 1] + datos_ordenados[len(datos_ordenados) // 4]) // 2
                q2 = np.median(datos_ordenados)  # Usar np.median directamente en los datos ordenados
                q3 = (datos_ordenados[len(datos_ordenados) * 3 // 4 - 1] + datos_ordenados[len(datos_ordenados) * 3 // 4]) // 2
            cuartiles_por_columna.append([q1, q2, q3])

        return cuartiles_por_columna

    def generacion_resumen_numerico(self):
        """
        Genera un resumen numérico que incluye media, mediana, desvío estándar, cuartiles, mínimo y máximo.

        Returns:
        dict: Un diccionario con el resumen numérico.
        """
        res_num = {
            'Media': self.calculo_de_media(),
            'Mediana': self.calculo_de_mediana(),
            'Desvio': self.calculo_de_desvio_estandar(),
            'Cuartiles': self.calculo_de_cuartiles(),
            'Mínimo': np.min(self.datos),
            'Máximo': np.max(self.datos)
        }

        return res_num

    def muestra_resumen(self):
        """
        Muestra el resumen numérico en la consola con los valores redondeados a 3 decimales.
        """
        res_num = self.generacion_resumen_numerico()
        for estad, valor in res_num.items():
            print(f'{estad}: {np.round(valor, 3)}')

class ResumenGrafico:
    """
    Una clase para generar y evaluar gráficos estadísticos y estimaciones de densidad.

    Atributos:
    datos (numpy.ndarray): Un arreglo numpy que contiene los datos.
    x (numpy.ndarray): Puntos en los que se evaluará la densidad o histograma.
    """

    def __init__(self, datos=None, x=None):
        """
        Inicializa la clase ResumenGrafico con un conjunto de datos y puntos x.

        Args:
        datos (numpy.ndarray, opcional): Un arreglo numpy que contiene los datos.
        x (numpy.ndarray, opcional): Puntos en los que se evaluará la densidad o histograma.
        """
        if datos is not None:
            self.datos = np.array(datos)
        self.x = x

    def evaluacion_histograma(self, h, x):
        """
        Devuelve una estimación del valor del histograma en x.

        Args:
        h (float): El ancho de los intervalos del histograma.
        x (numpy.ndarray): Puntos en los que se evaluará el histograma.

        Returns:
        list: Estimaciones del histograma en los puntos x.
        """
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
        """
        Calcula el valor del kernel Gaussiano en los puntos x.

        Args:
        x (numpy.ndarray): Puntos en los que se evaluará el kernel.

        Returns:
        numpy.ndarray: Valores del kernel Gaussiano en los puntos x.
        """
        self.x = x
        valor_kernel_gaussiano = (1/np.sqrt(2*np.pi)) * np.exp(-0.5 * self.x ** 2)
        return valor_kernel_gaussiano

    def kernel_uniforme(self, x):
        """
        Calcula el valor del kernel Uniforme en los puntos x.

        Args:
        x (numpy.ndarray): Puntos en los que se evaluará el kernel.

        Returns:
        numpy.ndarray: Valores del kernel Uniforme en los puntos x.
        """
        self.x = x
        valor_kernel_uniforme = 1 * ((self.x > -0.5) & (self.x < 0.5))
        return valor_kernel_uniforme

    def kernel_cuadratico(self, x):
        """
        Calcula el valor del kernel Cuadrático en los puntos x.

        Args:
        x (numpy.ndarray): Puntos en los que se evaluará el kernel.

        Returns:
        numpy.ndarray: Valores del kernel Cuadrático en los puntos x.
        """
        xx = 0.75 * (1 - x ** 2)
        valor_kernel_cuadratico = xx * ((x > -1) & (x < 1))
        return valor_kernel_cuadratico

    def kernel_triangular(self, x):
        """
        Calcula el valor del kernel Triangular en los puntos x.

        Args:
        x (numpy.ndarray): Puntos en los que se evaluará el kernel.

        Returns:
        numpy.ndarray: Valores del kernel Triangular en los puntos x.
        """
        xmas = (1 + x) * ((x > -1) & (x < 0))
        xmen = (1 - x) * ((x > 0) & (x < 1))
        valor_kernel_triangular = xmas + xmen
        return valor_kernel_triangular

    def mi_densidad(self, x, data, h, kernel):
        """
        Calcula la densidad estimada utilizando un kernel específico.

        Args:
        x (numpy.ndarray): Puntos en los que se evaluará la densidad.
        data (numpy.ndarray): Datos.
        h (float): Ancho de la ventana (bandwidth).
        kernel (str): Tipo de kernel a utilizar ('gaussiano', 'uniforme', 'cuadratico', 'triangular').

        Returns:
        list: Densidad estimada en los puntos x.
        """
        n = len(data)
        densidad_estimada = []
        for valor_x in x:
            contribuciones_kernel = []
            for dato in data:
                if kernel == "gaussiano":
                    contribuciones_kernel.append(self.kernel_gaussiano((dato - valor_x) / h))
                elif kernel == "uniforme":
                    contribuciones_kernel.append(self.kernel_uniforme((dato - valor_x) / h))
                elif kernel == "cuadratico":
                    contribuciones_kernel.append(self.kernel_cuadratico((dato - valor_x) / h))
                elif kernel == "triangular":
                    contribuciones_kernel.append(self.kernel_triangular((dato - valor_x) / h))
            suma_contribuciones = np.sum(contribuciones_kernel)
            densidad_estimada.append(suma_contribuciones / (n * h))
        return densidad_estimada

    def miqqplot(data):
        """
        Genera un gráfico Q-Q (quantile-quantile) para comparar los cuantiles muestrales con los teóricos.

        Args:
        data (numpy.ndarray): Datos a ser graficados.
        """
        media = np.mean(data)
        desvio = np.std(data)
        data_s = (data - media) / desvio
        cuantiles_muestrales = np.sort(data_s)
        n = len(data)
        pp = np.arange(1, (n + 1)) / (n + 1)
        cuantiles_teoricos = norm.ppf(pp)
        plt.scatter(cuantiles_teoricos, data_s, color='blue', marker='o')
        plt.xlabel('Cuantiles teóricos')
        plt.ylabel('Cuantiles muestrales')
        plt.plot(cuantiles_teoricos, cuantiles_teoricos, linestyle='-', color='red')
        plt.show()

class GeneradoraDeDatos:
    """
    Una clase para generar datos a partir de distribuciones normales y no estándar.

    Atributos:
    N (int): El número de datos a generar.
    """

    def __init__(self, N):
        """
        Inicializa la clase GeneradoraDeDatos con el número de datos a generar.

        Args:
        N (int): El número de datos a generar.
        """
        self.N = N

    def generar_datos_dist_norm(self, media, desvio):
        """
        Genera datos a partir de una distribución normal.

        Args:
        media (float): La media de la distribución.
        desvio (float): El desvío estándar de la distribución.

        Returns:
        numpy.ndarray: Datos generados a partir de una distribución normal.
        """
        return np.random.normal(loc=media, scale=desvio, size=self.N)

    def pdf_norm(self, x, media, desvio):
        """
        Calcula la función de densidad de probabilidad (PDF) de una distribución normal.

        Args:
        x (numpy.ndarray): Puntos en los que se evaluará la PDF.
        media (float): La media de la distribución.
        desvio (float): El desvío estándar de la distribución.

        Returns:
        numpy.ndarray: Valores de la PDF en los puntos x.
        """
        return norm.pdf(x, media, desvio)

    def r_BS(self):
        """
        Genera datos a partir de una distribución no estándar.

        Returns:
        numpy.ndarray: Datos generados a partir de una distribución no estándar.
        """
        u = np.random.uniform(size=(self.N,))
        y = u.copy()
        ind = np.where(u > 0.5)[0]
        y[ind] = np.random.normal(0, 1, size=len(ind))
        for j in range(5):
            ind = np.where((u > j * 0.1) & (u <= (j + 1) * 0.1))[0]
            y[ind] = np.random.normal(j/2 - 1, 1/10, size=len(ind))
            self.y = y
        return y

    def teorica_BS(self, x, media, desvio):
        """
        Calcula la función de densidad de probabilidad (PDF) teórica para una distribución no estándar.

        Args:
        x (numpy.ndarray): Puntos en los que se evaluará la PDF.
        media (float): La media de la distribución.
        desvio (float): El desvío estándar de la distribución.

        Returns:
        numpy.ndarray: Valores de la PDF teórica en los puntos x.
        """
        contribucion_estandar = norm.pdf(x, loc=media, scale=desvio) / 2  # Término 1: densidad de una normal teórica
        contribucion_adicional = 0  # Inicializar la variable antes del bucle for
        for j in range(5):
            media_adicional = (j/2) - 1
            desvio_adicional = 1 / 10
            contribucion_adicional += norm.pdf(x, loc=media_adicional, scale=desvio_adicional)

        contribucion_adicional *= (1 / 10)
        fBS_x = contribucion_estandar + contribucion_adicional
        return fBS_x

class Regresion():
    """
    Clase base para realizar regresiones.

    Atributos:
    datos (DataFrame): Conjunto de datos utilizado para la regresión.
    y (Series): Variable dependiente para la regresión.

    Métodos:
    __init__(datos, y=None): Inicializa la clase con los datos y la variable dependiente opcional.
    """
    def __init__(self, datos,y):
        self.datos = datos
        self.y = datos['y']
        self.x = datos.drop('y', axis=1)
        self.modelo = None
        self.resultados = None
        self.n = len(self.y)
        self.k = len(self.x.columns)

    def evaluar(self, X, y):
        """
        Calcula el error cuadrático medio (ECM)
        """
        predicciones = self.predecir(X)
        return ((predicciones - y) ** 2).mean()

class RegresionLineal(Regresion, ResumenGrafico):
    """
    Clase para realizar regresiones lineales.

    Hereda de:
    - Regresion: Clase base para realizar regresiones.
    - ResumenGrafico: Clase para generar gráficos resumen.

    Atributos:
    resultados (RegressionResults): Resultados del ajuste del modelo.

    Métodos:
    ajustar(): Ajusta el modelo de regresión lineal.
    predecir(x, alfa=0.05): Realiza predicciones con el modelo ajustado y devuelve intervalos de confianza y predicción.
    graficar(): Grafica la dispersión de los datos y la recta de mejor ajuste.
    calcular_coeficiente_correlacion(): Calcula los coeficientes de correlación entre las variables independientes y la variable dependiente.
    analizar_residuos(): Realiza un análisis de los residuos del modelo ajustado.
    varianza_res(): Calcula la varianza residual del modelo ajustado.
    estadisticas(): Devuelve estadísticas del modelo ajustado.
    """
    def ajustar(self):
        """
        Ajusta el modelo de regresión lineal.

        Agrega una constante a las variables independientes y ajusta un modelo OLS.
        Retorna:
        self.resultados (RegressionResults): Resultados del ajuste del modelo.
        """
        X = sm.add_constant(self.x)
        self.modelo = sm.OLS(self.y, X)
        self.resultados = self.modelo.fit()
        self.scale = self.varianza_res()
        self.ssr = self.calcular_ssr()
        self.df_resid = self.n - self.k
        return self.resultados

    def predecir(self,x, alfa = 0.05):
      """
        Realiza predicciones con el modelo ajustado.

        Parámetros:
        x (DataFrame): Datos para realizar la predicción.
        alfa (float): Nivel de significancia para los intervalos de confianza y predicción. Por defecto es 0.05.

        Retorna:
        diccionario_pred (dict): Diccionario con el resultado de la predicción, el intervalo de confianza y el intervalo de predicción.
      """
      if self.resultados is None:
            raise Exception("El modelo debe ser ajustado antes de calcular intervalos.")
      X_prediccion = np.inter(x,0,1)
      prediccion = self.resultados.get_prediction(X_prediccion)
      diccionario_pred ={
        'Resultado_predicion':prediccion.predicted_mean,
        'intervalo_confianza':prediccion.conf_int(alfa),
        'intervalo_prediccion':prediccion.conf_int(obs=True, alpha = alfa)
        }
      return diccionario_pred

    def graficar(self):
        """
        Grafica la dispersión de los datos y la recta de mejor ajuste.

        Genera gráficos de dispersión para cada variable independiente junto con la recta de mejor ajuste.
        """
        if self.resultados is None:
            raise Exception("El modelo debe ser ajustado antes de graficar la dispersión y la recta.")
        for columna in self.x.columns:
            plt.figure(figsize=(10, 6))
            plt.scatter(x=self.x[columna], y=self.y, label='Datos')
            X_const = sm.add_constant(self.x[columna])
            predicciones = sm.OLS(self.y, X_const).fit().predict(X_const)
            plt.plot(self.x[columna], predicciones, color='red', label='Recta de mejor ajuste')
            plt.title(f'Dispersión y recta de mejor ajuste para {columna}')
            plt.xlabel(columna)
            plt.ylabel('Respuesta')
            plt.show()
        return

    def calcular_coeficiente_correlacion(self):
        """
        Calcula los coeficientes de correlación entre las variables independientes y la variable dependiente.

        Retorna:
        correlaciones (dict): Diccionario con los coeficientes de correlación.
        """
        if self.resultados is None:
            raise Exception("El modelo debe ser ajustado antes de calcular los coeficientes de correlación.")
        correlaciones = {}
        for columna in self.x.columns:
            correlacion = self.x[columna].corr(self.y)
            correlaciones[columna] = correlacion
        return correlaciones

    def analizar_residuos(self):
        """
        Realiza un análisis de los residuos del modelo ajustado.

        Genera gráficos de residuos vs. valores predichos y un gráfico Q-Q de los residuos.
        """
        if self.resultados is None:
            raise Exception("El modelo debe ser ajustado antes de realizar el análisis de residuos.")
        self.residuos = self.resultados.resid
        predicciones = self.resultados.fittedvalues


        plt.figure(figsize=(10, 6))
        plt.plot(x=predicciones, y=self.residuos)
        plt.axhline(0, color='red', linestyle='--')
        plt.title('Residuos vs. Valores predichos')
        plt.xlabel('Valores predichos')
        plt.ylabel('Residuos')
        plt.show()

        # Gráfico Q-Q
        ResumenGrafico.mi_qqplot(self.residuos)
        plt.title('Gráfico Q-Q de los residuos')
        plt.show()
    def varianza_res(self):
        """
        Calcula la varianza residual del modelo ajustado.

        Retorna:
        varianza_res (float): Varianza residual.
        """
        if self.resultados is None:
            raise Exception("El modelo debe ser ajustado antes de calcular la varianza residual.")
        varianza_res = self.resultados.mse_resid
        return varianza_res
    def calcular_ssr(self):
        """
        Calcula el SSR (Sum of Squares of Residuals) del modelo ajustado.

        Retorna:
        ssr (float): SSR.
        """
        if self.resultados is None:
            raise Exception("El modelo debe ser ajustado antes de calcular el SSR.")
        ssr = self.resultados.ssr
        return ssr

    def estadisticas(self):
        """
        Devuelve estadísticas del modelo ajustado.

        Retorna:
        dict: Diccionario con los betas, errores estándar, t_obs, p_valores y el summary del modelo ajustado.
        """
        if self.resultados is None:
            raise Exception("El modelo debe ser ajustado antes de obtener las estadísticas.")
        summary = self.resultados.summary2().tables[1]
        betas = self.resultados.params
        errores_estandar = self.resultados.bse
        t_obs = self.resultados.tvalues
        p_valores = self.resultados.pvalues
        return {
            'betas': betas,
            'errores_estandar': errores_estandar,
            't_obs': t_obs,
            'p_valores': p_valores,
            'summary': summary
        }

    def calcular_coeficientes_determinacion(self):
        """
        Calcula los coeficientes de determinación del modelo ajustado.

        Retorna:
        dict: Diccionario con los coeficientes de determinación R2 y R2_ajustado.
        """
        if self.resultados is None:
            raise Exception("El modelo debe ser ajustado antes de calcular los coeficientes de determinación.")
        r2 = self.resultados.rsquared
        r2_ajustado = self.resultados.rsquared_adj
        return {'R2': r2, 'R2_ajustado': r2_ajustado}

class RegresionLogistica(Regresion):
    """
    Clase para realizar regresiones logísticas.

    Hereda de:
    - Regresion: Clase base para realizar regresiones.

    Atributos:
    X_train (DataFrame): Conjunto de datos de entrenamiento para las variables independientes.
    X_test (DataFrame): Conjunto de datos de prueba para las variables independientes.
    y_train (Series): Conjunto de datos de entrenamiento para la variable dependiente.
    y_test (Series): Conjunto de datos de prueba para la variable dependiente.
    X (DataFrame): Variables independientes del conjunto de datos.

    Métodos:
    __init__(datos): Inicializa la clase con los datos y divide el conjunto de datos en variables independientes y dependiente.
    dividir_data(test_size=0.2, seed=None): Divide los datos en conjuntos de entrenamiento y prueba.
    ajustar(): Ajusta el modelo de regresión logística.
    predecir_proba(X): Realiza predicciones de probabilidad con el modelo ajustado.
    predecir(X, umbral=0.5): Realiza predicciones binarias con el modelo ajustado.
    obtener_estadisticas_modelo(): Devuelve estadísticas del modelo ajustado.
    evaluar_modelo(umbral=0.5): Evalúa el modelo utilizando una matriz de confusión y calcula métricas de rendimiento.
    graficar_curva_roc(): Genera y grafica la curva ROC del modelo ajustado.
    """
    def __init__(self, datos):
        super().__init__(datos,datos['y'])
        self.X_train, self.X_test, self.y_train, self.y_test = None, None, None, None
        self.X = datos.drop('y', axis=1)

    def dividir_data(self,test_size = 0.2, seed = None):
        """
        Divide los datos en conjuntos de entrenamiento y prueba.

        Parámetros:
        test_size (float): Proporción del conjunto de prueba. Por defecto es 0.2.
        seed (int): Semilla para el generador de números aleatorios. Por defecto es None.

        Retorna:
        tuple: Conjunto de entrenamiento y prueba para las variables dependiente e independientes.
        """
        if seed is not None:
            random.seed(seed)
        n = len(self.X)
        n_train = int(n * (1 - test_size))
        cuales = random.sample(range(n), n_train)
        datos_train = self.datos.iloc[cuales]
        datos_test = self.datos.drop(cuales)
        self.y_train = datos_train['y']
        self.y_test = datos_test['y']
        self.X_train = datos_train.drop('y', axis=1)
        self.X_test = datos_test.drop('y', axis=1)

        return self.y_train, self.y_test, self.X_train, self.X_test

    def ajustar(self):
        """
        Ajusta el modelo de regresión logística.

        Agrega una constante a las variables independientes y ajusta un modelo Logit.
        """
        if self.X_train is None or self.y_train is None:
            raise Exception("Los datos de entrenamiento deben ser divididos antes de ajustar el modelo.")
        X_const = sm.add_constant(self.X_train)
        self.modelo = sm.Logit(self.y_train, X_const)
        self.resultados = self.modelo.fit()
        return self.resultados

    def predecir_proba(self, X):
        """
        Realiza predicciones de probabilidad con el modelo ajustado.

        Parámetros:
        X (DataFrame): Conjunto de datos para realizar la predicción.

        Retorna:
        np.array: Predicciones de probabilidad.
        """
        if self.resultados is None:
            raise Exception("El modelo debe ser ajustado antes de hacer predicciones.")
        X_const = sm.add_constant(pd.DataFrame(X))
        return self.resultados.predict(X_const)

    def predecir(self, X, umbral=0.5):
        """
        Realiza predicciones binarias con el modelo ajustado.

        Parámetros:
        X (DataFrame): Conjunto de datos para realizar la predicción.
        umbral (float): Umbral para la clasificación binaria. Por defecto es 0.5.

        Retorna:
        np.array: Predicciones binarias.
        """
        proba = self.predecir_proba(X)
        return (proba >= umbral).astype(int)

    def obtener_estadisticas_modelo(self):
        """
        Devuelve estadísticas del modelo ajustado.

        Retorna:
        dict: Diccionario con los betas, errores estándar, t_obs, p_valores y el summary del modelo ajustado.
        """
        if self.resultados is None:
            raise Exception("El modelo debe ser ajustado antes de obtener las estadísticas.")
        summary = self.resultados.summary2().tables[1]
        betas = self.resultados.params
        errores_estandar = self.resultados.bse
        t_obs = self.resultados.tvalues
        p_valores = self.resultados.pvalues
        return {
            'betas': betas,
            'errores_estandar': errores_estandar,
            't_obs': t_obs,
            'p_valores': p_valores,
            'summary': summary
        }

    def evaluar_modelo(self, umbral=0.5):
        """
        Evalúa el modelo utilizando una matriz de confusión y calcula métricas de rendimiento.

        Parámetros:
        umbral (float): Umbral para la clasificación binaria. Por defecto es 0.5.

        Retorna:
        dict: Diccionario con la matriz de confusión
        """
        if self.resultados is None:
            raise Exception("El modelo debe ser ajustado antes de evaluar el modelo.")
        predicciones = self.predecir(self.X_test, umbral)
        matriz_confusion = confusion_matrix(self.y_test, predicciones)
        d, b,c, a = matriz_confusion.ravel()
        error_total = (b + c) / (d + b + c + a)
        sensibilidad = a / (a + c)
        especificidad = d / (d + b)
        tabla =  pd.DataFrame({
    'y_test=1': [a , c],
    'y_test=0': [b, d],

}, index=['y_pred=1', 'y_pred=0'])
        return {
            'matriz_confusion': tabla,
            'error_total': error_total,
            'sensibilidad': sensibilidad,
            'especificidad': especificidad
        }

    def graficar_curva_roc(self):
        """
        Genera y grafica la curva ROC del modelo ajustado.

        Retorna:
        AUC
        """
        if self.resultados is None:
            raise Exception("El modelo debe ser ajustado antes de graficar la curva ROC.")
        proba_pred = self.predecir_proba(self.X_test)

        tfp, tvp, umbrales = roc_curve(self.y_test, proba_pred) #tfp: Tasa de Falsos Positivos, tvp: Tasa de Verdaderos Positivos
        auc = roc_auc_score(self.y_test, proba_pred)

        plt.figure(figsize=(10, 6))
        plt.plot(tfp, tvp, color='blue', label=f'ROC curve (AUC = {auc:.2f})')
        plt.plot([0, 1], [0, 1], color='red', linestyle='--')
        plt.xlabel('Tasa de Falsos Positivos')
        plt.ylabel('Tasa de Verdaderos Positivos')
        plt.title('Curva ROC')
        plt.legend(loc='lower right')
        plt.show()

        return auc


class ChiCuadrado:
    """
    Clase para realizar el test de Chi-cuadrado.

    Métodos:
    - test: Realiza el test de Chi-cuadrado para los datos observados y las probabilidades esperadas.
    """

    def __init__(self, datos=None):
        """
        Inicializa la clase con los datos.

        Parámetros:
        - datos (array-like): Datos de entrada.
        """
        if datos is not None:
            self.datos = np.array(datos)

    def test(self, val_obs, prob, alfa):
        """
        Realiza el test de Chi-cuadrado para los datos observados y las probabilidades esperadas.

        Parámetros:
        - val_obs (array-like): Valores observados.
        - prob (array-like): Probabilidades esperadas.
        - alfa (float): Nivel de significancia.

        Prints:
        - Estadístico observado y teórico, p-valor y conclusión del test.
        """
        n = sum(val_obs)
        val_esp = [p * n for p in prob]
        resta = [val_obs[i] - val_esp[i] for i in range(len(val_obs))]
        X_obs = sum(resta[i] ** 2 / val_esp[i] for i in range(len(val_esp)))
        gf = len(prob) - 1
        X_teo = chi2.ppf(1 - alfa, gf)
        p_valor = 1 - chi2.cdf(X_obs, gf)
        print('Estadístico observado:', X_obs)
        print('Estadístico teórico:', X_teo)
        print('p-valor:', p_valor)
        if p_valor > alfa and X_obs < X_teo:
            print('No hay evidencia suficiente para rechazar la hipótesis nula')
        elif p_valor <= alfa and X_obs >= X_teo:
            print('Hay evidencia suficiente para rechazar la hipótesis nula')
        else:
            print('Hay un error, no hay congruencia entre los resultados obtenidos')