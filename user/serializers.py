from rest_framework.serializers import ModelSerializer
from user.models import User

class UserSerializer(ModelSerializer):
      class Meta:
          model = User
          exclude = ['password','user_email','last_login','user_name','is_verify']