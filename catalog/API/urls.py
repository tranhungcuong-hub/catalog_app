from django.urls import path, include
from rest_framework import routers

from catalog.API import views


urlpatterns = [
    # CATEGORIES
    path('categories/', views.CategoryList.as_view(), name='cate_list_view'),
    path('category/POST/', views.CategoryCreate.as_view(), name='cate_create_view'),
    path('category/RETRIEVE/<int:id>', views.CategoryDetail.as_view(), name='cate_detail_view'),

    # PRODUCTS
    path('post/GET/', views.PostList.as_view(), name='api_post_view'),
    path('post/CREATE', views.PostCreate.as_view(), name='api_post_view'),
    path('post/RETRIEVE/<int:id>', views.PostRetriveDelete.as_view(), name='api_post_view'),

    # COMMENTS
    path('cmt/CREATE/', views.CommentsCreate.as_view(), name='comments_create_view'),
    path('cmt/RETRIEVE/<int:id>', views.CommentsDetail.as_view(), name='comments_detail_view'),

    # REPORT API
    path('category/report/', views.CategoryReport.as_view(), name='category_report'),
    path('post/report/', views.PostReport.as_view(), name='post_report'),
]
# ccollection & item
# collection use plural nouns
# item use id
# do not use verbs
