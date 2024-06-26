from django.db import models

# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length= 50, unique= True)
    slug = models.CharField(max_length= 100)
    description = models.TextField(max_length= 250, blank= True)
    cat_image = models.ImageField(upload_to= 'photos/categories', blank= True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.category_name