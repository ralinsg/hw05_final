from django.core.paginator import Paginator

NUMBERS_OF_POSTS = 10


def get_page_context(request, queryset):
    paginator = Paginator(queryset, NUMBERS_OF_POSTS)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return {"page_obj": page_obj}
