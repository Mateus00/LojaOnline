from django.db import models

class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.nome

class Produto(models.Model):
    nome = models.CharField(max_length=150)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=8, decimal_places=2)
    imagem = models.ImageField(upload_to='produtos/')
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.nome