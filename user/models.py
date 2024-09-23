from django.db import models

# Create your models here.
import uuid
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

class UserManager(BaseUserManager):
    def create_user(self,user_id, user_mobile_number, user_email, ):
        if not user_email:
            raise ValueError("Users must have an mobile number")
        
        user = self.model(
            user_email = user_email,
            user_id = user_id,
            user_mobile_number = user_mobile_number,
           
           
        )

      
        user.save(using=self._db)
        return user
class User(AbstractBaseUser):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_email = models.EmailField(max_length=225, unique=True , null=True,blank=True)
    user_mobile_number = models.CharField(max_length=10,unique=True)
    user_name = models.CharField(max_length=225,null=True,blank=True)
    is_verify = models.BooleanField(default=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = UserManager()

    USERNAME_FIELD = "user_mobile_number"
    REQUIRED_FIELDS = ["user_mobile_number"]

    def __str__(self):
        return self.user_email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True

    # @property
   
    
    def save(self, *args, **kwargs):     
        # self.user_password = make_password(self.user_password)
  
        super(User, self).save(*args, **kwargs)
    
