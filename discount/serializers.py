from rest_framework import serializers
from .models import Code, Status
from django.contrib.auth.models import User

class DiscountCodeSerializer(serializers.ModelSerializer):

    class Meta: 
        model = Code
        fields = ('id', 'user_id','title', 'code', 'list_product','created_date',)


class UserSerializer(serializers.ModelSerializer):

    class Meta: 
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name','date_joined', )

        

class DiscountStatusSerializer(serializers.ModelSerializer):

    class Meta: 
        model = Status
        fields = ('user', 'connected_date', 'status', 'paid', )