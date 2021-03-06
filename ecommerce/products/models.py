from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save
from django.db import models
from django.utils.text import slugify

class ProductQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def all(self, *args, **kwargs):
        return self.get_queryset().active()

    def get_related(self, **kwargs):
        return self.get_queryset()
class Product(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    sale_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    active = models.BooleanField(default=True)
    categories = models.ManyToManyField('Category', blank=True)
    default = models.ForeignKey('Category', related_name='default_category', null=True, blank=True)
    objects = ProductManager()

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"pk":self.pk})
def image_upload_to(instance, filename):
    title = instance.product.title
    slug = slugify(title)
    file_extension = filename.split(".")[1]
    new_filename = "%s.%s"%(instance.id, file_extension)
    return 'products/%s/%s' %(slug, new_filename)


class Variation(models.Model):
    product = models.ForeignKey(Product)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to=image_upload_to)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    sale_price = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    inventory = models.IntegerField(null=True, blank=True)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.title

    def get_price(self):
        if self.sale_price is not None:
            return self.sale_price
        else:
            return self.price

    def get_absolute_url(self):
        return self.product.get_absolute_url()

def post_save_signal_receiver(sender, instance, created, *args, **kwargs):
    product = instance
    variations = product.variation_set.all()
    if variations.count() == 0:
        new_var = Variation()
        new_var.product = product
        new_var.title = "Original Product"
        new_var.price = product.price
        new_var.save()
post_save.connect(post_save_signal_receiver, sender=Product)

def image_upload_to(instance, filename):
    title = instance.product.title
    slug = slugify(title)
    file_extension = filename.split(".")[1]
    new_filename = "%s.%s"%(instance.id, file_extension)
    return 'products/%s/%s' %(slug, new_filename)


class ProductImage(models.Model):
    product = models.ForeignKey(Product)
    image = models.ImageField(upload_to=image_upload_to)

    def __unicode__(self):
        return self.product.title


class Category(models.Model):

    title = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __unicode__(self):
        return self.title


    def get_absolute_url(self):
        return reverse("category_detail", kwargs={"slug": self.slug })

