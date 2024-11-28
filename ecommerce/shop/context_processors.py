from shop.models import Category
def category_list(request):
    c=Category.objects.all()
    return {'cl':c}