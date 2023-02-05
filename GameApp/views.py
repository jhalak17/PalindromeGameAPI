from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer, UserLoginSerializer, UserManageSerializer, UpdateBoardSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from django.contrib.auth import authenticate
from .models import UserModel, GameModel
from rest_framework.parsers import JSONParser
import random, string


# Create your views here.
@api_view(['POST'])
@csrf_exempt
def UserCreationView(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return Response({"message": "User created successfully"}, status= status.HTTP_201_CREATED)
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@csrf_exempt
def UserLoginView(request):
    if request.method == 'POST':
        try:
            serializer = UserLoginSerializer(data=request.data)
            if serializer.is_valid():   # returns a User object if the credentials are valid
                print("serializer in login = ", serializer.data)
                user = UserModel.objects.get(email = serializer.data.get("email"))
                request.session['user'] = user.id
                print("user id stored in session = ", user.id)
                return Response({'msg':'Login Success'}, status=status.HTTP_200_OK)  
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)  
        except Exception as e:
            return Response({'msg':"No User found"}, status=status.HTTP_404_NOT_FOUND)
        

@api_view(['DELETE','PUT'])
@csrf_exempt
def UserManageView(request, pk):

    try:
        user = UserModel.objects.get(id = pk)
    except user.DoesNotExist:
        return Response({'msg':'No User Found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        user.delete()
        return Response({'msg':'User deleted successfully'}, status=status.HTTP_200_OK) 

    if request.method == 'PUT':
        new_data = JSONParser().parse(request) 
        serializer = UserSerializer(user, data=new_data, partial = True)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return Response({"message": "Data updated successfully"}, status= status.HTTP_200_OK)
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@csrf_exempt
def StartGameView(request):
    if request.method == "POST":
        game_id = random.randrange(1000,9999)
        user_id = request.session.get("user")
        print("user id under start game = ", user_id)
        user = UserModel.objects.get(id = user_id)
        print("user under start game = ", user)
        game = GameModel(game_id = game_id, user = user)
        game.save()
        return Response({'GameId':game_id}, status=status.HTTP_200_OK) 

@api_view(['GET'])
def GetBoardView(request, pk):
    if request.method == "GET":
        game_id = pk
        game = GameModel.objects.get(game_id = pk)
        if len(game.game_string) >= 6:
            return Response({"message":"Please start a new game"}, status=status.HTTP_200_OK)
        return Response({'GameId':game_id,"string":""}, status=status.HTTP_200_OK)

@api_view(['POST'])
@csrf_exempt
def UpdateBoardView(request, pk):
    if request.method == 'POST':
        game = GameModel.objects.get(game_id = pk)
        game_string = game.game_string.replace("0","")
        if len(game_string) > 6:
            return Response({"message" : "Sorry!!! Game is over"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        print("game string from model = ", game_string)
        serializer = UpdateBoardSerializer(data=request.data)
        if serializer.is_valid():
            print(serializer.data)
            game_string = game_string + serializer.data.get("character")
            random_char = random.choice(string.ascii_letters)
            game_string = game_string + random_char.lower()
            print("game string updated = ", game_string)
            game.game_string = game_string
            game.save()
            if len(game_string) == 6:
                if game_string == game_string[::-1]:
                    game.is_palindrome = True
                    return Response({"string":game_string, "message" : "Congratulations!!! You have created a palindrome"},status=status.HTTP_200_OK)
                else:
                    game.is_palindrome = False
                    return Response({"string":game_string, "message":"OOPSS!!!! This is not a palindrome"},status=status.HTTP_200_OK)
            if len(game_string) > 6:
                return Response({"message" : "Sorry!!! Game is over"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            return Response({"string":game_string},status=status.HTTP_200_OK)



