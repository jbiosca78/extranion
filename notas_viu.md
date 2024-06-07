# Práctica VIU, mejoras y extras

Este juego nace como una práctica del curso de programación de videojuegos de la Universidad de Valencia (VIU) impartida por Iván Fuertes.

El tipo de juego es parecido al videojuego que se desarrolla en el curso, ya que también se trata de un videojuego shot'tem up, pero a medida que he ido desarrollandolo se ha ido separando del juego del curso. A continuación detallo algunas diferencias importantes respecto a la programación y la mecánica.

## Clases 'singleton'
Las clases 'singleton', no me gustan personalmente, no le veo sentido en python a tener una clase que sólo se instancia una vez ya que el propio funcionamiento de los módulos de python ya realiza esa función.
Por lo tanto en lugar de tener clases, ejecuto la inicialización de los objetos en el propio módulo y los métodos de la clase estática los dejo como métodos del propio módulo.

De esta manera se reduce mucho la simplicidad del código en los módulos y en las llamadas a los métodos, ya que puedo prescindir del ".instance().". Como ejemplo el módulo config se reduce de 28 líneas de código a 7.

## Assets
No me gusta mezclar código python con los propios assets del juego, por lo que he creado un directorio data con los binarios (imágenes, fuentes, etc) y he dejado en assets únicamente el código.

## Configuración
En clase utilizamos un archivo json para la configuración del juego. Pero en ocasiones necesitamos probar distintas variables de configuración y es interesante comentar y descomentar ciertas variables o grupos de variables.
Desgraciadamente el formato json original no soporta comentarios. Existe una variable de json, llamada jsonc promovida por Microsoft que sí que la soporta, pero la librería estandard de json no lo soporta.
Además, el formato json no es precisamente amigable. Por ejemplo si comentas la última línea de un grupo de variables tienes que quitar la última coma de la línea anterior.
Por lo tanto he decidido utilizar un archivo de configuración en formato yaml, que es mucho más amigable y soporta comentarios.
