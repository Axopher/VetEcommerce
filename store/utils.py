from .models import Product
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def paginateProducts(request,products,results):
    page = request.GET.get('page')
    results = results
    paginator = Paginator(products,results)

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        products = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        products = paginator.page(page)


    leftIndex = (int(page) - 4)

    if leftIndex < 1:
        leftIndex = 1

    rightIndex = (int(page) + 5)   

    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_range =  range(leftIndex,rightIndex)

    # Get the total number of results
    total_results = paginator.count

    # Get the current page number
    page_number = request.GET.get('page')
    current_page = paginator.get_page(page_number)

    # Get the number of results on the current page
    num_results_on_page = len(current_page)

    return custom_range, products, num_results_on_page, total_results

def searchProducts(request,category_id=None):
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')


    products = Product.objects.filter(
        Q(name__icontains=search_query) |
        Q(description__icontains=search_query)
    )

    if category_id:
        products = products.filter(category_id=category_id)


    return products,search_query