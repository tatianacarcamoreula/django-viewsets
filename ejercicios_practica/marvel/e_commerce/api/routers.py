# Importamos DefaultRouter
from rest_framework.routers import DefaultRouter

# Tal cual hacíamos con APIView, importamos los
# Viewsets necesarios, ya que no deja de ser una View.
from .viewsets import (
    CustomUserViewSet,
    UserViewSet,
    FilteringUserViewSet,
    FilteringBackendUserViewSet
)

# Con esto indicamos que el router se haga cargo de nuestras
# rutas, por ende, internamente va a generar las rutas automáticamente 
# para cada petición HTTP que hayamos establecido en la view.
router = DefaultRouter()

# Registramos el endpoint y finalmente se lo
# asignamos a "urlpatterns".
# NOTE: Recordar que cuando enlazamos un archivo de rutas, Django
# siempre va intentar buscar en el archivo es que exista la lista
# 'urlpatterns'.
router.register(r'modelviewset/users', UserViewSet)
router.register(
    r'modelviewset/filtering-backend/users', FilteringBackendUserViewSet
)
router.register(r'viewset/users', CustomUserViewSet)
router.register(r'genericviewset/users', FilteringUserViewSet)
urlpatterns = router.urls