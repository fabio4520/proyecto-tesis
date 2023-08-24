# Documentación del Proyecto de Tesis
Este documento proporciona una descripción detallada de los archivos clave de un proyecto de tesis que utiliza la librería Mediapipe para detectar puntos de referencia de la mano y controlar un servomotor en base a esos puntos.

## Archivo: functions.py
### Descripción
Este archivo contiene funciones reutilizables que se utilizan en el proyecto para cálculos y dibujos relacionados con la detección de mano y el control del servomotor.

### Funciones
`rotateservo(pin, angle, board)`

Esta función controla un servomotor conectado a una placa Arduino. Toma como argumentos el pin del servomotor, el ángulo al que se debe girar el servomotor y la placa Arduino a la que está conectado. Utiliza el módulo pyfirmata para realizar la rotación.

`calculate_landmark_list(hand_landmarks)`

Esta función toma como entrada un objeto hand_landmarks que representa los puntos de referencia de la mano detectados por Mediapipe. Devuelve una lista de coordenadas (x, y) redondeadas de los puntos de referencia.

`calc_bounding_rect(image, landmarks)`

Esta función calcula un rectángulo delimitador alrededor de los puntos de referencia de la mano detectados. Toma como argumentos una imagen y los puntos de referencia de la mano. Devuelve las coordenadas (x, y, x + w, y + h) del rectángulo.

`draw_bounding_rect(image, brect)`

Esta función dibuja un rectángulo delimitador en una imagen. Toma como argumentos una imagen y las coordenadas (x, y, x + w, y + h) del rectángulo. Devuelve la imagen con el rectángulo dibujado.

`draw_info_text(image, frame, brect, handedness, hand_landmarks, wrist_x, wrist_y)`

Esta función dibuja información relacionada con la mano en la imagen, como si es izquierda o derecha, y las coordenadas de los puntos de referencia. Toma como argumentos la imagen, el cuadro de referencia, el resultado de la detección de la mano, los puntos de referencia de la mano y las coordenadas de la muñeca. Devuelve la imagen con la información dibujada.

## Archivo: tesis.py
### Descripción
Este archivo es la parte principal del proyecto y utiliza las funciones definidas en functions.py para detectar puntos de referencia de la mano y controlar un servomotor en base a esos puntos.

### Desarrollo del Programa
1. Importa las bibliotecas necesarias, como cv2, mediapipe, copy, math y pyfirmata.

2. Establece la conexión con un Arduino utilizando el puerto COM especificado. Define el pin del servomotor del pulgar.

3. Define los valores máximos y mínimos de distancia permitidos para cada dedo con respecto a la muñeca.

4. Define una función principal llamada main() que realiza lo siguiente:
    * Inicializa la detección de manos utilizando la librería Mediapipe.
    * Captura video en tiempo real utilizando la cámara.
    * Procesa cada cuadro:
      * Calcula las distancias entre los puntos de referencia de los dedos y la muñeca.
      * Normaliza las distancias según los valores máximos y mínimos permitidos.
      * Controla el servomotor del pulgar en función de las distancias normalizadas.
      * Dibuja los resultados en la imagen del cuadro.
    * Muestra la imagen procesada en una ventana y espera la tecla 'q' para salir.
5. Si el archivo se ejecuta directamente, llama a la función main() para iniciar el proceso de control del servomotor en tiempo real.

## Uso
Para ejecutar el proyecto, asegúrate de tener las bibliotecas requeridas instaladas y de que el Arduino esté conectado correctamente. Ejecuta el archivo tesis.py y observa cómo el servomotor del pulgar se controla en función de los puntos de referencia de la mano detectados por Mediapipe.

## Instalaciones necesarias
### Arduino
Para poder correr el programa en python es necesario instalar la librería `Firmata` by Firmata Developers. La versión usada en este proyecto es 2.5.9
```cmd
Firmata v2.5.9
```

En Herramientas seleccionamos el tipo de Arduino y el puerto al que se va a conectar (Este puerto es importante también para el código en Python).
Una vez instalada la librería y seleccionado el puerto y Arduino, nos dirigimos a `Archivo -> Ejemplos -> Firmata -> StandardFirmata`. Se abrirá una nueva ventana y cargamos el archivo al arduino. Esta es toda la instalación necesaria para Arduino.


### Python
Para poder ejecutar la función en python se necesita instalar las siguientes librerías.
```cmd
pip install cv2
pip install mediapipe
pip install pyfirmata
```

Las versiones para las librerías en este proyecto son:
```
python                       3.10.0
mediapipe                    0.10.3
opencv-contrib-python        4.8.0.76
opencv-python                4.8.0.76
pip                          23.2.1
pyFirmata                    1.1.0
```
