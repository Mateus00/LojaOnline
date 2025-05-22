from django.db import models
from django.utils.text import slugify

class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    promocao = models.BooleanField(default=False)
    
    def __str__(self):
        return self.nome

class Produto(models.Model):
    nome = models.CharField(max_length=150)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=8, decimal_places=2)
    imagem = models.ImageField(upload_to='produtos/')
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    banner = models.BooleanField(default=False)
    promocao = models.BooleanField(default=False)
    preco_promocional = models.DecimalField(max_digits=8, decimal_places=2)
    data_adicionado = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True)
    # outros campos...

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome

class Carrossel(models.Model):
    titulo = models.CharField(max_length=200)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, null=True, blank=True)
    promocao = models.BooleanField(default=False)

    def produtos(self):
        if self.promocao:
            if self.categoria:
                return Produto.objects.filter(categoria=self.categoria, promocao=True)
            else:
                return Produto.objects.filter(promocao=True)
        else:
            if self.categoria:
                return Produto.objects.filter(categoria=self.categoria)
            else:
                return Produto.objects.all()

    def __str__(self):
        return self.titulo
    
class Banner(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    imagem = models.ImageField(upload_to='banners/')
    categoria = models.ManyToManyField('Categoria', related_name='banners', blank=True)
    data_adicionado = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True)
    # outros campos...

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)  # Corrigir para self.titulo
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.titulo
