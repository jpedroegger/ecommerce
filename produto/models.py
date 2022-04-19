from django.db import models
from PIL import Image
import os
from django.conf import settings
from django.utils.text import slugify
from utils.utils import formata_preco


class Produto(models.Model):
    nome = models.CharField(max_length=255)
    descricao_curta = models.TextField(max_length=255)
    descricao_longa = models.TextField()
    imagem = models.ImageField(upload_to='produto_imagens/%Y/%m')  # Cria uma pasta para as fotos (mês/ano)
    slug = models.SlugField(unique=True, blank=True, null=True)  # Precisa ser único. É o 'id' do produto.
    preco_marketing = models.FloatField(verbose_name='Preço')
    preco_marketing_promocional = models.FloatField(default=0,verbose_name='Preço Promo')
    tipo = models.CharField(
        default='V',
        max_length=1,
        choices=(
            ('V', 'Variável'),
            ('S', 'Simples'),
        )
    )

    def get_preco_formatado(self):
        return formata_preco(self.preco_marketing)
    get_preco_formatado.short_description = 'Preço'
    
    def get_preco_promocional_formatado(self):
        return formata_preco(self.preco_marketing_promocional)
    get_preco_promocional_formatado.short_description = 'Preço Promo.'

    @staticmethod
    def resize_image(img, new_width=800):
        img_full_path = os.path.join(settings.MEDIA_ROOT, img.name)  # Localiza o caminho do arquivo.
        img_pil = Image.open(img_full_path)  # Abre o arquivo da imagem utilizando o caminho salvo na variável acima.
        original_width, original_height = img_pil.size  # Guarda a altura e largura da imagem original nas variávels.

        if original_width <= new_width:  # Se a largura original for <= que o desejado, nada acontece.
            img_pil.close()
            return
        
        new_height = round((new_width * original_height) / original_width)  # Regra de 3 para obter x.

        new_img = img_pil.resize((new_width, new_height), Image.LANCZOS)  # Ajusta a nova imagem para os novos parametros.
        new_img.save(
            img_full_path,
            optimize=True,  # Otimizar foto.
            quality=50  # Qualidade em 50%
        )

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = f'{slugify(self.nome)}'
            self.slug = slug

        super().save(*args, **kwargs)

        max_image_size = 800

        if self.imagem:
            self.resize_image(self.imagem, max_image_size)

    def __str__(self):
        return self.nome



class Variacao(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    nome = models.CharField(max_length=50, blank=True, null=True)
    preco = models.FloatField()
    preco_promocional = models.FloatField(default=0)
    estoque = models.PositiveIntegerField(default=1)


    def __str__(self):
        return self.nome or self.produto.nome
    
    class Meta:
        verbose_name = 'Variação'
        verbose_name_plural = 'Variações'