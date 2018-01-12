# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import gettext_lazy as _
#from simple_history.models import HistoricalRecords
from ckeditor.fields import RichTextField
#from ckeditor_uploader.fields import RichTextUploadingField


class Institute(models.Model):
    name = models.CharField(_("Name"), max_length=128, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Institute")
        verbose_name_plural = _("Institutes")


class Team(models.Model):
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE, related_name='teams')
    name = models.CharField(_("Name"), max_length=128)
    members = models.ManyToManyField('Person')  #, through='X_Team_Author')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Team")
        verbose_name_plural = _("Teams")


class Industry(models.Model):
    name = models.CharField(_("Name"), max_length=128, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Industry")
        verbose_name_plural = _("Industries")


class Branch(models.Model):
    industry = models.ForeignKey(Industry, on_delete=models.CASCADE, related_name='branches')
    name = models.CharField(_("Name"), max_length=128)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Branch")
        verbose_name_plural = _("Branches")


class Person(models.Model):  # authors + depositors + contact_tt
    lastname = models.CharField(_("Lastname"), max_length=48)
    other_names = models.CharField(_("Other names"), max_length=128)
    title_before = models.CharField(_("Title before"), max_length=128, null=True, blank=True)
    title_after = models.CharField(_("Title after"), max_length=128, null=True, blank=True)

    def __str__(self):
        return '%s %s' % (self.lastname, self.other_names)

    class Meta:
        verbose_name = _("Person")
        verbose_name_plural = _("People")


class Offer(models.Model):
    name = models.CharField(_("Name"), max_length=128, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Offer type")
        verbose_name_plural = _("Offer types")


#class TTManager(models.Manager):
#    def get_queryset(self):
#        return super().get_queryset().filter(tt=True)


#class DepositorManager(models.Manager):
#    def get_queryset(self):
#        return super().get_queryset().filter(depositor=True)


class Product(models.Model):
    tt = models.ForeignKey(Person, verbose_name=_("Transfer adviser"), on_delete=models.PROTECT, related_name='products_as_tt')
    depositor = models.ForeignKey(Person, verbose_name=_("Depositor"), on_delete=models.PROTECT, related_name='products_as_depositor')
    #author = models.ManyToManyField(Person, through='X_Product_Author')
    #author = models.ManyToManyField(Person)
    name = models.CharField(_("Name"), max_length=128)
    #created = models.DateTimeField(auto_now_add=True)
    #updated = models.DateTimeField(null=True, blank=True)
    published = models.DateTimeField(_("Published"), null=True, blank=True)
    #history = HistoricalRecords()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")


class ProductLoc(models.Model):
    LANG_CHOICES = (
        ('en_US', _('english')),
        ('cs_CZ', _('czech')),
    )

    product = models.ForeignKey(Product, verbose_name=_("Product"), on_delete=models.CASCADE, related_name='product_localizations')
    lang = models.CharField(max_length=5, choices=LANG_CHOICES)
    name = models.CharField(_("Name"), max_length=128)
    anotation = models.TextField(_("Synopsis"))
    content = RichTextField(_("Content"), null=True, blank=True, config_name='product_content')
    #pokus = RichTextUploadingField(config_name='awesome2_ckeditor', null=True, blank=True)  # všechny parametry jsem si vymyslel


    def __str__(self):
        return '%s: %s' % (self.lang, self.name)


# -----------------

class X_Product_Offer(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='offers', verbose_name=_("Product"))
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name='products', verbose_name=_("Offer type"))

    class Meta:
        verbose_name = _("Product offer type")
        verbose_name_plural = _("Product offer types")


class X_Product_Branch(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='branches', verbose_name=_("Product"))
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='products', verbose_name=_("Branch"))

    class Meta:
        verbose_name = _("Product_Branch")
        verbose_name_plural = _("Product_Branches")


class X_Product_Team(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='teams', verbose_name=_("Product"))
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='products', verbose_name=_("Team"))

    class Meta:
        verbose_name = _("Product team")
        verbose_name_plural = _("Product teams")


class X_Product_Author(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='authors', verbose_name=_("Product"))
    author = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='products', verbose_name=_("Author"))

    class Meta:
        verbose_name = _("Product author")
        verbose_name_plural = _("Product authors")


class X_Team_Author(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='authors', verbose_name=_("Team"))
    author = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='teams', verbose_name=_("Author"))
    role = models.CharField(max_length=128)

    class Meta:
        verbose_name = _("Team membership")
        verbose_name_plural = _("Team memberships")
