from authentication.api.serializers import LoginSerializer, RegisterSerializer, UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import authenticate, login, logout


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    "success": True,
                    "message": "User registered successfully",
                    "data": UserSerializer(user).data
                },
                status=status.HTTP_201_CREATED
            )
        errors = serializer.errors
        if "email" in errors:
            message = "Registration failed: Email already exists"
        elif "password" in errors:
            message = "Registration failed: Passwords do not match"
        elif "username" in errors:
            message = "Registration failed: Username already exists"
        else:
            message = "Registration failed due to invalid data"
        return Response(
            {
                "success": False,
                "message": message,
                "errors": errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )

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
                login(request, user)
                return Response(
                    {
                        "success": True,
                        "message": "Login successful",
                        "data": UserSerializer(user).data
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
        try:
            logout(request)
            return Response(
                {
                    "success": True,
                    "message": "Successfully logged out",
                    "data": {}
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {
                    "success": False,
                    "message": "Logout failed",
                    "errors": {"non_field_errors": [str(e)]}
                },
                status=status.HTTP_400_BAD_REQUEST
            )
class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            serializer = UserSerializer(request.user)
            response_data = {
                "success": True,
                "message": "Profile retrieved successfully"
            }
            # Only include data if serializer.data is non-empty
            if serializer.data:
                response_data["data"] = serializer.data
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {
                    "success": False,
                    "message": "Failed to retrieve profile",
                    "errors": {"non_field_errors": [str(e)]}
                },
                status=status.HTTP_400_BAD_REQUEST
            )