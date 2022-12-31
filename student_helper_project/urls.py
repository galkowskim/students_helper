from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('todolist/', include(('todolist.urls', 'todolist'), namespace='todolist')),
    path('', include(('base.urls', 'base'), namespace='base')),
]
