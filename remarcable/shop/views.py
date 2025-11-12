from django.db.models import Q
from django.views.generic import ListView
from .models import Product, Category, Tag


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
        print(self.request.GET.get, flush=True)
        # inputs
        q = self.request.GET.get("q", "").strip()
        category_val = (self.request.GET.get("category") or "")
        tag_vals = self.request.GET.getlist("tags")

        # search by name/description
        if q:
            qs = qs.filter(Q(description__icontains=q) | Q(name__icontains=q))

        # filter by category (ID or slug)
        if category_val:
            # try integer ID first, then fall back to slug
            try:
                qs = qs.filter(category_id=int(category_val))
            except ValueError:
                raise Exception("Failed to filter by category")

        if tag_vals:
            # normalize to IDs if numeric; otherwise treat as slugs
            tag_ids = []
            for v in tag_vals:
                tag_ids.append(int(v))

            # require ALL tags; chain filters
            if tag_ids:
                for tid in tag_ids:
                    qs = qs.filter(tags__id=tid)

        # avoid duplicates from M2M joins and set a sensible default ordering
        return qs.distinct().order_by("-created_at")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["q"] = self.request.GET.get("q", "")
        ctx["categories"] = Category.objects.all().order_by("name")
        ctx["tags"] = Tag.objects.all().order_by("name")
        ctx["selected_category"] = self.request.GET.get("category")
        ctx["selected_tags"] = set(self.request.GET.getlist("tags"))
        return ctx
