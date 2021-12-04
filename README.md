PAV - P4: reconocimiento y verificación del locutor
===================================================

Obtenga su copia del repositorio de la práctica accediendo a [Práctica 4](https://github.com/albino-pav/P4)
y pulsando sobre el botón `Fork` situado en la esquina superior derecha. A continuación, siga las
instrucciones de la [Práctica 2](https://github.com/albino-pav/P2) para crear una rama con el apellido de
los integrantes del grupo de prácticas, dar de alta al resto de integrantes como colaboradores del proyecto
y crear la copias locales del repositorio.

También debe descomprimir, en el directorio `PAV/P4`, el fichero [db_8mu.tgz](https://atenea.upc.edu/pluginfile.php/3145524/mod_assign/introattachment/0/spk_8mu.tgz?forcedownload=1)
con la base de datos oral que se utilizará en la parte experimental de la práctica.

Como entrega deberá realizar un *pull request* con el contenido de su copia del repositorio. Recuerde
que los ficheros entregados deberán estar en condiciones de ser ejecutados con sólo ejecutar:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.sh
  make release
  run_spkid mfcc train test classerr verify verifyerr
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Recuerde que, además de los trabajos indicados en esta parte básica, también deberá realizar un proyecto
de ampliación, del cual deberá subir una memoria explicativa a Atenea y los ficheros correspondientes al
repositorio de la práctica.

A modo de memoria de la parte básica, complete, en este mismo documento y usando el formato *markdown*, los
ejercicios indicados.

## Ejercicios.

### SPTK, Sox y los scripts de extracción de características.

- Analice el script `wav2lp.sh` y explique la misión de los distintos comandos involucrados en el *pipeline*
  principal (`sox`, `$X2X`, `$FRAME`, `$WINDOW` y `$LPC`). Explique el significado de cada una de las 
  opciones empleadas y de sus valores.
 
  En este script vemos un "usage" que nos guia como se utiliza en el wav2lp.sh, que requiere de una señal .wav de entrada, y que nos devuelve un fichero salida.lp.
  Como comentamos en la sesion de laborarorio, en el script wa2lp.sh vemos que se eliminan los ficheros temporales previamente al hacer la parametrización de la señal .wav.  Si existiesen ficheros temporales asociados a la parametrización, en este caso a través del cálculo de los coeficientes de predición lineal (LPC). Tambien un "usage" que nos indica como se utiliza el script, este necesita de una señal .wav de entrada, y que devuelve un fichero salida.lp.
  
  *****captura 1******
  
  Acto seguido, declaramos los parámetros que el usuario especifique en el momento en que se invoque el script. En este caso los parámetros importantes son los fichersos de entrada y salida y el número de coeficientes de prediccion lineal (LPC) que queremos que se calculen. Guardamos tanto en $1 como $2 y $3 los parámetros especificados en orden en la terminal. El $0 no lo usamos porque es el primer argumento de todos que habitualmente suele ser el propio nombre del script. Mas adelante, en función del valor de la variable de entorno UBUNTU_SPTK, especificamos como se invocan los programas y los comandos del paquete de código SPTK.
  
    *****captura 2******
    
    Una vez especificados los parámetros que el usuario escriba en la linea de comandos, pasamos a la función principal del script wav2lp.sh. Con el pipeline principal conseguimos una correcta extracción de caracteristicas para la señal, esto es asi debido a los programas especificados justo en el paso anterior. El pipeline principal es el que mostramos a continuacion:
    
    *****captura 3******
    
    Como comentamos en la sesión de laboratorio, en la pipeline siguiente, sox nos permite convertir la entrada (formato de ley mu) a enteros de 16 bits con signo. Este paso es fundamental porque los ficheros .wav estan codificados con la ley mu, pero el paso de despues de la parametrización con SPTK solo es capaz de leer señales tipo float4.
    
    *****captura 4******
    
    En el siguiente paso es cuando conseguimos convertir definitavamente los datos del archivo de entrada. Gracias a este paso lo tenemos en formato de enteros con signo de 2 bytes (+s). Y ahora lo pasamos a float de 4 bytes (+f).
    
     *****captura 5******
    
    En la siguiente captura usamos el programa "frame", este programa nos permite estructurar la ventana de extracción de datos de una secuencia. Como vimos en la sesion de laboratorio en este caso nos interesaria  elegir una ventana de 30ms y con frecuencia de muestreo de 8000Hz (perteneciente a una ventana de 240 muestras). Además hemos añadido un desplazaminento de 10ms entre las ventanas, es decir, 80 muestras.
    
    *****captura 6******

- Explique el procedimiento seguido para obtener un fichero de formato *fmatrix* a partir de los ficheros de
  salida de SPTK (líneas 45 a 47 del script `wav2lp.sh`).

  * ¿Por qué es conveniente usar este formato (u otro parecido)? Tenga en cuenta cuál es el formato de
    entrada y cuál es el de resultado.

- Escriba el *pipeline* principal usado para calcular los coeficientes cepstrales de predicción lineal
  (LPCC) en su fichero <code>scripts/wav2lpcc.sh</code>:

- Escriba el *pipeline* principal usado para calcular los coeficientes cepstrales en escala Mel (MFCC) en su
  fichero <code>scripts/wav2mfcc.sh</code>:

### Extracción de características.

- Inserte una imagen mostrando la dependencia entre los coeficientes 2 y 3 de las tres parametrizaciones
  para todas las señales de un locutor.
  
  + Indique **todas** las órdenes necesarias para obtener las gráficas a partir de las señales 
    parametrizadas.
  + ¿Cuál de ellas le parece que contiene más información?

- Usando el programa <code>pearson</code>, obtenga los coeficientes de correlación normalizada entre los
  parámetros 2 y 3 para un locutor, y rellene la tabla siguiente con los valores obtenidos.

  |                        | LP   | LPCC | MFCC |
  |------------------------|:----:|:----:|:----:|
  | &rho;<sub>x</sub>[2,3] |      |      |      |
  
  + Compare los resultados de <code>pearson</code> con los obtenidos gráficamente.
  
- Según la teoría, ¿qué parámetros considera adecuados para el cálculo de los coeficientes LPCC y MFCC?

### Entrenamiento y visualización de los GMM.

Complete el código necesario para entrenar modelos GMM.

- Inserte una gráfica que muestre la función de densidad de probabilidad modelada por el GMM de un locutor
  para sus dos primeros coeficientes de MFCC.
  
- Inserte una gráfica que permita comparar los modelos y poblaciones de dos locutores distintos (la gŕafica
  de la página 20 del enunciado puede servirle de referencia del resultado deseado). Analice la capacidad
  del modelado GMM para diferenciar las señales de uno y otro.

### Reconocimiento del locutor.

Complete el código necesario para realizar reconociminto del locutor y optimice sus parámetros.

- Inserte una tabla con la tasa de error obtenida en el reconocimiento de los locutores de la base de datos
  SPEECON usando su mejor sistema de reconocimiento para los parámetros LP, LPCC y MFCC.

### Verificación del locutor.

Complete el código necesario para realizar verificación del locutor y optimice sus parámetros.

- Inserte una tabla con el *score* obtenido con su mejor sistema de verificación del locutor en la tarea
  de verificación de SPEECON. La tabla debe incluir el umbral óptimo, el número de falsas alarmas y de
  pérdidas, y el score obtenido usando la parametrización que mejor resultado le hubiera dado en la tarea
  de reconocimiento.
 
### Test final

- Adjunte, en el repositorio de la práctica, los ficheros `class_test.log` y `verif_test.log` 
  correspondientes a la evaluación *ciega* final.

### Trabajo de ampliación.

- Recuerde enviar a Atenea un fichero en formato zip o tgz con la memoria (en formato PDF) con el trabajo 
  realizado como ampliación, así como los ficheros `class_ampl.log` y/o `verif_ampl.log`, obtenidos como 
  resultado del mismo.
