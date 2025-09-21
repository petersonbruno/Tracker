from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from .models import User
from .serializers import UserSerializer

# Register Driver
@api_view(['POST'])
@permission_classes([AllowAny])
def driver_register(request):
    data = request.data.copy()
    data['role'] = 'driver'
    serializer = UserSerializer(data=data)
    if serializer.is_valid():
        serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
        serializer.save()
        return Response({"message": "Driver registered successfully"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def driver_login(request):
    email = request.data.get("email")
    password = request.data.get("password")

    user = authenticate(request, email=email, password=password)

    if user is not None and user.role == "driver":
        login(request, user)  # Django creates a session
        return Response({
            "message": "Login successful",
            "user": {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "role": user.role
            }
        })
    return Response({"error": "Invalid credentials or not a driver"}, status=status.HTTP_401_UNAUTHORIZED)
