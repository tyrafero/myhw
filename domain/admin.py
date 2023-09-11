from django.contrib import admin
from .models import User, Assignment, Bid, Order, Review, Message

admin.site.register(User)
admin.site.register(Assignment)
admin.site.register(Bid)
admin.site.register(Order)
admin.site.register(Review)
admin.site.register(Message)