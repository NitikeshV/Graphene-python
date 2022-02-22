import graphene
from graphene import relay, ObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from .models import *

class CategoryNode(DjangoObjectType):
    class Meta:
        model = Category
        filter_fields = ['name', 'ingredients']         # The filter_fields parameter is used to specify the fields which can be filtered upon. The value specified here is passed directly to django-filter
        interfaces = (relay.Node, )

class IngredientNode(DjangoObjectType):
    class Meta:
        model = Ingredient
        # Allow for some more advanced filtering here
        filter_fields = {                                       # The filter_fields parameter is used to specify the fields which can be filtered upon. The value specified here is passed directly to django-filter
            'name': ['exact', 'icontains', 'istartswith'],
            'notes': ['exact', 'icontains'],
            'category': ['exact'],
            'category__name': ['exact'],
        }
        interfaces = (relay.Node, )

class Query(graphene.ObjectType):
    category = relay.Node.Field(CategoryNode)                   # specific category
    all_categories = DjangoFilterConnectionField(CategoryNode)      # list all categories

    ingredients = relay.Node.Field(IngredientNode)                  # specific ingredient
    all_ingredients = DjangoFilterConnectionField(IngredientNode)       # list all ingredients


""" Note that the above Query class is marked as ‘abstract’. This is because we will now create a project-level query which will combine all our app-level queries. """

schema = graphene.Schema(query=Query)