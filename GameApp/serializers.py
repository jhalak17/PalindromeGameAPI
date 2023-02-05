from .models import UserModel
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserModel
        fields = ['username', 'email', 'password', 'password2']

    def create(self, validate_data):
        return UserModel.objects.create(**validate_data)

    def validate(self, data):
        password = data.get('password')
        password2 = data.get('password2')
        if password != password2:
            raise serializers.ValidationError("Password does not match")
        return data

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length = 255)
    class Meta:
        model = UserModel
        fields = ['email','password']

class UserManageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['email','id','password']

class UpdateBoardSerializer(serializers.Serializer):
    character = serializers.CharField(max_length = 1)



