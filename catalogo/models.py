from django.db import models

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
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.nome

class Carrossel(models.Model):
    titulo = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.titulo
    
class Banner(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    imagem = models.ImageField(upload_to='produtos/')
    data_adicionado = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.titulo
