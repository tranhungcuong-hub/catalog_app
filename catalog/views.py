from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User

from catalog.models import Post, Category, ProductImages
from catalog.forms import PostForm, UpdateForm, CateForm


# Create views here.
class HomeView(ListView):
    model = Post
    images = ProductImages
    template_name = 'catalog.html'
    ordering = ['-post_time']
    paginate_by = 3

    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()

        context = super(HomeView, self).get_context_data(*args, **kwargs)
        context["cat_menu"] = cat_menu
        # context["user"] = current_user
        return context


def CategoryView(request, pk):
    categories = Category.objects.all()
    cate_post = Post.objects.filter(category__id=pk)

    return render(request, 'category.html', {'id': pk, 'cate_post': cate_post, 'categories': categories})


class ArticleDetailView(DetailView):
    model = Post
    template_name = 'article.html'

    def get(self, *args, **kwargs):
        self.object = self.get_object()
        if self.request.user.id != self.object.author.id:
            self.object.views = self.object.views + 1
            self.object.save()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class AddPostView(CreateView):
    user = User
    form_class = PostForm
    template_name = 'add_post.html'

    def form_valid(self, form):
        p = form.save()
        images = self.request.FILES.getlist('images')
        for i in images:
            ProductImages.objects.create(post=p, images=i)

        for k in form.cleaned_data['category']:
            selection = Category.objects.get(name=k)
            p.category.add(selection)
        return super().form_valid(form)


class AddCategoryView(CreateView):
    model = Category
    form_class = CateForm
    template_name = 'add_cate.html'


class CateHomeView(ListView):
    model = Category
    template_name = 'edit_category.html'

    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(CateHomeView, self).get_context_data(*args, **kwargs)
        context["cat_menu"] = cat_menu
        return context


def DeleteCate(request, pk):
    cat_id = get_object_or_404(Category, pk=pk)
    cat_id.delete()
    return redirect('cate_view')


class DeleteCategoryView(DeleteView):
    model = Category
    success_url = reverse_lazy('cate_view')


class UpdatePostView(UpdateView):
    model = Post
    form_class = UpdateForm
    template_name = 'update_post.html'


class DeletePostView(DeleteView):
    model = Post
    template_name = 'delete_post.html'
    success_url = reverse_lazy('category')
