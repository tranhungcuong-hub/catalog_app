from dataclasses import dataclass
from decimal import Decimal

from django.db.models import Sum, Count

from catalog.models import Category, Post, Comments


@dataclass
class CategoryReport:
    category: Category
    total_post: Decimal


@dataclass
class PostReport:
    post: Post
    total_comment: Decimal


def Category_report():
    data = []

    queryset = Post.objects.values("category").annotate(
        total_post = Count('id'),
    )

    categories_index = {}
    for category in Category.objects.all():
        categories_index[category.id] = category

    for item in queryset:
        category = categories_index[item['category']]
        data_input = CategoryReport(category, item['total_post'])
        data.append(data_input)

    return data


def Post_report():
    data = []

    # cmt = Comments.objects.select_related('post')


    for item in Post.objects.all():
        try:
            cmt = Comments.objects.filter(post_id=item.id).count()
        except Comments.DoesNotExist:
            cmt = 0
        data_input = PostReport(item, cmt)
        data.append(data_input)

    return data