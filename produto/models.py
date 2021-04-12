from os import truncate
from utils import utils
from django.db import models
from PIL import Image
import os 
from django.conf import settings
from django.utils.text import slugify


class Produto(models.Model):
    nome = models.CharField(max_length=255)
    descricao_curta = models.TextField(max_length=255)
    descricao_longa = models.TextField()
    imagem = models.ImageField(
        upload_to = 'produto_imagens/%Y/%m/', blank=True, null=True
    )
    slug = models.SlugField(unique=True, blank=True, null=True)
    preco_marketing = models.FloatField(verbose_name='Preço')
    preco_marketing_promocional = models.FloatField(default=0, verbose_name='Preço promo.')
    tipo = models.CharField(
        max_length=1,
        default='V',
        choices=(
            ('V', 'Variável'),
            ('S', 'Simples')
        )
    )

    def __str__(self):
        return self.nome

    def get_preco_formatado(self):
        return utils.formata_preco(self.preco_marketing)
    get_preco_formatado.short_description = 'Preço'

    def get_preco_promocional_formatado(self):
        return utils.formata_preco(self.preco_marketing_promocional)
    get_preco_promocional_formatado.short_description = 'Preço promo.'
    
    @staticmethod
    def resize_image(img, new_width):
        img_full_path = os.path.join(settings.MEDIA_ROOT, img.name) 
        img_pil = Image.open(img_full_path)
        original_width, original_height = img_pil.size
        
        if original_width <= new_width:
            img_pil.close()
            return
        
        new_height = round((original_height * new_width) / original_width)

        new_img = img_pil.resize((new_width, new_height), Image.LANCZOS)
        new_img.save(
            img_full_path,
            quality=50,
            optimize=True
        )
    
    def save(self, *args, **kwargs):
        if not self.slug:
            slug = f'{slugify(self.nome)}'
            self.slug = slug

        super().save(*args, **kwargs)

        max_image_width = 800
        
        if self.imagem:
            self.resize_image(self.imagem, max_image_width)  
        

class Variacao(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    nome = models.CharField(max_length=50, blank=True, null=True)
    preco = models.FloatField()
    preco_promocional = models.FloatField(default=0)
    estoque = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.nome or self.produto.nome
