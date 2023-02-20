from django.db.models import Q
from django.shortcuts import render, redirect,get_object_or_404
from rest_framework.views import APIView
from posts.models import Post
from posts.api.serializers import PostSerializer
from posts.api.permissions import IsAuthorOrReadOnly
from rest_framework.pagination import LimitOffsetPagination
from User.models import User 
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.http import require_http_methods
from django.http import Http404
from rest_framework import generics




class DeletePostApiView(APIView):
    
    def post(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404("Post no existe")
        post.delete()
        return redirect('posts-list')



class EditPostApiView(APIView):
    permission_classes = [IsAuthorOrReadOnly]
    template_name="posts/post_edit.html"

    def get(self,request,pk):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = PostSerializer(post)
        return render(request, self.template_name, context={'post': post})
    
    def post(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return redirect('posts-list')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DetailPostApiView(APIView):

    template_name = 'posts/post_detail.html'        

    def get(self, request, pk):
        if not request.user.is_authenticated:
            return redirect('login')
        
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = PostSerializer(post)
        return render(request, self.template_name, context={'post': post})
    

class CreatePostApiView(APIView):
    template_name = 'posts/post_create.html'


    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        data = request.data.copy()
    
        access_token = request.GET.get('access_token', None)
        if access_token:
            from rest_framework_simplejwt.tokens import AccessToken
            decoded_token = AccessToken(access_token.replace('Bearer ', ''))
            user_id = decoded_token['user_id']
            user = User.objects.get(pk=user_id)
            data['user'] = user.id

        serializer = PostSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return redirect('posts-list')


class PostApiView(APIView):
    permission_classes = [IsAuthorOrReadOnly]
    pagination_class = LimitOffsetPagination
    template_name = 'posts/post_list.html'

    def get(self, request):

        if not request.user.is_authenticated:
            return redirect('login')
        
        queryset = Post.objects.all()
        userr = self.request.user
        if not userr.is_superuser:
            queryset = queryset.filter(Q(published=True) | Q(user=userr.id))
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)
        serializer = PostSerializer(page, many=True)

        context = {'posts': serializer.data}


        return render(request, self.template_name, context=context) 

