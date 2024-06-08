# Game Design Document

## Resumen del juego

El juego es un homenaje del juego Exerion de 1983, un matamarcianos sencillo estilo arcade que además de recreativas también estuvo en ordenadores personales como MSX.

Genero: Shoot'em up estilo retro pixelado, vertical.
Audiencia: Jugadores de todas las edades, que disfruten de juegos de naves espaciales y de estilo retro, especialmente quienes jugaron en su infancia a juegos como Exerion.
Estilo de juego: El jugador maneja una nave y varias hordas de marcianos aparecen en pantalla, siendo necesario matarlos a todos para pasar a la siguiente pantalla. La dificultad aumenta progresivamente tras cada pantalla.
Otras características: Puntuación y tabla de puntuaciones al estilo de las recreativas clásicas.

## Estilo visual

El estilo visual del juego es pixelado, los marcianos serán los mismos assets que el juego Exerion del que nos inspiramos.

Nota: Debido a que se reutilizan los assets de Exerion, no es posible distribuir el juego ni siquiera como Open Source. Si alguna vez fuera necesario habría que reemplazar los assets de Exerion por otros distintos.
Se podrían generar con alguna herramienta de creación de sprites aleatoria como por ejemplo:
https://ianburnette.itch.io/random-sprite-generator

La nave del jugador no será tan pixelada, sin llegar a tener una resulución muy alta, pero algo mas moderno.
Para generarla hemos partido de una imagen encontrada por internet, reduciendo mucho su resolución y posteriormente alterando mucho su aspecto y colores.

Finalmente para el logo de inicio hemos usado un generador de imágenes de IA para generar múltiples alternativas, hemos seleccionado uno y modificado para obtener el aspecto deseado.

## Interface

La pantalla inicial consta de una presentación y logotipo del juego.

La interface del juego es sencilla, basada en el estilo de Exerion. En la parte central se encuentra el espacio de juego y a la derecha el interfaz informativo, que consta de un registro de la puntuación máxima conseguida, la puntuación de la partida actual, el nivel de carga que tenemos para los disparos rápidos, la escena en la que nos encontramos y finalmente un contador de vidas.

Excepto el contador de vidas que se corresponde con imágenes de naves monocromas, el resto de elementos son texto, usando una fuente pixelada sin antialiasing (fuente específica para terminales) y así conseguimos un aspecto retro.

## Mecánicas

### Movimiento de la nave

El movimiento de la nave es el básico de una nave espacial vista desde arriba, pero dispone de un sistema de inercia que hace que la nave siga moviéndose en la dirección en la que se movió por última vez, aunque el jugador deje de pulsar las teclas de dirección. De esta manera se consigue un efecto de ingravidez.
Además el movimiento con los cursores no será directo sino que la nave se moverá en la dirección pulsada con una aceleración y velocidad máxima. Con esto damos un poco de complejidad y realismo al movimiento de la nave para que no sea tan sencillo esquivar las balas y enemigos.

### Movimiento de los enemigos
### Colisiones
### Disparos de la nave
### Disparos de los enemigos

## Puntuación y vidas

Puntos por matar enemigos
Vidas

## Audio y música

