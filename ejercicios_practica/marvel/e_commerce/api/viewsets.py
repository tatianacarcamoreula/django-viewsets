from django.shortcuts import get_object_or_404
from django.db.models import Q

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action

# Librería para manejar filtrado:
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

# Para manejar paginado:
from rest_framework.pagination import (
    LimitOffsetPagination,
    PageNumberPagination
)

from e_commerce.models import User
from .serializers import UserSerializer, UpdatePasswordUserSerializer


# Genero una clase para configurar el paginado de la API.
class ShortResultsSetPagination(PageNumberPagination):
    page_size = 3   # Cantidad de resultados por página

    # Me va a permitir configurar la cantidad de resultados a mostrar
    # por página.
    page_size_query_param = 'page_size'
    max_page_size = 10


# NOTE: Vemos que ahora los métodos para cada
# método HTTP, en los viewsets directamente 
# se los llaman "acciones". Ejemplo: list, create,
# update, retrieve, destroy, etc.
class CustomUserViewSet(viewsets.ViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = UserSerializer
    queryset = User.objects.all()   # equivale a: User.objects.filter()

    # Este método permite administrar los permisos según el tipo de 
    # acción que se ejecute.
    def get_permissions(self):
        if self.action != 'list':
            self.permission_classes = [IsAuthenticated]
        return [permission() for permission in self.permission_classes]

    def list(self, request):
        return Response(
            data=self.serializer_class(self.queryset, many=True).data,
            status=status.HTTP_200_OK
        )

    def create(self, request):
        user_serializer = self.serializer_class(data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(
                data=user_serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            data=user_serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
        
    def update(self, request, pk=None):
        _user = self.queryset.filter(pk=pk)
        if _user:
            user_serializer = self.serializer_class(
                instance = _user.first(),
                data=request.data
            )
            if user_serializer.is_valid():
                user_serializer.save()
                return Response(
                    data=user_serializer.data,
                    status=status.HTTP_200_OK
                )
            return Response(
                data=user_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
                data={'error': 'the user does not exist'},
                status=status.HTTP_404_NOT_FOUND
            )

    def retrieve(self, request, pk=None):
        # Me devuelve la instancia a partir del queryset, en caso
        # de no existir, retorna un código de estado 404.
        _user = get_object_or_404(self.queryset, pk=pk)
        return Response(
            data=self.serializer_class(
                instance=_user,
                many=False
            ).data,
            status=status.HTTP_200_OK
        )

    def destroy(self, request, pk=None):
        _user = get_object_or_404(self.queryset, pk=pk)
        _user.delete()
        return Response(
            data={'message': 'the user was deleted successfully'},
            status=status.HTTP_204_NO_CONTENT
        )

    # Al trabajar con Viewsets podemos definir nuestras propias
    # acciones basándonos en los métodos HTTTP.
    @action(
        detail=True,
        methods=['put'],
        name="change-password",
        url_path='change-password'
    )
    def change_password(self, request, pk=None):
        _user = get_object_or_404(self.queryset, pk=pk)
        _user_serializer = UpdatePasswordUserSerializer(
            instance=_user,
            data=request.data,
            partial=True
        )
        # `raise_exception=True` evito de realizar la condición de la línea
        # 48, pero de todas maneras genero una excepción si hay un problema
        # con la validación de los datos.
        _user_serializer.is_valid(raise_exception=True)
        _user_serializer.save()
        return Response(
            data=_user_serializer.data,
            status=status.HTTP_200_OK
        )


# Ahora veamos que sucede si los viewsets los
# heredamos de ModelViewSet.
class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    # NOTE: Con el siguiente atributo puedo administrar que tipo
    # de métodos permite esta view.
    # http_method_names = ['get', 'post', 'put', 'delete']
    queryset = serializer_class.Meta.model.objects.all()


class FilteringBackendUserViewSet(viewsets.ModelViewSet):
    '''
    Vista de API basada en Clase que permite manejar
    el filtrado, búsqueda, paginado y orden de los resultados del
    listado de la API.
    '''
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    # NOTE: Habilito sólo el método 'GET' para esta view.
    http_method_names = ('get',)
    queryset = serializer_class.Meta.model.objects.all()

    # NOTE: Utilizo el tipo de filtro.
    filter_backends = (DjangoFilterBackend,)
    # filter_backends = (DjangoFilterBackend, SearchFilter)
    # filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    
    # NOTE: Selecciono los campos a filtrar.
    filterset_fields = ('id', 'username', 'email', 'is_staff')
    # filterset_fields = {
    #     "id": ('gte', 'lte'),
    #     "username": ("contains",),
    #     "first_name": ("contains",),
    #     "last_name": ("exact",),
    #     "email": ('exact', 'contains'),
    #     "is_staff": ('exact',)
    # }

    # Genero un Paginado
    pagination_class = LimitOffsetPagination
    # pagination_class = ShortResultsSetPagination

    # Para buscar el valor en los campos seleccionados.
    # NOTE: se requiere `SearchFilter`.
    search_fields = ('username', 'first_name', 'last_name')

    # Permite ordenar el listado por los campos seleccionados.
    # NOTE: se requiere `OrderingFilter`.
    ordering_fields = ('pk', 'username')
    ordering = ('pk',)
    # ordering = ('-pk',)


class FilteringUserViewSet(viewsets.GenericViewSet):
    '''
    Vista de API basada en Clase que permite manejar
    el filtrado, búsqueda, y orden de los resultados del
    listado de la API utilizando el ORM de Django.
    '''
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    queryset = serializer_class.Meta.model.objects.all()

    # NOTE: Habilito sólo el método 'GET' para esta view.
    http_method_names = ('get',)

    def get_queryset(self):
        # Obtengo el queryset llamando al método get_queryset mediante super.
        queryset = super(FilteringUserViewSet, self).get_queryset()

        # Obtengo los parámetros dinámicos que me llegan en la URL
        # cuando el usuario realiza una petición de tipo GET.
        # NOTE: Recordar que otra forma de hacerlo es:
        # _pk: self.request.GET.get('id')
        _pk = self.request.query_params.get('id')
        _username = self.request.query_params.get('username')
        _email = self.request.query_params.get('email')
        _is_staff = self.request.query_params.get('is_staff')
        _search = self.request.query_params.get('search')
        _ordering = self.request.query_params.get('ordering')

        # Realizo el filtrado según los parámetros que me pasen.
        if _pk:
            queryset = queryset.filter(pk=int(_pk))
        if _username:
            queryset = queryset.filter(username__icontains=_username)
        if _email:
            queryset = queryset.filter(email__exact=_email)
        if _is_staff:
            queryset = queryset.filter(is_staff=_is_staff)

        # Realizo la búsqueda:
        # NOTE: El objeto 'Q' es equivalente al operador OR en SQL.
        if _search:
            queryset = queryset.filter(
                Q(username__icontains=_search) | 
                Q(first_name__icontains=_search) |
                Q(last_name__icontains=_search)
            )

        # Realizo el ordenamiento:
        if _ordering:
            # NOTE: Podríamos resolverlo con esta única línea pero
            # el usuario podría escribir mal el nombre de un parámetro y
            # provocaría que el servidor arroje un error.
            # Si estamos seguro de que siempre va a pasar bien los parámetros
            # podemos usar esta línea.
            # queryset = queryset.order_by(_ordering.lower())

            # Con esto nos aseguramos de que me ordene según estos campos.
            if _ordering == '-pk':
                queryset = queryset.order_by('-pk')
            elif _ordering == 'username':
                queryset = queryset.order_by('username')
            else:
                queryset = queryset.order_by('pk')

        return queryset

    def list(self, request):
        return Response(
            data=self.get_serializer(
                instance=self.get_queryset(), many=True
            ).data,
            status=status.HTTP_200_OK
        )

