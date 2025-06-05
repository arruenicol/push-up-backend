# backend/users/serializers.py
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User, Student, AdminProfile


class UserSerializer(serializers.ModelSerializer):
    user_type = serializers.SerializerMethodField()
    is_admin = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'user_type', 'is_admin')
        read_only_fields = ('id',)
    
    def get_user_type(self, obj):
        """Determine user type based on related models"""
        if hasattr(obj, 'adminprofile'):
            return 'admin'
        elif hasattr(obj, 'student'):
            return 'student'
        return None
    
    def get_is_admin(self, obj):
        """Check if user is admin"""
        return hasattr(obj, 'adminprofile')


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=[('student', 'Student'), ('admin', 'Admin')], write_only=True)
    sede = serializers.CharField(required=False, write_only=True)
    seccion = serializers.CharField(required=False, write_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'password', 'role', 'sede', 'seccion')
        read_only_fields = ('id',)

    def create(self, validated_data):
        role = validated_data.pop('role')
        sede = validated_data.pop('sede', None)
        seccion = validated_data.pop('seccion', None)

        user = User.objects.create_user(
            email=validated_data.get('email'),
            username=validated_data.get('email'),
            password=validated_data.get('password'),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )

        if role == 'student':
            Student.objects.create(user=user, sede=sede, seccion=seccion)
        elif role == 'admin':
            AdminProfile.objects.create(user=user)
            # Set Django's built-in staff status for admin users
            user.is_staff = True
            user.save()

        return user


class PushTokenSerializer(serializers.Serializer):
    push_token = serializers.CharField(max_length=255)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        
        # Add user information to the response
        user_serializer = UserSerializer(self.user)
        data['user'] = user_serializer.data
        
        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer