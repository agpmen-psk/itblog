from django.contrib import admin
from .models import Blog, Comment, Category, Product, Order, OrderItem


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ("title", "posted")
    search_fields = ("title", "description", "content")
    list_filter = ("posted",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("author", "post", "date")
    search_fields = ("author__username", "post__title", "text")
    list_filter = ("date",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name", "description")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "is_available", "created_at")
    search_fields = ("name", "short_description", "description")
    list_filter = ("category", "is_available", "created_at")


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "client", "status", "created_at", "updated_at")
    search_fields = ("client__username", "comment")
    list_filter = ("status", "created_at", "updated_at")
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "product", "quantity", "price")
    search_fields = ("order__id", "product__name")