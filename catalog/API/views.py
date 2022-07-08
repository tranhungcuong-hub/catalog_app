from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, BasePermission, SAFE_METHODS
from rest_framework.response import Response

from catalog.API.serializers import CategorySerializers, PostSerializers, CreatePostSerializers, CommentsCreateSerializers, CategoryReportSerializers, PostReportSerializers
from catalog.models import Category, Post, Comments
from catalog.reports import Category_report, Post_report


class PostUserPermission(BasePermission):
    message = 'Edditing post is restricted to the author only'

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.author == request.user


class PostList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializers

    def get_queryset(self):
        print(Post.objects.all())
        return Post.objects.all()


class PostCreate(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreatePostSerializers
    # parser_classes = (FormParser, MultiPartParser)

    # parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)

    def get_queryset(self):
        return Post.objects.all()


class PostRetriveDelete(generics.RetrieveUpdateDestroyAPIView, PostUserPermission):
    permission_classes = [PostUserPermission]
    serializer_class = PostSerializers
    lookup_field = 'id'

    def get_queryset(self):
        return Post.objects.all()


class CategoryList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CategorySerializers
    """
    List all categories, or create a new snippet.
    """

    def get_queryset(self):
        return Category.objects.all()


class CategoryCreate(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CategorySerializers

    def perform_create(self, serializer):
        return serializer.save()


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CategorySerializers
    lookup_field = 'id'

    def get_queryset(self):
        return Category.objects.all()


class CommentsCreate(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentsCreateSerializers

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)

    def get_queryset(self):
        return Comments.objects.all()


class CommentsDetail(generics.RetrieveUpdateDestroyAPIView, PostUserPermission):
    permission_classes = [PostUserPermission]
    serializer_class = CommentsCreateSerializers
    lookup_field = 'id'

    # def get_queryset(self):
    #     return Comments.objects.filter(author=self.request.user)


class CategoryReport(APIView):
    def get(self, request):
        data = Category_report()
        serializer = CategoryReportSerializers(instance=data, many=True)
        return Response(data=serializer.data)


class PostReport(APIView):
    def get(self, request):
        data = Post_report()
        serializer = PostReportSerializers(instance=data, many=True)
        return Response(data=serializer.data)