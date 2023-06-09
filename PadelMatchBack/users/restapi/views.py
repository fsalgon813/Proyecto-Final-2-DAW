from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import RegisterUserSerializer, LoginSerializer
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication

@api_view(['POST'])
def register_user(request):
    serializer = RegisterUserSerializer(data=request.data)
    if serializer.is_valid():
        response_data = serializer.save()
        return Response(response_data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 

class LoginView(APIView):
    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(email=email, password=password)

        if not user:
            return Response({'error': 'Credenciales inválidas'}, status=status.HTTP_404_NOT_FOUND)

        refresh = RefreshToken.for_user(user)
        user_id = user.id  # Obtén el ID del usuario

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user_id': user_id  # Incluye el ID del usuario en la respuesta
        })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def protected_view(request):
    user = JWTAuthentication().authenticate(request)
    if user is not None:
        user_id = user[0].id
        return Response({'user_id': user_id})
    else:
        return Response({'error': 'Usuario no autenticado'}, status=status.HTTP_401_UNAUTHORIZED)

class GetUserIDView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_id = request.user.id
        return Response({'user_id': user_id})