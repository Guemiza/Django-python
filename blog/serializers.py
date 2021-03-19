from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('Project_name','Identifiat','project_description','visibility_Level','name_customer','Project_URL','status')
