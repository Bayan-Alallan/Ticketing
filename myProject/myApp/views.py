from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
import token

from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.authtoken.models import Token
from rest_framework.request import Request
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import viewsets

from .serializer import UserSerializer


#Signup
class signup_view(APIView):
    permission_classes=[AllowAny]
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.save()

            token, created = Token.objects.get_or_create(user=user)
            return Response({'token':token.key,}, status=status.HTTP_201_CREATED)
        return Response (serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        return Response({'detail': 'Method Not Allowed. Use POST for this endpoint.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    


#Login
class Login_view(ObtainAuthToken):
    def post(self, request, *args, **Kwargs):
        serializer = self.serializer_class(data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        
        token, created=Token.objects.get_or_create(user=user)
        return Response({'token':token.key,},status=status.HTTP_200_OK)

#Logout
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    if request.method == 'POST':
        try:
            # Delete the user's token to logout
            request.user.auth_token.delete()
            return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



#Change_password(Update)
class change_password(APIView):
    permission_classes=[IsAuthenticated]
    def post(self, request):
        user = request.user
        current_password = request.data.get('current_password')
        new_password = request.data.get('new_password')  
        if not user.check_password(current_password):
            return Response({"error":"Current Passsword is uncorrect!"},status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(new_password)
        user.save()
        return Response({"Success":"Password was updated successfully."}, status=status.HTTP_200_OK)




#Add_user
@api_view(['POST'])
@permission_classes([IsAdminUser]) 
def add_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"Success": "User added successfully!", "user": serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#Delete_user
@api_view(['DELETE'])
@permission_classes([IsAdminUser])  
def delete_user(request, id):
    try:
        user = User.objects.get(id=id)  # Get the user by ID
        user.delete()  
        return Response({"Success": "User deleted successfully!"}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"Error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

#Search_user
@api_view(['GET'])
@permission_classes([IsAdminUser])  
def search_user(request):
    query = request.GET.get('query', '')  # Get the search query parameter (username or email)
    
    if query:
        users = User.objects.filter(username__icontains=query) | User.objects.filter(email__icontains=query)
        if users.exists():
            # You can serialize the users or return a list of user details directly
            user_data = [{"id": user.id, "username": user.username, "email": user.email} for user in users]
            return Response({"users": user_data}, status=status.HTTP_200_OK)
        return Response({"Error": "No users found"}, status=status.HTTP_404_NOT_FOUND)
    
    return Response({"Error": "Please provide a search query"}, status=status.HTTP_400_BAD_REQUEST)