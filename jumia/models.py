from django.db import models


class Smartphone(models.Model):
    nom = models.CharField(max_length=200)
    price_final = models.FloatField()
    old_price = models.FloatField()
    discount_f = models.IntegerField()
    product_url = models.URLField()
    image= models.URLField()

    def __str__(self):
        return self.nom

    class Meta:
        db_table = 'smartphone'
