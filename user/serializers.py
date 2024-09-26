from rest_framework.serializers import ModelSerializer
from user.models import User

class UserSerializer(ModelSerializer):
      class Meta:
          model = User
          exclude = ['password','user_email','last_login','user_name','is_verify']
        
        
class UserAllDetailSerializer(ModelSerializer):
      class Meta:
          model = User
          fields = ('user_email','user_mobile_number','user_name')