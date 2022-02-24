from django.urls import path
from . import views
app_name = "app"

urlpatterns =[
    path("api/",views.ProductDRFListView.as_view(),name="app_home"),
    path("api/<slug:slug>/", views.ProductDRF.as_view(),name='product'),
]