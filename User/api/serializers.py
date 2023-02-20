import re
from rest_framework import serializers
from User.models import User
from django.core.exceptions import ValidationError


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField()
    #Esta linea nos garantiza que el correo electronico suministrado sea válido
    email = serializers.EmailField() 
    
    class Meta:
        model = User
        fields = ['id','email','username','password']
        
    #Aqui vamos a encriptar la contraseña y no mostrarla en el retorno de datos del método post y la encriptacion la hace django por detras
    def create(self, validated_data):
        password = validated_data.pop('password',None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    
    # Validamos que la contraseña ingresada cumpla con la siguiente expresion regular
    #OJO CON LA ER
    def validate_password(self, value):
        pattern = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#\?])[a-zA-Z\d!@#\?]{10,}$")
        if not pattern.match(value):
            raise ValidationError("La contraseña debe tener al menos 10 caracteres, incluir una mayúscula, una minúscula y uno de los siguientes caracteres !, @, #, ?")
        return value
    

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email','username','first_name','last_name']


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']
        