from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('todolist/', include(('todolist.urls', 'todolist'), namespace='todolist')),
    path('translator/', include(('translator.urls', 'translator'), namespace='translator')),
    path('', include(('base.urls', 'base'), namespace='base')),
]
