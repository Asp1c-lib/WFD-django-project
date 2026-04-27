from django.contrib import admin
from .models import Case, CaseNote, CaseLog

# Register your models here.


admin.site.register(Case)
admin.site.register(CaseNote)
admin.site.register(CaseLog)