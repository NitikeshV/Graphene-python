"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from graphene_django.views import GraphQLView

"""
    If you have enabled CSRF protection in your Django app you will find that it prevents your API clients from POSTing to the graphql endpoint.
    You can either update your API client to pass the CSRF token with each request
    or you can exempt your Graphql endpoint from CSRF protection by wrapping the GraphQLView with the csrf_exempt decorator
"""

from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('admin/', admin.site.urls),
    path("graphql",csrf_exempt(GraphQLView.as_view(graphiql=True))),

]
