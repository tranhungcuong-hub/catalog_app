from django.urls import path, include
from django.conf.urls.static import static

from catalog import views
from catalog_app1 import settings

urlpatterns = [
                    path('', include('user.urls')),
                    path("category/", views.HomeView.as_view(), name='category'),
                    path("detail/<int:pk>", views.ArticleDetailView.as_view(), name='detail'),
                    path("add_cate/", views.AddCategoryView.as_view(), name='add_cate'),
                    path("cate_view/", views.CateHomeView.as_view(), name='cate_view'),
                    path("cate_view/<int:pk>", views.DeleteCate, name='delete_cate'),
                    path("add_post/", views.AddPostView.as_view(), name="add_post"),
                    path("update_post/<int:pk>", views.UpdatePostView.as_view(), name="update_post"),
                    path("delete_post/<int:pk>", views.DeletePostView.as_view(), name="delete_post"),
                    path("cate/<int:pk>", views.CategoryView, name="cate"),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
