from django.shortcuts import render, redirect, get_object_or_404
from .models import Client, Product, Order
from .forms import ClientForm, ProductForm, OrderForm
from django.shortcuts import render
from datetime import timedelta, datetime

def home(request):
    return render(request, 'myapp/home.html')

def create_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_clients')
    else:
        form = ClientForm()
    return render(request, 'myapp/create_client.html', {'form': form})

def list_clients(request):
    clients = Client.objects.all()
    return render(request, 'myapp/list_clients.html', {'clients': clients})

def update_client(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('list_clients')
    else:
        form = ClientForm(instance=client)
    return render(request, 'myapp/update_client.html', {'form': form})

def delete_client(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    client.delete()
    return redirect('list_clients')

def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)  # Убедитесь, что вы передаете request.FILES
        if form.is_valid():
            form.save()
            return redirect('list_products')  # Перенаправление после успешного создания продукта
    else:
        form = ProductForm()

    return render(request, 'myapp/create_product.html', {'form': form})


def list_products(request):
    products = Product.objects.all()
    return render(request, 'myapp/list_products.html', {'products': products})

def update_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('list_products')
    else:
        form = ProductForm(instance=product)
    return render(request, 'myapp/update_product.html', {'form': form})

def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect('list_products')


def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.save()
            form.save_m2m()
            return redirect('list_orders')
    else:
        form = OrderForm()

    return render(request, 'myapp/create_order.html', {'form': form})


def list_orders(request):
    orders = Order.objects.all()
    return render(request, 'myapp/list_orders.html', {'orders': orders})

def update_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('list_orders')
    else:
        form = OrderForm(instance=order)
    return render(request, 'myapp/update_order.html', {'form': form})

def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.delete()
    return redirect('list_orders')


def client_orders(request):
    clients = Client.objects.all()  # Получаем всех клиентов

    # Если клиент выбран, получаем его идентификатор
    client_id = request.GET.get('client_id')

    if client_id:
        # Получаем заказы для выбранного клиента
        client = Client.objects.get(id=client_id)

        # Определяем временные рамки
        end_date = datetime.now()
        week_ago = end_date - timedelta(days=7)
        month_ago = end_date - timedelta(days=30)
        year_ago = end_date - timedelta(days=365)

        # Получаем продукты из заказов клиента за последние 7, 30 и 365 дней
        orders_week = Order.objects.filter(
            client=client,
            order_date__gte=week_ago
        ).values_list('products', flat=True)

        orders_month = Order.objects.filter(
            client=client,
            order_date__gte=month_ago
        ).values_list('products', flat=True)

        orders_year = Order.objects.filter(
            client=client,
            order_date__gte=year_ago
        ).values_list('products', flat=True)

        # Получаем уникальные продукты за каждый период
        products_week = Product.objects.filter(id__in=set(orders_week)).distinct()
        products_month = Product.objects.filter(id__in=set(orders_month)).distinct()
        products_year = Product.objects.filter(id__in=set(orders_year)).distinct()

        context = {
            'clients': clients,
            'client': client,
            'products_week': products_week,
            'products_month': products_month,
            'products_year': products_year,
        }

        return render(request, 'myapp/client_orders.html', context)

    # Если клиент не выбран, возвращаем список клиентов
    context = {
        'clients': clients,
    }

    return render(request, 'myapp/client_orders.html', context)