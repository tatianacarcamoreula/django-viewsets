![Inove banner](/inove.jpg)
Inove Escuela de Código\
info@inove.com.ar\
Web: [Inove](http://inove.com.ar)

---
# Tarea: Django - REST FRAMEWORK 2

Al realizar esta tarea pondremos en práctica los conocimientos adquiridos en clase.
Una vez finalizada, el alumno debe subir el enlace a su repositorio "forkeado" el foro de tarea correspondiente -NO SE ADMITE LA DEVOLUCIÓN POR OTRO CANAL SALVO SE ESPECIFIQUE LO CONTRARIO- 

Recuerde que no debe subir la base de datos al sistema, para ello se encuentra el archivo .gitignore que especifica los archivos y directorios omitidos.

---

### 1. Implemente el serializador necesario para el modelo WishList.
Basado en el material visto en clase, incluido en la carpeta "ejemplos_clase" desarrolle el serializador necesario para el modelo WishList.
Para poder incluir las Foreign Keys debe utilizar el método 'serializers.PrimaryKeyRelatedField' por ejemplo:
    ```user_id = serializers.PrimaryKeyRelatedField(write_only=True,
                                                   queryset=User.objects.all())```
Luego el atributo debe ser incluido dentro de los 'fields', junto con el resto de los atributos del modelo.

### 2. Realizar las vistas de API.
Debe realizar todas las vistas de API necesarias para realizar el CRUD de la base de datos para la entidad "WishList".
Debe proporcionar protección de acceso a estas vistas de API, la que debe ser accesible solo si el usuario está autenticado.

### 3. Asignar las URLs para las vistas de API.
Asigne las URLs para poder acceder a estas vistas, por ejemplo:
```
path('Wish/get', GetWishListAPIView.as_view()),
```

### 4. Realizar una API "mixta".
Realice una API mixta para consultar los comics favoritos de un usuario particular.
Para ello recomendamos sobrescribir el método "get_queryset()" y realizar allí todas las consultas lógicas.
Utilice un endpoint del estilo:
    
 ``` 
 path('favs/<username>/get', GetUserFavsAPIView.as_view()), 
 ```

La lógica a seguir podría ser:
* Obtener el parametro 'username' del request
* Consultar al modelo 'User' si existe dicho usuario y obtener el objeto del modelo.
    * ``` user = User.objects.filter(username=username) ```
* Con dicho objeto, consultar en el modelo "WishList" por los comics que este usuario posee en favoritos. La consulta puede ser similar a:
    * ``` wish_list = WishList.objects.filter(user_id=user.first(), favorite=True) ```
* Ahora dispondrá de una lista de objetos del modelo "WishList" de dicho usuario que están en favoritos, con estos datos, debemos consultar qué comics están en esta lista:
    * ``` comic_obj = Comic.objects.filter(id=f'{wish.comic_id}').first() ```
(Nótese que el argumento del filtro está casteado a string y lo llamamos "wish" ya que es solo un elemento de la lista "wish_list") 

* El paso siguiente es armar la lista de diccionarios de retorno, como por ejemplo:

``` 
[{
        'marvel_id': '',
        'title': '',
        'description': '',
        'price': 1.00,
        'stock_qty': '',
        'picture': '',
    },
    {
        'marvel_id': '',
        'title': '',
        'description': '',
        'price': 1.00,
        'stock_qty': '',
        'picture': '',
    },
    ...] 
```
* La API también debe solicitar autenticación para su uso.

### 5. Instale Swagger para poder ver la documentación general de las APIs. 
Basandose en la documentación de clase y el ejemplo brindado en "ejemplo_clase" instale Swagger para poder ver la documentación de sus APIs.

---

## ¿Dudas?
Ante cualquier inquietud, debe referirse a los canales especificados para su trato en inove.