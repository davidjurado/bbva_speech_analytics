# Reto Speech Analytics

Nuestro equipo Avengers ha desarrollado esta herramienta para detectar los motivos de las llamadas de los clientes del Banco BBVA.

Link de la herramienta [AQUI](http://jarvis.com.s3-website-us-east-1.amazonaws.com/index.html).

## Arquitectura

Para nuetra implementación utilizamos herramientas de AWS, tales como: S3, EC2, Transcibe, Sagemaker y Lambda.

![arquitectura](https://i.imgur.com/03RU9zU.png)

Nuestra aplicación web está alojda en un bucket S3 donde el usuario puede cargar un archivo de audio en formato .wav

Una función Lambda se encarga de guardar el archivo .wav en un bucket S3

Cuando un nuevo archivo llega a este bucket, otra función Lambda se ejecuta para crear un Job de transcribción de audio a texto usando Amazon Trancribe.

Este proceso es el más demorado y costoso de toda la implementación, para un audio de 10 minutos de duración el trabajo de transcribción se puede llegar a demorar hasta 3 minutos.

el reusltado del trabajo de trascribción se guarda en un S3 en formato .json, Cuando un nuevo archivo llega a este bucket, otra función Lambda se ejecuta para obtener el texto de la llamada y enviarlo a el modulo de análisis de texto.

Se usó Amazon SageMaker para entrenar multiples modelos para clasificar: Producto, Intención, Tipo de movimiento, Contexto 1, Contexto 2, Detalle y verbalización del cliente.

Los modelos se alojaron en una instancia t2.micro de EC2 donde se raliza la inferencia, este es nuestro modulo de análisis de texto al cual podemos acceder mediante una petición POST http.

Al final se guardan los resultados en el bucket que contiene la aplicación web y son mostrados en un [Dashboard](http://jarvis.com.s3-website-us-east-1.amazonaws.com/dashboard.html).

## Proyección de costos

Se usó una cuenta con acceso a la capa gratuita, para el desarrollo estos fueron las proyecciones de costos en AWS

![costos](https://i.imgur.com/85N0IfW.png)

# Integrantes

* David Fernando Jurado. [contacto](https://www.linkedin.com/in/david-fernando-jurado-blanco-69799b136/).

* Mateo Marin Echeverri [contacto](www.linkedin.com/in/mateomarinecheverri)

* Julieth Andrea López Castiblanco[contacto](https://github.com/JuliethLopez)

* Diana Isabel Torres [contacto](https://www.linkedin.com/in/dianaitr/)