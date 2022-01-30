from django.db import models
from config.g_model import TimeStampMixin
from django.utils import timezone
# Create your models here.
class Variant(TimeStampMixin):
    title = models.CharField(max_length=40, unique=True)
    description = models.TextField()
    active = models.BooleanField(default=True)


class Product(TimeStampMixin):
    title = models.CharField(max_length=255)
    sku = models.SlugField(max_length=255, unique=True)
    description = models.TextField()


class ProductImage(TimeStampMixin):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    file_path = models.URLField()


class ProductVariant(TimeStampMixin):
    variant_title = models.CharField(max_length=255)
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class ProductVariantPrice(TimeStampMixin):
    product_variant_one = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, null=True,
                                            related_name='product_variant_one')
    product_variant_two = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, null=True,
                                            related_name='product_variant_two')
    product_variant_three = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, null=True,
                                              related_name='product_variant_three')
    price = models.FloatField()
    min_price = models.FloatField(null=True,)
    stock = models.FloatField()
    min_stock = models.FloatField(null=True,)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    insertion_time              =models.DateField(auto_now=True, auto_now_add=False)
    last_updated                =models.DateField(auto_now=False, auto_now_add=True)
    
    def date_trunc_field(self):
        return self.insertion_time.strftime('%m/%d/%Y')

    def save(self, *args, **kwargs):
        if self.last_updated is None:
            self.last_updated = timezone.now()
        elif not self.last_updated is not None:
            self.last_updated = None
        super(ProductVariantPrice, self).save(*args, **kwargs)