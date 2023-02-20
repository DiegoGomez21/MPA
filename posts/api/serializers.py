from rest_framework import serializers
from posts.models import Post

class PostSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = Post
        fields = ['id','title','content','slug','miniature','published','user','username']