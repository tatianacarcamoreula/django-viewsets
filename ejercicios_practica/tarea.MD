![Inove banner](/inove.jpg)
Inove Escuela de Código\
info@inove.com.ar\
Web: [Inove](http://inove.com.ar)

---
# Tarea: Django - REST FRAMEWORK 3

Al realizar esta tarea pondremos en práctica los conocimientos adquiridos en clase.
Una vez finalizada, el alumno debe subir el enlace a su repositorio "forkeado" el foro de tarea correspondiente -NO SE ADMITE LA DEVOLUCIÓN POR OTRO CANAL SALVO SE ESPECIFIQUE LO CONTRARIO- 

Recuerde que no debe subir la base de datos al sistema, para ello se encuentra el archivo .gitignore que especifica los archivos y directorios omitidos.

---
### 1. Realizar las vistas de API.
Debe realizar una vista de API que herede de `GenericViewSet` y permita realizar un **CRUD** del modelo Comic.
- Tenga en cuenta que las acciones no vienen predefinidas por defecto, debe realizarlas desde 0, todas deben pasar por el serializador correspondiente.
- Debe proporcionar protección de acceso a estas vistas de API, la que debe ser accesible solo si el usuario está autenticado.
- Debe sobreescribir el método que poseen los serializadores para no mostrar el campo `description` al listar objetos o instancias.

### 2. Realizar una nueva vista de API.
Debe realizar una vista de API que herede de ModelViewSet y permita **únicamente** listar los comics.
La vista debe:
- Permitir filtrar por el campo `title`, `marvel_id`, filtrar aquellos comics cuya cantidad sea mayor e igual a 5. Utilizar la clase que permita realizar este filtro genérico.
- Permitir que pueda buscar y que contenga en la view en el campo `title`, el valor a pasar, no distinguiendo entre maýusculas y minúsculas.
- Permitir que pueda ordenar de mayor a menor por campo `marvel_id`, y, ordenar alfabéticamente según el campo `title`. Utilizar la clase que permita eso.
- *AYUDA*: No debe sobreescribir la acción sino que toda la lógica debe estar implementada en el método `.get_queryset()`. Debe sobreescribirlo.
- Debe proporcionar protección de acceso a estas vistas de API, la que debe ser accesible solo si el usuario está autenticado.
- **NOTA**: Crear un archivo dentro del directorio *api* llamado `comic_viewsets.py` y colocar todas las vistas pedidas con su lógicas correspondientes.

### 3. Crear el router para que administre las rutas del endpoint de manera automática.
- Crear un archivo llamado `comic_routers.py` dentro del directorio *api* y llamar a la clase correspondiente para agregar el ruteo de nuestra API.
- Se deja a criterio de cada uno, definir el endpoint.
**Ayuda**: Puede fijarse los ejemplos de clase para poder guiarse.

### 4. Ejercicio extra:
Crear una vista de API que **únicamente** liste los comics que *estén en el carrito de compras y que sean favoritos de un determinado usuario*.
Tenga en cuenta que acá se buscar obtener el detalle de un usuario, por lo tanto, se pide que por parámetro estático pueda ingresar el `id` o `pk` del usuario y devuelva los resultados correspondientes.
- Puede optar por utilizar vistas de API basadas en clases, o, basadas en funciones. Si utiliza vistas basadas en clases, puede heredar la que más le guste (ListAPIView, RetrieveAPIView, ModelViewSet). Si utiliza una vista de API basada en funciones, recuerde utilizar el decorador `@api_view`.
- El listado debe pasar por el serializador correspondiente.
- Debe definir el endpoint, lo cual queda a su criterio.
- **PLUS**: Agregar paginado a la API. Para ello observe los ejemplos de clase, dentro del archivo `viewsets.py`, la clase *LimitOffsetPagination*, *PageNumberPagination* y *ShortResultsSetPagination*.
---

## ¿Dudas?
Ante cualquier inquietud, debe referirse a los canales especificados para su trato en inove.