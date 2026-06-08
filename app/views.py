from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404, redirect, render

from .forms import RegistrationForm, BlogForm, CommentForm, OrderCreateForm
from .models import Blog, Comment, Category, Product, Order, OrderItem


def index(request):
    latest_posts = Blog.objects.order_by("-posted")[:3]
    categories = Category.objects.all()
    products = Product.objects.filter(is_available=True)[:6]
    return render(request, "app/index.html", {
        "latest_posts": latest_posts,
        "categories": categories,
        "products": products,
    })


def about(request):
    return render(request, "app/about.html")


def contact(request):
    return render(request, "app/contact.html")


def blog(request):
    posts = Blog.objects.all()
    return render(request, "app/blog.html", {"posts": posts})


def blogpost(request, post_id):
    post = get_object_or_404(Blog, id=post_id)
    comments = post.comments.all()

    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect("login")

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect("blogpost", post_id=post.id)
    else:
        form = CommentForm()

    return render(request, "app/blogpost.html", {
        "post": post,
        "comments": comments,
        "form": form,
    })


@login_required
def newpost(request):
    if not request.user.is_staff:
        return redirect("blog")

    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("blog")
    else:
        form = BlogForm()

    return render(request, "app/newpost.html", {"form": form})


def registration(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()

            client_group, created = Group.objects.get_or_create(name="Client")
            user.groups.add(client_group)

            login(request, user)
            return redirect("home")
    else:
        form = RegistrationForm()

    return render(request, "app/registration.html", {"form": form})


def catalog(request):
    categories = Category.objects.all()
    products = Product.objects.filter(is_available=True)
    return render(request, "app/catalog.html", {
        "categories": categories,
        "products": products,
    })


def products_by_category(request, category_id):
    categories = Category.objects.all()
    selected_category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=selected_category, is_available=True)

    return render(request, "app/catalog.html", {
        "categories": categories,
        "products": products,
        "selected_category": selected_category,
    })


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_available=True)
    return render(request, "app/product_detail.html", {"product": product})


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_available=True)

    order, created = Order.objects.get_or_create(
        client=request.user,
        status=Order.StatusChoices.CART
    )

    item, item_created = OrderItem.objects.get_or_create(
        order=order,
        product=product,
        defaults={"quantity": 1, "price": product.price}
    )

    if not item_created:
        item.quantity += 1
        item.save()

    messages.success(request, "Товар добавлен в корзину.")
    return redirect("cart")


@login_required
def cart_view(request):
    order = Order.objects.filter(
        client=request.user,
        status=Order.StatusChoices.CART
    ).first()

    return render(request, "app/cart.html", {"order": order})


@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(
        OrderItem,
        id=item_id,
        order__client=request.user,
        order__status=Order.StatusChoices.CART
    )
    item.delete()
    messages.success(request, "Товар удалён из корзины.")
    return redirect("cart")


@login_required
def checkout(request):
    order = Order.objects.filter(
        client=request.user,
        status=Order.StatusChoices.CART
    ).first()

    if not order or not order.items.exists():
        messages.error(request, "Корзина пуста.")
        return redirect("cart")

    if request.method == "POST":
        form = OrderCreateForm(request.POST, instance=order)
        if form.is_valid():
            checkout_order = form.save(commit=False)
            checkout_order.status = Order.StatusChoices.NEW
            checkout_order.save()
            messages.success(request, "Заказ оформлен.")
            return redirect("orders_list")
    else:
        form = OrderCreateForm(instance=order)

    return render(request, "app/checkout.html", {
        "order": order,
        "form": form,
    })


@login_required
def orders_list(request):
    orders = Order.objects.filter(client=request.user).exclude(
        status=Order.StatusChoices.CART
    )
    return render(request, "app/orders_list.html", {"orders": orders})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(
        Order,
        id=order_id,
        client=request.user
    )
    return render(request, "app/order_detail.html", {"order": order})