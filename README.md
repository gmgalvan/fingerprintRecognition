# CNN para reconocimiento de huellas dactilares
Este proyecto fue desarrollado durante la 2da edición de Saturdays.AI Guadalajara

Proyecto para el reconocimiento de huellas de cuerpos postmortem y validación de huella dentro de base de datos mysql.

## Instalación

Usar entorno virtual con python 3.7, Linux Ubuntu.

* numpy
* matplotlib
* keras
* sklearn
* imgaug
* pymysql
* paramiko
* sshtunnel
* PIL

## Como usar

1. Agregar variables de entorno para conexion con instancia de base de datos mysql:

```bash
export SQL_HOSTNAME=<>
export SQL_USERNAME=<>
export SQL_PASSWORD=<>
export DB=<>
export DB_PORT=<>
export SSH_HOST=<>
export SSH_USER=<>
export SSH_PORT=<>
```

2. Se establece el path cambiando la linea 14 de train_fingerprint.py

3. En fingerprint_db se cambia linea 31 y 38 con la tabla correspondiente.

4. Cambiar el nombre de las columnas en las querys

5. Conexión:
```python
python fingerprint_db.py 
```

6. Entrenamiento:
```python
python train_fingerprint.py
```

## Descripción
El modelo es una red neuronal convulocional que se entrno con 1k imagenes reales y 3k generados de forma aumentada. La base de datos no es de uso público y es necesario que el dataset que se utilice tenga el formato wsq. 

![data](https://github.com/gmgalvan/fingerprintRecognition/blob/master/Imagenes/Figure%202020-07-02%20184016.png)
![data](https://github.com/gmgalvan/fingerprintRecognition/blob/master/Imagenes/Figure%202020-07-02%20184100.png)

### La arquitectura de la red
```
Layer (type)                    Output Shape         Param #     Connected to                     
==================================================================================================
input_4 (InputLayer)            (None, 90, 90, 1)    0                                            
__________________________________
input_5 (InputLayer)            (None, 90, 90, 1)    0                                            
__________________________________
model_3 (Model)                 (None, 22, 22, 32)   9568        input_4[0][0]                    
                                                                 input_5[0][0]                    
__________________________________
subtract_2 (Subtract)           (None, 22, 22, 32)   0           model_3[1][0]                    
                                                                 model_3[2][0]                    
__________________________________
conv2d_6 (Conv2D)               (None, 22, 22, 32)   9248        subtract_2[0][0]                 
__________________________________
max_pooling2d_6 (MaxPooling2D)  (None, 11, 11, 32)   0           conv2d_6[0][0]                   
__________________________________
flatten_2 (Flatten)             (None, 3872)         0           max_pooling2d_6[0][0]            
__________________________________
dense_3 (Dense)                 (None, 64)           247872      flatten_2[0][0]                  
__________________________________
dense_4 (Dense)                 (None, 1)            65          dense_3[0][0]                    
==================================================================================================
Total params: 266,753
Trainable params: 266,753
Non-trainable params: 0
__________________________________
```

## Resultados
La salida del modelo es la imagen original con su etiqueta en el lado izquierdo, en el centro la imagen con mayor porcentage de parentesco y en la derecha una imagen con menor parentesco.

![data](https://github.com/gmgalvan/fingerprintRecognition/blob/master/Imagenes/Figure%202020-07-02%20184117.png)
![data](https://github.com/gmgalvan/fingerprintRecognition/blob/master/Imagenes/Figure%202020-07-02%20184126.png)
![data](https://github.com/gmgalvan/fingerprintRecognition/blob/master/Imagenes/Figure%202020-07-02%20184151.png)

## Publicación 
Hemos escrito un artículo en Medium sobre nuestra experiencia en el curso y detalles de la realización del proyecto en Medium: [Parte 1](https://medium.com/saturdays-ai/ai-fingerprint-recognition-inteligencia-artificial-para-reconocimiento-de-cuerpos-post-mortem-210e1e25dd4) [Parte 2](https://medium.com/saturdays-ai/parte-ii-ai-fingerprint-recognition-inteligencia-artificial-para-reconocimiento-de-cuerpos-1a33ea32a192)


## Créditos
El código que fue generado durante el proyecto está basado en [fingerprint_recognition](https://github.com/kairess/fingerprint_recognition)

