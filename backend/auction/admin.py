# admin.py
from django.contrib import admin
from .models import Auction, Bid
from django import forms
# from django.contrib.contenttypes.models import ContentType

# class AuctionAdminForm(forms.ModelForm):
#     class Meta:
#         model = Auction
#         exclude = ['item_category']  # Exclude 'item_category' from the form
#         labels = {
#             'item_id': 'Vehicle',  # Change the label for 'item_id' to 'Vehicle'
#         }
#     def __init__(self, *args, **kwargs):
#         super(AuctionAdminForm, self).__init__(*args, **kwargs)
        
#         # Preselect item_category for vehicles
#         vehicle_content_type = ContentType.objects.get(app_label='vehicle', model='vehicle')
#         self.vehicle_content_type_id = vehicle_content_type.id
#         content_type = ContentType.objects.get_for_id(vehicle_content_type.id)
#         objects = content_type.model_class().objects.all()
#         self.fields['item_id'].widget = forms.Select(choices=[(obj.id, obj.name) for obj in objects])

#     def save(self, commit=True):
#         instance = super(AuctionAdminForm, self).save(commit=False)
#         instance.item_category_id = self.vehicle_content_type_id  # Set item_category internally
#         if commit:
#             instance.save()
#         return instance
# class AuctionAdmin(admin.ModelAdmin):
#     form = AuctionAdminForm

# admin.site.register(Auction, AuctionAdmin)
admin.site.register(Bid)
admin.site.register(Auction)
