from django.urls import path
from .views import MainPageToDoList, TaskDetail, TaskCreate, TaskUpdate, TaskDelete, ProjectCreate, ProjectDetail, ProjectUpdate, ProjectDelete

urlpatterns = [
    path('', MainPageToDoList.as_view(), name='tasks'),
    path('task/<int:pk>/', TaskDetail.as_view(), name='task'),
    path('task-create/', TaskCreate.as_view(), name='task-create'),
    path('task-update/<int:pk>/', TaskUpdate.as_view(), name='task-update'),
    path('task-delete/<int:pk>/', TaskDelete.as_view(), name='task-delete'),
    path('project/<int:pk>/', ProjectDetail.as_view(), name='project'),
    path('project-create/', ProjectCreate.as_view(), name='project-create'),
    path('project-update/<int:pk>/', ProjectUpdate.as_view(), name='project-update'),
    path('project-delete/<int:pk>/', ProjectDelete.as_view(), name='project-delete'),
]