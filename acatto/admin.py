from django.contrib import admin
#from django.contrib.auth.models import Group, User
#from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.utils.translation import ugettext as _

ModelAdmin = admin.ModelAdmin

from .models import (
        Institute, Team,
        Industry, Branch,
        Offer,
        Person,
        X_Team_Author,
        Product, ProductLoc,
        X_Product_Offer, X_Product_Branch, X_Product_Team, X_Product_Author,)


# DRY classes

class TabularInline(admin.TabularInline):
    extra = 0


class StackedInline(admin.StackedInline):
    extra = 0


class MetaProduct:  # toto je moje třída, nikoli konstrukt Djanga
    verbose_name = _("Product")
    verbose_name_plural = _("Products")


# inlines

class IndustryBranchInline(TabularInline):
    model = Branch


class InstituteTeamInline(TabularInline):
    model = Team


class TeamAuthorInline(TabularInline):
    model = X_Team_Author
    verbose_name = _("Author")
    verbose_name_plural = _("Authors")


class AuthorTeamInline(TabularInline):
    model = X_Team_Author
    verbose_name = _("Team")
    verbose_name_plural = _("Teams")


class ProductLocInline(StackedInline):
    model = ProductLoc
    verbose_name = _("Product localization")
    verbose_name_plural = _("Product localizations")


class ProductOfferInline(TabularInline):
    model = X_Product_Offer
    verbose_name = _("Offer type")
    verbose_name_plural = _("Offer types")


class OfferProductInline(TabularInline):
    model = X_Product_Offer
    verbose_name = MetaProduct.verbose_name
    verbose_name_plural = MetaProduct.verbose_name_plural


class ProductBranchInline(TabularInline):
    model = X_Product_Branch
    verbose_name = _("Branch")
    verbose_name_plural = _("Branches")


class BranchProductInline(TabularInline):
    model = X_Product_Branch
    verbose_name = MetaProduct.verbose_name
    verbose_name_plural = MetaProduct.verbose_name_plural


class ProductTeamInline(TabularInline):
    model = X_Product_Team
    verbose_name = _("Team")
    verbose_name_plural = _("Teams")


class TeamProductInline(TabularInline):
    model = X_Product_Team
    verbose_name = MetaProduct.verbose_name
    verbose_name_plural = MetaProduct.verbose_name_plural


class ProductAuthorInline(TabularInline):
    model = X_Product_Author
    verbose_name = _("Author")
    verbose_name_plural = _("Authors")

    #def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #    if db_field.name == "author":
    #        kwargs["queryset"] = Person.objects.filter(author=True)
    #    return super().formfield_for_foreignkey(db_field, request, **kwargs)


class AuthorProductInline(TabularInline):
    model = X_Product_Author
    verbose_name = MetaProduct.verbose_name
    verbose_name_plural = MetaProduct.verbose_name_plural


# extended adminsites

class InstituteAdmin(ModelAdmin):
    inlines = [InstituteTeamInline,]

class TeamAdmin(ModelAdmin):
    #fields = ['members']
    inlines = [TeamAuthorInline, TeamProductInline]


class IndustryAdmin(ModelAdmin):
    inlines = [IndustryBranchInline,]


class BranchAdmin(ModelAdmin):
    inlines = [BranchProductInline,]


class OfferAdmin(ModelAdmin):
    inlines = [OfferProductInline,]


class PersonAdmin(ModelAdmin):
    inlines = [AuthorProductInline, AuthorTeamInline]

'''
from django import forms
class ProductForm(forms.ModelForm):
    pass
'''

class ProductAdmin(ModelAdmin):
    # form = ProductForm
    inlines = [ProductLocInline, ProductOfferInline, ProductBranchInline, ProductTeamInline, ProductAuthorInline]

    #def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #    if db_field.name == "tt":
    #        kwargs["queryset"] = Person.objects.filter(tt=True)
    #    elif db_field.name == "depositor":
    #        kwargs["queryset"] = Person.objects.filter(depositor=True)
    #    return super().formfield_for_foreignkey(db_field, request, **kwargs)


# https://stackoverflow.com/questions/40090090/django-1-10-override-adminsite -- daniel.widyanto
# READ THIS !! https://stackoverflow.com/questions/4877335/how-to-use-custom-adminsite-class
# asi nic: https://stackoverflow.com/questions/4392424/how-to-solve-this-problem-you-dont-have-permission-to-edit-anything-in-dj

'''
class AdminSite(admin.AdminSite):
    # site_header = 'My Project Title'
    # site_title  = 'My Project Title Administration'
    index_title = 'Academic - Administrace'

    def get_app_list(self, request):
        """
        Return a sorted list of all the installed apps that have been
        registered in this site.
        """
        app_dict = self._build_app_dict(request)

        # Sort the apps alphabetically.
        app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())

        # Sort the models alphabetically within each app.
        """
        for app in app_list:
            xx=app['models']
            from pdb import set_trace; set_trace()
            app['models'].sort(key=lambda x: x['name'])
        """

        return app_list


# Create admin_site object from MyAdminSite
admin_site = AdminSite()  # name='my_project_admin'
'''

admin.site.register(Institute, InstituteAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Industry, IndustryAdmin)
admin.site.register(Branch, BranchAdmin)
admin.site.register(Offer, OfferAdmin)
admin.site.register(Person, PersonAdmin)
#admin.site.register(X_Team_Author)
admin.site.register(Product, ProductAdmin)
#admin.site.register(X_Product_Offer)
#admin.site.register(X_Product_Branch)
#admin.site.register(X_Product_Team)
#admin.site.register(X_Product_Author)

admin.site.index_title = 'Academic TTO'
