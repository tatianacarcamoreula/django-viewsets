from django.contrib.auth.models import User

# Importamos un validador de password que ofrece Django.
from django.contrib.auth import password_validation
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError as DjangoValidationError

# Luego importamos todos los serializadores de django rest framework.
from rest_framework import serializers
from rest_framework.authtoken.models import Token

# Primero importamos los modelos que queremos serializar:
from e_commerce.models import Comic, WishList


class ComicSerializer(serializers.ModelSerializer):
    # new_field =  serializers.SerializerMethodField()
    
    class Meta:
        model = Comic
        fields = ('marvel_id','title', 'description', 'price', 'stock_qty', 'picture')
        # fields = ('marvel_id', 'title', 'algo')

    # def get_new_field(self, obj):
    #     return {'hola':10}


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = '__all__'
        exclude = ('groups', 'user_permissions')

    def validate_password(self, value):
        try:
            password_validation.validate_password(value)
            return value
        except DjangoValidationError as e:
            raise serializers.ValidationError({'messages': e})

    def validate(self, attrs):
        attrs['password'] = make_password(
            password=attrs.get('password')
        )
        return attrs

    def create(self, validated_data):
        '''
        Método que permite administrar y manejar el tema
        de la creación de una instancia cuando se realiza
        un 'POST'.
        '''
        print('Se crea el objeto/instancia')
        return super(UserSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        '''
        Método que permite administrar y manejar el tema
        de la actualización de una instancia cuando se realiza
        un 'PUT/PATCH'.
        '''
        print('Se actualiza el objeto/instancia')
        return super(UserSerializer, self).update(instance, validated_data)

    # NOTE: Descomentar este método y observar que sucede con los métodos
    # 'create()' y 'update()' cuando se realiza un POST o PUT/PATCH.
    # def save(self):
    #     '''
    #     Método que permite administrar la persistencia
    #     al crearse o actualizarse uno o varios objetos.
    #     '''
    #     print('Entró al método ".save()".')
    #     # super(UserSerializer, self).save()

    def to_representation(self, instance):
        '''
        Método que permite personalizar
        los campos que deseo que se muestren al
        retornar una instancia o varias de ellas.
        '''
        data = super(UserSerializer, self).to_representation(instance)
        
        # NOTE: Descomentar, realizar una petición GET
        # y observar que sucede.
        # data.pop('password')
        # data.pop('is_active')
        return data


class UserTokenSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password')

    def validate(self, data):
        _username = self.Meta.model.objects.filter(
            username=data.get('username')
        ).first()
        if not _username:
            raise serializers.ValidationError(
                'El username ingresado no existe'
            )
        if not _username.check_password(data.get('password')):
            raise serializers.ValidationError(
                'La password ingresada es incorrecta'
            )
        return data

class TokenSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Token
        fields = ('key', 'user')
        

class UpdatePasswordUserSerializer(serializers.ModelSerializer):
    current_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        exclude = ('groups', 'user_permissions')

    def _required_field_message(self, fieldname):
        raise serializers.ValidationError(
            {f"{fieldname}": "This field is required."}
        )

    def validate_username(self, value):
        print('Validación de campo')
        print(value)
        if value != self.instance.username:
            raise serializers.ValidationError(
                 {'message': 'The current username entered is not correct.'}
            )
        return value

    # Override del método que valida y verifica si la password actual
    # corresponde al user en cuestión.
    def validate_current_password(self, value):
        print('Validación de campo')
        print(value)
        print(self.instance.check_password(value))
        if not self.instance.check_password(value):
            raise serializers.ValidationError(
                {'message': 'The current password entered is not correct.'}
            )
        return value

    # Override del método que valida la nueva password ingresada.
    # Se utiliza la función 'validate_password()' de Django para realizar
    # las validaciones.
    # https://docs.djangoproject.com/en/3.1/topics/auth/passwords/
    def validate_new_password(self, value):
        print('Validación de campo')
        print(value)
        try:
            password_validation.validate_password(
                value, self.instance
            )
            if self.instance.check_password(value):
                raise serializers.ValidationError(
                    {"message": "You entered the same password as the current."}
                )
            return value
        except DjangoValidationError as e:
            raise serializers.ValidationError({'messages': e})

    def validate(self, data):
        '''
        Este método es conveniente cuando se necesita validar
        campos que están relacionados entre sí.
        Acá se realiza la validación de todos los campos que están
        vigentes en el parámetro 'data'.
        '''
        print('Validación de objeto')
        print(data)
        if not data.get('username'):
            self._required_field_message('username')
        if not data.get('current_password'):
            self._required_field_message('current_password')
        if not data.get('new_password'):
            self._required_field_message('new_password')
        return data

    # Override del método "update()"" que actúa cuando se realiza
    # un 'PUT'.
    def update(self, instance, validated_data):
        '''
        Este método se ejecuta cuando se realiza un método HTTP: 'PUT'.
        Se ejecuta luego de pasar todas las validaciones, tanto a nivel de
        campo como de objeto/instancia.
        '''
        # El método `set_password()` me permite cambiar la password y se
        # encarga de hashearla.
        instance.set_password(validated_data.get('new_password'))
        instance.save() # Este ".save()" es el que actúa en el modelo.
        print('Password actualizada')
        return instance

    def to_representation(self, instance):
        '''
        Este método permite administrar los datos y/o campos a mostrar
        cuando se realizar un response.
        '''
        data = super(
            UpdatePasswordUserSerializer, self
        ).to_representation(instance)

        # NOTE: 'data' es un diccionario, por lo tanto
        # puedo utilizar los métodos de la clase 'dict'
        # y aplicarlos.
        data.pop('password')
        data.pop('is_active')
        return data


# TODO: Realizar el serializador para el modelo de WishList
class WishListSerializer(serializers.ModelSerializer):
    # algo =  serializers.SerializerMethodField()
    user = serializers.PrimaryKeyRelatedField(
        write_only=True,
        queryset=User.objects.all()
    )
    comic = serializers.PrimaryKeyRelatedField(
        write_only=True,
        queryset=Comic.objects.all()
    )
    
    class Meta:
        model = WishList
        fields = (
            'id',
            'user',
            'comic',
            'favorite',
            'cart',
            'wished_qty',
            'buied_qty'
        )