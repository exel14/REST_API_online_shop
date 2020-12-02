from django.contrib import admin
from .models import *

admin.site.register([Product,Order,Address,ProductToOrder])

