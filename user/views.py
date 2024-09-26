from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from user.serializers import UserSerializer,UserAllDetailSerializer
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
import requests
import json
from user.models import User 
# Create your views here.

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'access': str(refresh.access_token),
        'refresh': str(refresh)
    }

def otpSender(id,mobile_number): # type: ignore
        url = "https://cpaas.messagecentral.com/verification/v3/send?countryCode=91&customerId={id}&flowType=SMS&mobileNumber="+mobile_number

        payload = {}
        headers = { 
                    'authToken': 'eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJDLUMzQTY0OTJDRTRBOTRDNiIsImlhdCI6MTcyNjU3MTc2NywiZXhwIjoxODg0MjUxNzY3fQ.S8Lf51Zp7RrODBpVgYdwY9F7I4nRqf5bHPzsiFtYJaa_8r9PKXTiP04j3nIbd9R2P23F9s0GsoFF2WcTHsQisQ'
                   }

        response = requests.request("POST", url, headers=headers, data=payload)
        print(id)
    
        data = json.loads(response.text)
        verification_id = data['data']['verificationId']
        return verification_id
    

  
  
def createUser(dataa):
        serializer = UserSerializer(data = dataa)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        mobile_number = serializer.data['user_mobile_number']
        id = serializer.data['user_id']
        verification_id = otpSender(id,mobile_number)
        return verification_id
       
       
       
        
class UserLoginView(GenericAPIView):
    serializer_class = UserSerializer
    def post(self, request, format=None):
        mobile_number = request.data.get('user_mobile_number')
     
        
        try:   
        #        print("dfvgbffrggrfgb ")
               user = User.objects.get(user_mobile_number=mobile_number)
        
               print(user.is_verify)
      
               if user.is_verify == False:
                #    token = get_tokens_for_user(user)
                   verification_id = otpSender(user.user_id,mobile_number)
                   return Response({
                         "verification_id": verification_id,
                         "message":"User is logged in successfully",
                        #  "token": token,
                     },status=200)
               else:
                     
                    #  token = get_tokens_for_user(user)
                     verification_id = otpSender(user.user_id,mobile_number)
                     return Response({
                           "verification_id": verification_id,
                           "message":"user is not verified",
                        #    "token": token
               },status=200)
        except:      
            
              verification_id  = createUser(request.data)
              user = User.objects.get(user_mobile_number = mobile_number)
             
              print("tghyjhgf3edrfgthyjnhg4rf5thyjnhgrtg5yhjumhyg4rtghyjumjhg3r4ghyjum")
            #   token = get_tokens_for_user(user)
              return Response({
                 "message": "User registered successfully",
                 "verification_id": verification_id,
                #  "tokens": token
                 
                },status=200)
class UserDeleteView(APIView):
    def delete(self, request, ):
        User.objects.all().delete()
        return Response({
            'status': status.HTTP_200_OK,
            'message': "All users deleted successfully"
        }, status=200)
        
        
        
        
class UserUpdateView(GenericAPIView):
    serializer_class = UserAllDetailSerializer
    def patch(self, request,input,format=None):
        id = input
        user = User.objects.get(user_id=id)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)