from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
    SEX_TYPE = (
        ('M', 'Masculin'),
        ('F', 'Féminin'),
    )
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    adresse = models.CharField(max_length=255)
    sexe = models.CharField(max_length=1, choices=SEX_TYPE)
    age = models.CharField(max_length=20)
    zip_code = models.CharField(max_length=10)
    save_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True) # models.SET_NULL ou models.PROTECT
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'

    @property
    def get_total_spent(self):
        articles = self.article_set.all() # permet d'avoir tout les objets articles d'une facture précise
        total = sum(article.get_total_price() for article in articles)
        return total

    def __str__(self):
        return self.name

class Invoice(models.Model):
    """
        Model representing an invoice.
        Name : Invoice
        Description : This model represents an invoice issued to a customer.
        Authors : Edithson (moafogaus@gmail.com)
    """
    INVOICE_TYPE = (
        ('S', 'Standard'),
        ('P', 'Proforma'),
        ('R', 'Recu'),
        ('C', 'Credit'),
    )
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.BooleanField(default=False)
    invoice_type = models.CharField(max_length=50, default='S', choices=INVOICE_TYPE)
    comment = models.TextField(null=True, blank=True, max_length=500, default="Aucun commentaire")
    save_by = models.ForeignKey('auth.User', on_delete=models.PROTECT, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Facture'
        verbose_name_plural = 'Factures'

    def __str__(self):
        return f"Invoice # {self.id} - {self.customer.name} - {self.invoice_type} - {'Paid' if self.paid else 'Unpaid'}"
    
class Article(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='articles')
    name = models.CharField(max_length=100)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    save_by = models.ForeignKey('auth.User', on_delete=models.PROTECT, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'

    @property
    def get_total_price(self):
        unit_price = self.unit_price or 0
        quantity = self.quantity or 0
        return unit_price * quantity

    def __str__(self):
        return self.name
