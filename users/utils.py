from store.models import Order
from django.core.paginator import Paginator, PageNotAnInteger,EmptyPage

def paginateOrders(request,orders,results):
    # Paginate the orders
    page = request.GET.get('page')
    paginator = Paginator(orders, results)  # Adjust the number of orders per page as needed

    try:
        orders = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        orders = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        orders = paginator.page(page)    

    leftIndex = (int(page) - 4)
    if leftIndex < 1:
        leftIndex = 1
    
    rightIndex = (int(page) + 5)   
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    print(orders)

    custom_range = range(leftIndex,rightIndex)

    return custom_range,orders

