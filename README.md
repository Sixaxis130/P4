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
 
  Dentro de este script encontramos como usar el wav2lp.sh, este mismo requiere de una señal .wav de entrada y que nos devuelve un archivo output.lp.
  Como comentamos en la sesion de laborarorio, en el script wa2lp.sh vemos que se eliminan los ficheros temporales previamente al hacer la parametrización de la señal .wav. En este caso utilizamos lo hacemos a través del calculo de los coeficientes de predición lineal (LPC). 
  
  <img width="427" alt="Captura de Pantalla 2021-12-07 a les 12 18 27" src="https://user-images.githubusercontent.com/91251152/145019899-030203c2-3c96-4e57-95e2-c9acef4ccd40.png">

  Acto seguido, declaramos los parámetros que el usuario tendrá que introducir en el momento en que se invoque dicho script. En este caso los parámetros importantes son el número de coeficientes de prediccion lineal (LPC), los ficheros de entrada y salida que queremos utilizar en el proceso. Guardamos tanto en $1, como en $2, y en $3 los parámetros especificados en orden pasados per la terminal introducidos por el usuario. El $0 no lo usamos para evitar posibles problemas debido a que se suele definir como el propio nombre del script al ser el primer argumento de todos. Más adelante, en función del valor de la variable de entorno UBUNTU_SPTK, especificamos como se invocan los programas y los comandos del paquete de código SPTK.
  
    <img width="592" alt="Captura de Pantalla 2021-12-07 a les 12 25 58" src="https://user-images.githubusercontent.com/91251152/145020931-8274b798-ceb3-4940-8e12-50c1338844cc.png">
    
    Una vez especificados los parámetros que el usuario deberá escribir en la linea de comandos, pasamos a la función principal del script wav2lp.sh. Con el pipeline principal conseguimos una correcta extracción de las caracteristicas de la señal debido a los programas especificados justo en el paso anterior. El pipeline principal es el que mostramos a continuacion:
    
    <img width="941" alt="Captura de Pantalla 2021-12-07 a les 12 28 29" src="https://user-images.githubusercontent.com/91251152/145021262-5bb3d1a0-325b-4bf8-a15d-550ddaadd6f8.png">

 
    Como comentamos en la sesión de laboratorio, en la primera pipeline el sox nos permite convertir la entrada (formato de ley mu) a enteros de 16 bits con signo. Este paso es fundamental porque los ficheros .wav estan codificados con la ley mu y la parametrización con SPTK solo es capaz de leer señales tipo float4, siendo crucial este cambio para su correcta lectura.
    
    Con la siguiente pipeline conseguimos convertir los datos del archivo de entrada. Después de este paso, utilizando las diferentes opciones que nos ofrece el "X2X", obteniendo en formato de enteros con signo de 2 bytes usando (+s) para luego pasarlo a float de 4 bytes mediante (+f).
    
    En la siguiente pipeline usamos el programa "FRAME", este programa nos permite estructurar la ventana de extracción de datos de una secuencia. Como vimos en la sesion de laboratorio en este caso nos interesaria  elegir una ventana de 30ms y con frecuencia de muestreo de 8000Hz (perteneciente a una ventana de 240 muestras). Además hemos añadido un desplazaminento de 10ms entre las ventanas, es decir, 80 muestras.
    
    En la penúltima pipeline usamos el programa "WINDOW" con el objetivo de enventanar la señal. En primer lugar, determinamos el número de muestras que entran, que sabemos que son 240 ya que lo hemos configurado previamente en la pipeline. Por último determinamos la longitud de salida.

    Para acabar usamos el programa "LPC" con el que determinamos el número de muestras y el número de coeficientes LPC en base a su orden.
    
    
- Explique el procedimiento seguido para obtener un fichero de formato *fmatrix* a partir de los ficheros de
  salida de SPTK (líneas 45 a 47 del script `wav2lp.sh`).
  
  <img width="943" alt="Captura de Pantalla 2021-12-07 a les 12 44 47" src="https://user-images.githubusercontent.com/91251152/145023416-b244e4f3-f9ae-412c-89af-6367b3ff90b3.png">
  
  El objetivo que tenemos es obtener el número de columnas de la matriz, para ello especificamos el orden que es el numeros de coeficientes del LPC. Además hemos de tener en cuenta una unidad extra debido a que el primer valor se corresponde con la ganancia. Utilizamos el comando perl con el propósito de calcular el número de filas. 
  
  Lo primero que hacemos es pasar el contenido de nuestros archivos temporales, siendo un conjunto de floats de 4 bytes concatenados a formato ASCII. De esta manera se genera un archivo con un valor ASCII en cada una de las lineas que podemos extraer con el comando "wc -l", obteniendo asi el numero de lineas del archivo. Gracias a lo anterior mencionado obtenemos la cantidad de valores que tenía nuestro fichero temporal. Si conociesemos el numero de columnas podriamos obtener la cantidad de filas de la matriz, al hacer es una división de la cantidad de datos totales entre el numero de columnas.

  * ¿Por qué es conveniente usar este formato (u otro parecido)? Tenga en cuenta cuál es el formato de
    entrada y cuál es el de resultado.
    
    Es conveniente usar este formato, en el cual hemos pasado de una señal .wav codificada con la ley mu de 8 bits a el formato fmatrix permitiendonos obtener las señales ordenadas y caracterizadas por tramas y coeficientes. De esta manera, cada columna corresponde a los coeficientes con los que hemos parametrizado la trama y las filas hacen referencia a las tramas de senñal. Además, este formato nos permite trabajar con los datos de manera más sencilla y comoda al poder seleccionar columnas en especifico de los ficheros que queramos, esto se hace mediante los programas "fmatrix_show" y "fmatrix_cut". 


- Escriba el *pipeline* principal usado para calcular los coeficientes cepstrales de predicción lineal
  (LPCC) en su fichero <code>scripts/wav2lpcc.sh</code>:
  
  <img width="946" alt="Captura de Pantalla 2021-12-07 a les 13 01 28" src="https://user-images.githubusercontent.com/91251152/145025586-634aa3a5-c917-4307-af5c-aef7000c7063.png">

  Para ello, hemos hecho uso de la plantilla wav2lp.sh para crear el script wav2lpcc.sh, este mismo lo incluimos en el script meson.build para luego compilar el programa y tenerlo incluido. Como podemos apreciar, la pipeline principal de la parametrización LPCC sigue la misma forma que la parametrización hecha previamente. Aunque con la diferencia que ahora hay que tener en cuenta que para encontrar los coeficientes cepstrales antes necesitamos sacar los coeficientes LPC. Por este motivo, antes de pasar los datos de la parametrización cepstral al archivo .lpcc, tenemos que sacar los coeficientes LPC con el comando "lpc". Finalmente utilizamos el comando "lpcc" para obtener los coeficientes LPCC.

- Escriba el *pipeline* principal usado para calcular los coeficientes cepstrales en escala Mel (MFCC) en su
  fichero <code>scripts/wav2mfcc.sh</code>:
  
  <img width="946" alt="Captura de Pantalla 2021-12-07 a les 13 08 06" src="https://user-images.githubusercontent.com/91251152/145026431-8e3feeaf-3f6a-4d06-b93a-e93fe7562f08.png">

  Aplicando los mismos pasos que en el caso anterior pero ahora buscando los coeficientes Mel-cepstrum, utilizamos el comando "mfcc". En este comando especificamos el número de coeficientes y también el banco de filtros que utilizaremos.

### Extracción de características.


- Inserte una imagen mostrando la dependencia entre los coeficientes 2 y 3 de las tres parametrizaciones
  para todas las señales de un locutor.
  
  <img width="639" alt="Captura de Pantalla 2021-12-07 a les 13 10 17" src="https://user-images.githubusercontent.com/91251152/145026703-fc5c81cc-622a-440f-93ce-27a53ce089ad.png">

   <img width="650" alt="Captura de Pantalla 2021-12-07 a les 13 10 30" src="https://user-images.githubusercontent.com/91251152/145026730-88cf5be9-e82a-4638-bcb4-29ff4280dd9d.png">
   
  <img width="602" alt="Captura de Pantalla 2021-12-07 a les 13 11 22" src="https://user-images.githubusercontent.com/91251152/145026820-c70d2eae-02c9-4192-8a7f-bf9c91c257b4.png">

  
  + Indique **todas** las órdenes necesarias para obtener las gráficas a partir de las señales 
    parametrizadas.
    
    Si nos fijamos en como está estructurada la fmatrix vemos que las columnas cuarta y quinta nos dan la informacion del segundo y el tercer coeficiente.
    
    <img width="1018" alt="Captura de Pantalla 2021-12-07 a les 13 14 41" src="https://user-images.githubusercontent.com/91251152/145027251-f7bbedec-5fbe-42df-99a7-174fa4e12f62.png">

    
  + ¿Cuál de ellas le parece que contiene más información?

  Como podemos apreciar en las gráficas generadas anteriormente los coeficientes de las parametrizaciones MFCC y LPCC son mucho más dispersas, en consecuencia los coeficientes de MFCC y LPCC son más incorrelados que los LP. Además, observamos una distribución más o menos lineal en el caso de la parametrización LP. Así pues, la que contiene más información de las 3, es decir, la que es menos redundante y presenta mayor entropía es la parametrización MFCC.

- Usando el programa <code>pearson</code>, obtenga los coeficientes de correlación normalizada entre los
  parámetros 2 y 3 para un locutor, y rellene la tabla siguiente con los valores obtenidos.
  
  Usamos el programa <code>pearson</code> para obtener los .txt:
  
  <img width="1008" alt="Captura de Pantalla 2021-12-07 a les 13 19 25" src="https://user-images.githubusercontent.com/91251152/145027867-acfe7242-948f-49f9-947b-e88e0193ecb8.png">

  Extraemos el coeficiente de correlación Pearson a partir de los ficheros que obtenemos. 
  
  Para los coeficientes de predicción lineal (LP):
  
  <img width="312" alt="Captura de Pantalla 2021-12-07 a les 13 21 00" src="https://user-images.githubusercontent.com/91251152/145028057-0a19ee89-8345-46fc-9afc-86e285c355a1.png">

  Para los coeficientes cepstrales (LPCC):
  
  <img width="315" alt="Captura de Pantalla 2021-12-07 a les 13 21 53" src="https://user-images.githubusercontent.com/91251152/145028158-7c4bf9ab-f5c1-442b-8897-8d64bdfec842.png">

  Para los coeficientes Mel-cepstrales (MFCC):
  
  <img width="313" alt="Captura de Pantalla 2021-12-07 a les 13 22 07" src="https://user-images.githubusercontent.com/91251152/145028196-f359b798-8c5a-4445-81e6-d9f7367de39c.png">

   
 Obtenemos la siguiente tabla:

  |                        | LP   | LPCC | MFCC |
  |------------------------|:----:|:----:|:----:|
  | &rho;<sub>x</sub>[2,3] |   -0.666745    |   0.303116   |   0.0588095   |
  
  + Compare los resultados de <code>pearson</code> con los obtenidos gráficamente.

Observamos que los coeficientes LPCC y MFCC que hemos visto eran los mas incorrelados, siendo los que tienen un coeficiente Pearson más cercano al 0. Sin embargo, los coeficientes LP los cuales eran  más correlados tienen un coeficiente de correlación Pearson más alejado del 0. Estos resultados que estamos comentando son razonables, ya que un valor cercano a -1 o +1 implica una elevada correlación entre componentes, permitiendonos estimar el valor de uno en función del otro. Mientras que un valor cercano a 0 implica que las componentes estan más incorreladas.

  
- Según la teoría, ¿qué parámetros considera adecuados para el cálculo de los coeficientes LPCC y MFCC?

Como hemos estudiado en la teoría de la asignatura, para el caso de los LPCC se aconseja trabajar con un orden de 13 coeficientes. Para los MFCC se recomienda usar entre 24 y 40 filtros del banco de mel, y unos 13 coeficientes Mel-Ceptrales. A partir de los 20 coeficientes, la información proporcionada por los coeficientes podría confundir al sistema de reconocimiento de voz dando posibilidad a errores.

### Entrenamiento y visualización de los GMM.

Complete el código necesario para entrenar modelos GMM.

- Inserte una gráfica que muestre la función de densidad de probabilidad modelada por el GMM de un locutor
  para sus dos primeros coeficientes de MFCC.
  
  <img width="562" alt="Captura de Pantalla 2021-12-10 a les 9 42 16" src="https://user-images.githubusercontent.com/91251152/145543916-f52fe893-792c-430c-8941-a46972268cc8.png">
  
  Hemos obtenido la gráfica con el siguiente comando:
  
  <img width="850" alt="Captura de Pantalla 2021-12-10 a les 9 45 49" src="https://user-images.githubusercontent.com/91251152/145544436-13cefd35-b8db-4ae2-a1d4-8debb1fe8d93.png">


- Inserte una gráfica que permita comparar los modelos y poblaciones de dos locutores distintos (la gŕafica
  de la página 20 del enunciado puede servirle de referencia del resultado deseado). Analice la capacidad
  del modelado GMM para diferenciar las señales de uno y otro.
  
  Ahora representamos la GMM con las muestras del locutor al que corresponde con el siguiente comando:
  
 <img width="850" alt="Captura de Pantalla 2021-12-10 a les 9 47 34" src="https://user-images.githubusercontent.com/91251152/145544776-fde450d6-cf5d-4d24-9595-83492ce06fb1.png">
 
 Obtenemos la gráfica siguiente:
 
 <img width="593" alt="Captura de Pantalla 2021-12-10 a les 9 50 29" src="https://user-images.githubusercontent.com/91251152/145545203-aa3efb6f-a5de-4886-a887-e736aa038f0c.png">
 
 
 A continuación representamos la GMM anterior con las muestras de un nuevo locutor al que no corresponde con el siguiente comando:
 
 <img width="1003" alt="Captura de Pantalla 2021-12-10 a les 9 57 45" src="https://user-images.githubusercontent.com/91251152/145546304-be7b92eb-2a87-413b-83ca-d677d04c3d98.png">
 
 Obtenemos la gráfica siguiente:
 
 <img width="602" alt="Captura de Pantalla 2021-12-10 a les 9 59 07" src="https://user-images.githubusercontent.com/91251152/145546507-e585897a-ee64-4fce-8148-411bf9f6c279.png">

Comparanando las dos gráficas de las GMM, observamos con claridad que la primera gráfica modela mucho mejor al locutor que la segunda gráfica.

Ahora lo hacemos con otro mas diferente para tener varios ejemplos:

<img width="866" alt="Captura de Pantalla 2021-12-10 a les 10 02 19" src="https://user-images.githubusercontent.com/91251152/145546936-c8ed82da-e3eb-4554-8a6d-ad647d58d5a4.png">

<img width="615" alt="Captura de Pantalla 2021-12-10 a les 10 03 28" src="https://user-images.githubusercontent.com/91251152/145547091-513efed4-896e-4cde-938c-7a9dbd8faa9b.png">

### Reconocimiento del locutor.

Complete el código necesario para realizar reconociminto del locutor y optimice sus parámetros.

- Inserte una tabla con la tasa de error obtenida en el reconocimiento de los locutores de la base de datos
  SPEECON usando su mejor sistema de reconocimiento para los parámetros LP, LPCC y MFCC.

Hemos usado 8 coeficientes LP, 13 coeficientes LPCC, 16 coeficientes MFCC y 24 filtros del banco de filtros.

tasa error lp:

<img width="818" alt="Captura de Pantalla 2021-12-10 a les 10 06 19" src="https://user-images.githubusercontent.com/91251152/145547514-ee37a8f9-fc52-42ef-bcaa-5864198a9ddf.png">

tasa error lpcc:

<img width="682" alt="Captura de Pantalla 2021-12-10 a les 10 06 35" src="https://user-images.githubusercontent.com/91251152/145547546-6044dbd1-b59a-4fe1-87f9-26eddd11c85e.png">

tasa error mfcc:

<img width="681" alt="Captura de Pantalla 2021-12-10 a les 10 06 53" src="https://user-images.githubusercontent.com/91251152/145547590-7d38aeac-2a3b-48dc-a297-c687d7e478ac.png">


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
