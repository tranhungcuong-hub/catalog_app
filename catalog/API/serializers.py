from django.db import models
from rest_framework import serializers, status
from rest_framework.response import Response

from catalog.models import Category, Post, ProductImages, Comments


class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'parent']


class ImagesSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = ['id', 'images']


class CommentsSerializers(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    reply_count = serializers.SerializerMethodField()

    class Meta:
        model = Comments
        fields = ['id', 'content', 'parent', 'author', 'reply_count', 'post_id']

    def get_reply_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        return 0

    def get_author(self, obj):
        return obj.author.username


class CommentsCreateSerializers(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = Comments
        fields = ['id', 'content', 'parent', 'author', 'post']

    def get_author(self, obj):
        return obj.author.username


class PostSerializers(serializers.ModelSerializer):
    category = CategorySerializers(many=True, required=False, read_only=True)
    # category = Category.objects.prefetch_related('post').only('id', 'name')
    images = ImagesSerializers(many=True, required=False, read_only=True)
    author = serializers.SerializerMethodField()
    comments = CommentsSerializers(read_only=True, many=True)
    # comments = Comments.objects.select_related('post')

    def get_author(self, obj):
        return obj.author.username

    class Meta:
        model = Post
        fields = ['id', 'author', 'title', 'script', 'post_time', 'thumnail', 'category', 'images', 'comments', 'views']


class CreatePostSerializers(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), write_only=True, many=True)
    images = serializers.ListField(
        child=serializers.ImageField(max_length=None, allow_empty_file=True, allow_null=True, use_url=True,
                                     required=False))
    thumnail = serializers.ImageField(max_length=None, allow_empty_file=True, allow_null=True, use_url=True,
                                      required=False)

    class Meta:
        model = Post
        fields = ['id', 'title', 'script', 'post_time', 'thumnail', 'category', 'images']

    def create(self, validated_data):
        images_data = validated_data.pop('images')
        categories_data = validated_data.pop('category')
        post = Post(**validated_data)
        post.save()

        for image_data in images_data:
            i = ProductImages(post=post, images=image_data)
            i.save()

        for cats in categories_data:
            post.category.add(cats)

        return PostSerializers(post).data


class Post_Serializers(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    def get_author(self, obj):
        return obj.author.username

    class Meta:
        model = Post
        fields = ['id', 'title', 'author', 'script', 'views']


class CategoryReportSerializers(serializers.Serializer):
    category = CategorySerializers()
    total_post = serializers.DecimalField(max_digits=None, decimal_places=0)


class PostReportSerializers(serializers.Serializer):
    post = Post_Serializers()
    total_comment = serializers.DecimalField(max_digits=None, decimal_places=0)
