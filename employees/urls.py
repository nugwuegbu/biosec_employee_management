from django.urls import path
from employees import views


urlpatterns = [
    path('',views.home,name='home'),
    path('new-staff',views.create,name="new-staff"),
    path('store',views.store),
    path('list', views.employee_list),
    path('update/<str:id>', views.update_employee),
    path('create', views.add_employee),
    path('delete/<str:id>',views.employee_delete),
    path('archive/<str:id>',views.archive),
    path('update-record/<str:id>',views.update),
    path('store-update/<str:id>',views.store_update,name="update"),
    path('logs',views.getlogs,name='logs'),
]