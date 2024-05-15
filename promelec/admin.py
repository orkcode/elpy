from django.contrib import admin
from promelec.models import PromelecProduct, PromelecInventory, PromelecCategory, PromelecBrand, PromelecOrder, SitemapURL

# Register your models here.
admin.site.register(PromelecCategory)
admin.site.register(PromelecProduct)
admin.site.register(PromelecInventory)
admin.site.register(PromelecBrand)
admin.site.register(PromelecOrder)
admin.site.register(SitemapURL)

