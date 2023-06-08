from django.contrib import admin

from .models import Stock
from .models import Transaction
from .models import User
from .models import Portfolio

admin.site.register(Stock)
admin.site.register(Transaction)
admin.site.register(User)
admin.site.register(Portfolio)

# Register your models here.
