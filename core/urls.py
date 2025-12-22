from django.urls import path
from .views import home, delete_task, toggle_task,signup

urlpatterns = [
    path("", home, name='home'),
    path('signup/',signup,name='signup'),
    path('delete/<int:item_id>/',delete_task, name='delete_task' ),
    path('toggle/<int:item_id>/',toggle_task, name='toggle_task'),
]