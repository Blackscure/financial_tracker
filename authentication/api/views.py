from authentication.api.serializers import LoginSerializer, RegisterSerializer, UserSerializer
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from django.contrib.auth import authenticate
from rest_framework.views import APIView


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            return Response({
                "success": True,
                "message": "User registered successfully",
                "data": {
                    "user": UserSerializer(user).data,
                  
                }
            }, status=status.HTTP_201_CREATED)
        return Response({
            "success": False,
            "message": "Registration failed",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                request,
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password']
            )
            if user:
                # Generate Knox token only if authentication succeeds
                token = AuthToken.objects.create(user)[1]
                return Response(
                    {
                        "success": True,
                        "message": "Login successful",
                        "user": UserSerializer(user).data,
                        "token": token
                    },
                    status=status.HTTP_200_OK
                )
            return Response(
                {
                    "success": False,
                    "message": "Invalid username or password",
                    "errors": {"non_field_errors": ["Invalid credentials"]}
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
        return Response(
            {
                "success": False,
                "message": "Login failed due to invalid data",
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )



class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        request._auth.delete()
        return Response({
            "success": True,
            "message": "Successfully logged out"
        }, status=status.HTTP_200_OK)


class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response({
            "success": True,
            "message": "Profile retrieved successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
