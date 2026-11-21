from django.db import models

from cloudinary_storage.storage import RawMediaCloudinaryStorage

# Create your models here.

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, null= True)
    biography = models.TextField()
    author_image = models.ImageField(upload_to="author_image/",blank=True,null=True)
    user_name = models.CharField(max_length=100, unique=True, null = True, blank = True)
    website = models.URLField(blank= True)
    nationality = models.CharField(max_length=100, blank=True)
   

    def __str__(self):
        return self.first_name


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ManyToManyField (Category)
    cover_image = models.ImageField(upload_to="book_covers/",blank=True, null=True)
    pdf_file = models.FileField(upload_to="book_pdfs/",storage=RawMediaCloudinaryStorage(), blank=True,null=True)
    source = models.CharField(max_length=255,blank=True)
    license = models.CharField(max_length=255,blank=True)
    pdf_url = models.URLField(blank=True)

    def __str__(self):
        return self.title
