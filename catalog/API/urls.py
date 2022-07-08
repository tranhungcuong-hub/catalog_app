from django.urls import path, include
from rest_framework import routers

from catalog.API import views


urlpatterns = [
    # CATEGORIES
    path('category_list/', views.CategoryList.as_view(), name='cate_list_view'),
    path('category_create/', views.CategoryCreate.as_view(), name='cate_create_view'),
    path('category_detail/<int:id>', views.CategoryDetail.as_view(), name='cate_detail_view'),

    # PRODUCTS
    path('post_list/', views.PostList.as_view(), name='api_post_view'),
    path('post_create/', views.PostCreate.as_view(), name='api_post_view'),
    path('post_detail/<int:id>', views.PostRetriveDelete.as_view(), name='api_post_view'),

    # COMMENTS
    path('cmt_create/', views.CommentsCreate.as_view(), name='comments_create_view'),
    path('cmt_detail/<int:id>', views.CommentsDetail.as_view(), name='comments_detail_view'),

    # REPORT API
    path('category_report/', views.CategoryReport.as_view(), name='category_report'),
    path('post_report/', views.PostReport.as_view(), name='post_report'),
]
