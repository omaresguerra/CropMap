from django.contrib import admin

from .models import Image, Data, CroppingImage, CroppingData, CroppingDataDetail, Comparison

admin.site.register(Image)
admin.site.register(Data)
admin.site.register(CroppingImage)
admin.site.register(CroppingData)
admin.site.register(CroppingDataDetail)
admin.site.register(Comparison)
