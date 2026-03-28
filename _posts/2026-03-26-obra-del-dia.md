---
title: Obra del día
layout: post
ia: https://chat.deepseek.com/share/322v5uv3fuzi2aekyn
---
***
Comenzamos el día abordando la necesidad de automatizar la actualización de la página con una obra del día diferente cada vez, que coincida con el material generado para redes.

Probablemente sea inevitable abordar la complejidad de un script que:

1. Revisa si hay uno en particular programado para ese día
2. Si no hay uno programado para ese día, seleccionar cualquier otro que no esté seleccionado

Entonces definitivamente habría que trabajar con dos colecciones

for book in site.data.posts
	if book.date = todays.date
		define book as todays-book
	endif
endfor

if todays-book != nil
	print item
else
	define filtered books
		for book in site.data.books
			print one random book
		endfor
endif

***
Lo de arriba fue casi logrado. Queda pendiente:

1. Arreglar el render de la imagen en obra del día tal como está hoy pues los libros provenientes del archivo MOREL no se están mostrando. Esto ya lo arreglé en el layout de book, así que es cuestión de copiar eso.
2. Integrar el render de la obra no programada dentro de la obra programada (include "time-selector"). Hice un intento, ahora interrumpido deshecho por la confusión del punto anterior. Pero había llegado al problema de que se repetía infinitamente el libro, y no conseguía averiguar en qué punto estaba limitándose a uno originalmente en el index.

***
Quedó pendiente de la generación de videos poner para el futuro este ajuste:

Mejoras:

- en post_creator.py
 - arreglar book.author para que enumere los autores correctamente

***