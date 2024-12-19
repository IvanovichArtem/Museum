from django.db import models

from user.models import User

class ProductType(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self) -> str:
        return f"{self.name}"

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    img = models.ImageField(upload_to="product_images")
    quantity = models.PositiveIntegerField(default=0)
    type = models.ForeignKey(ProductType, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.name} | {self.type}"



class ProductBasket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"User {self.user} | Product {self.product}"
