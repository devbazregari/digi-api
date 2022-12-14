from time import timezone
from django.db import models
from User.models import User
from datetime import datetime
from django.db.models import Count
from rest_framework.response import Response


class Attr(models.Model):
    name = models.CharField(max_length=2000, null=False, blank=False)


class Category(models.Model):
    name = models.CharField(max_length=500, null=False, blank=False)

class Product(models.Model):
    product_id      =   models.BigAutoField(null=False, blank=False, primary_key=True)
    attrs           =   models.ManyToManyField(to=Attr)
    category_id_fk  =   models.ForeignKey(to=Category , on_delete=models.CASCADE)


    title           =   models.CharField(null=False, blank=False, max_length=100)
    brand           =   models.CharField(max_length=100, null=False, blank=False)
    price           =   models.BigIntegerField(null=False, blank=False)
    mainImage       =   models.CharField(null=False, blank=False, max_length=300)
    brandCategory   =   models.CharField(null=False, blank=False, max_length=200)
    intro           =   models.CharField(null=False, blank=False, max_length=1000)
    overView        =   models.CharField(null=False, blank=False, max_length=1000)
    # attrs           =      models.JSONField(blank=True, null=True, max_length=10000) this could be here 


class Seen(models.Model):
   
    seen            =   models.BigIntegerField(blank=True, null=True, default=0)
    user_id_fk      =   models.ForeignKey(to = User ,blank=False , null= False , on_delete=models.CASCADE)
    prod_id_fk      =   models.ForeignKey(to = Product ,blank=False , null= False , on_delete=models.CASCADE)
    category_id_fk  =   models.ForeignKey(to = Category , on_delete=models.CASCADE , null=True , blank=True)
    last            =   models.CharField(default='True' , max_length=10)
    created_on      =   models.DateTimeField(default = datetime.now())

    def get_most_seen_product(kwargs):

        try:
            ctg  = Category.objects.get(name=kwargs['category'])
            print('here')
        except Category.DoesNotExist:
            print('wwww')
            ctg  = Category.objects.get(pk=1)

        query = "select id , seen,sum(seen)  from Products_seen where category_id_fk_id = {} group by prod_id_fk_id order by sum(seen) desc limit 1" .format(ctg.pk)
        top_expensive_prod = Seen.objects.raw(query)
        queryset = Product.objects.filter(product_id__in = [i.prod_id_fk_id	 for i in top_expensive_prod])
    
        return queryset


class Sold(models.Model):

    sold            =   models.BigIntegerField(blank=True, null=True, default=0)
    user_id_fk      =   models.ForeignKey(to = User ,blank=False , null= False , on_delete=models.CASCADE)
    prod_id_fk      =   models.ForeignKey(to = Product ,blank=False , null= False , on_delete=models.CASCADE)
    category_id_fk  =   models.ForeignKey(to = Category , on_delete=models.CASCADE)
    discount        =   models.BooleanField(default=False , blank=True , null=True)
    created_on      =   models.DateTimeField(default = datetime.now())


    def get_queries(kwargs):

        try:
            ctg  = Category.objects.get(name=kwargs['category'])
        except Category.DoesNotExist:
            ctg  = Category.objects.get(pk=1)
        types = {'popular':['count','product_id','desc'] , 'expensive':['sum','-product_id','desc'] , 'cheapest':['sum','product_id','asc']}
        search_type = types[kwargs['type']]

        query = "select id , {}(sold) , prod_id_fk_id  from Products_sold where category_id_fk_id = '{}' group by prod_id_fk_id order by {}(sold) {} limit 1 ".format(search_type[0],ctg.pk,search_type[0],search_type[2])
        top_expensive_prod = Sold.objects.raw(query)

        queryset = Product.objects.filter(product_id__in = (i.prod_id_fk_id for i in top_expensive_prod) , category_id_fk=ctg.pk).order_by(search_type[1])
        return queryset
