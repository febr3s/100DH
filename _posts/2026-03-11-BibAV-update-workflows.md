---
title: bibav workflows
---
Estoy en proceso de estabilizar y documentar los flujos para actualizar BibAV.

Está el tema de que actualmente la página se construye desde la rama biva_improvements, e idealmente se construiría desde main. Sin embargo eso implica cuidar la sincronización con la página principal de MOREL, y eso es un esfuerzo que pertenece a mi próximo proyecto, que es 100DH.

Por eso, por ahora:

BibAV se actualiza cuando hay cambios en la rama ´biva_improvements´. Si se cambia cualquier cosa que *no* sea ´books_zotero.csv´, se actualiza la página sin tocar el contenido. Si se cambia books_zotero, se regenera todo el contenido… sin las imágenes locales. Entonces hay que seguir, por ahora, los pasos de morelrep. 

Hay otras consideraciones pero podemos ir pasando a las conclusiones.

# Para actualizar el sitio desde el escritorio

Usamos un clon del repositorio forkeado. Hay que clonar de GitHub y después bajarse la rama biva_improvements.

##  Sin tocar la colección de libros (ningún cambio a  books_zotero.csv)

Por ejemplo, si queremos agregar una página, corregir un link en el footer, etc.

 1. Hacer los cambios en el clon local
 2. Commit and push
 3. Monitorear en ´https://github.com/morelrep/BibAV/actions´

## Modificando la colección (actualizando books_zotero.csv)

1. Generar el contenido actualizado usando los scripts de Python
 2. Commit and push **agregando al commit message (MUY IMPORTANTE)** ´[skip ci]´
 3. Cambiar el YML para triggerear la generacion (esto hay que eliminarlo pronto, pero por los momentos es la vía segura)
 4. Monitorear en ´https://github.com/morelrep/BibAV/actions´