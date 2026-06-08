from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Blog(models.Model):
    title = models.CharField(
        max_length=100,
        unique_for_date="posted",
        verbose_name="Заголовок"
    )
    description = models.TextField(verbose_name="Краткое содержание")
    content = models.TextField(verbose_name="Полное содержание")
    posted = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name="Опубликована"
    )
    image = models.ImageField(
        upload_to="news/",
        default="temp.jpg",
        verbose_name="Изображение"
    )

    def get_absolute_url(self):
        return reverse("blogpost", args=[str(self.id)])

    def __str__(self):
        return self.title

    class Meta:
        db_table = "Posts"
        ordering = ["-posted"]
        verbose_name = "новость"
        verbose_name_plural = "новости"


class Comment(models.Model):
    text = models.TextField(verbose_name="Комментарий")
    date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name="Дата"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор"
    )
    post = models.ForeignKey(
        Blog,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Новость"
    )

    def __str__(self):
        return f"Комментарий {self.author} к {self.post}"

    class Meta:
        db_table = "Comments"
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии к новостям"
        ordering = ["-date"]


class Category(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Название категории"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Описание"
    )
    image = models.ImageField(
        upload_to="categories/",
        blank=True,
        null=True,
        verbose_name="Изображение"
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = "категория"
        verbose_name_plural = "категории"


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Категория"
    )
    name = models.CharField(
        max_length=150,
        verbose_name="Название"
    )
    short_description = models.CharField(
        max_length=255,
        verbose_name="Краткое описание"
    )
    description = models.TextField(verbose_name="Полное описание")
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена"
    )
    image = models.ImageField(
        upload_to="products/",
        blank=True,
        null=True,
        verbose_name="Изображение"
    )
    is_available = models.BooleanField(
        default=True,
        verbose_name="Доступен"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Добавлен"
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = "товар"
        verbose_name_plural = "товары"


class Order(models.Model):
    class StatusChoices(models.TextChoices):
        CART = "cart", "Корзина"
        NEW = "new", "Новый"
        IN_PROGRESS = "in_progress", "В обработке"
        COMPLETED = "completed", "Выполнен"
        CANCELLED = "cancelled", "Отменён"

    client = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="orders",
        verbose_name="Клиент"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Создан"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Обновлён"
    )
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.CART,
        verbose_name="Статус"
    )
    comment = models.TextField(
        blank=True,
        verbose_name="Комментарий клиента"
    )

    def __str__(self):
        return f"Заказ №{self.id} - {self.client.username}"

    def total_cost(self):
        return sum(item.total_price() for item in self.items.all())

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "заказ"
        verbose_name_plural = "заказы"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="Заказ"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="Товар"
    )
    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name="Количество"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена на момент заказа"
    )

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"

    def total_price(self):
        return self.quantity * self.price

    class Meta:
        verbose_name = "позиция заказа"
        verbose_name_plural = "позиции заказа"