from django.http import HttpResponse
from django.db.models import Q
from django.views.generic import ListView
from .models import Product, Category, Tag


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


class ProductListView(ListView):
    model = Product
    context_object_name = "products"
    paginate_by = 12

    def get_queryset(self):
        qs = (
            Product.objects
            .select_related("category")
            .prefetch_related("tags")
            .all()
        )
        q = self.request.GET.get("q", "").strip()
        category_slug = self.request.GET.get("category")
        tag_slugs = self.request.GET.getlist("tags")  # multiple tags

        if q:
            qs = qs.filter(Q(description__icontains=q) | Q(name__icontains=q))

        if category_slug:
            qs = qs.filter(category__slug=category_slug)

        if tag_slugs:
            qs = qs.filter(tags__slug__in=tag_slugs).distinct()

        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["q"] = self.request.GET.get("q", "")
        ctx["categories"] = Category.objects.all()
        ctx["tags"] = Tag.objects.all()
        ctx["selected_category"] = self.request.GET.get("category")
        ctx["selected_tags"] = set(self.request.GET.getlist("tags"))
        return ctx
