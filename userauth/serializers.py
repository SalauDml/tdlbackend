from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
class UserSerializer (ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','password']
        read_only_fields = ['id']

    
    

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
    