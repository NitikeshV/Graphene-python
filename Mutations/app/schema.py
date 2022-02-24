import graphene
from graphene_django import DjangoObjectType
from graphene_django import DjangoListField
from .models import Category,Pet,Product
from .forms import MyForm,PetForm
from .serializers import ProductSerializer
from graphene_django.rest_framework.mutation import SerializerMutation
from graphene import relay
from graphql_relay import from_global_id

from graphene_django.forms.mutation import DjangoFormMutation, DjangoModelFormMutation



class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ("topic","id",)

""" adding new Category """

class CategoryMutationAdd(graphene.Mutation):
    class Arguments:
        topic = graphene.String(required=True)         # passing all the arguments present in the particular model to fetch data

    category = graphene.Field(CategoryType)         # connecting to the schema field

    @classmethod
    def mutate(cls, root,info,topic):
        category = Category(topic=topic)
        category.save()                             # saving new category
        return CategoryMutationAdd(category=category)


""" updating existing elements in the Category Field """

class CategoryMutationUpdate(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        topic = graphene.String(required=True)

    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls, root,info,topic,id):
        category = Category.objects.get(id=id)
        category.topic = topic
        category.save()                             # saving new category
        return CategoryMutationUpdate(category=category)



""" DjangoModelFormMutation """
class PetType(DjangoObjectType):
    class Meta:
        model = Pet

class PetMutation(DjangoModelFormMutation):
    pet = (PetType)
    class Meta:
        form_class = PetForm


""" DjangoFormMutation """
class MyMutation(DjangoFormMutation):
    class Meta:
        form_class = MyForm


""" Django REST Framework """
class MyProductMutation(SerializerMutation):
    class Meta:
        serializer_class = ProductSerializer
        model_operations = ['create', 'update']
        lookup_field = 'id'


""" Django REST Framework - Overriding Update Queries """
class MyProductMutationOverriding(SerializerMutation):
    class Meta:
        serializer_class = ProductSerializer

    @classmethod
    def get_serializer_kwargs(cls, root, info, **input):
        if 'id' in input:
            instance = Product.objects.filter(
                id=input['id'],
            ).first()
            if instance:
                return {'instance': instance, 'data': input, 'partial': True}

            else:
                raise http.Http404

        return {'data': input, 'partial': True}


""" Relay (similar to add new category class) """

class CategoryRelay(relay.ClientIDMutation):
    class Input:
        topic = graphene.String(required=True)
        id = graphene.String()

    category = graphene.Field(CategoryType)

    @classmethod
    def mutate_and_get_payload(cls, root,info,topic,id):
        try:
            print("*"*50)
            print(id)
       
            print(from_global_id(id))
            category = Category.objects.get(pk=from_global_id(id)[1])
        except Exception as e:
            print("Exception:- ",e)

        category = Category.objects.get(pk=from_global_id(id)[1])
        category.topic=topic
        category.save()
        return CategoryMutationAdd(category=category)
   

class CategoryNode(DjangoObjectType):
    class Meta:
        model = Category
        interfaces = (relay.Node, )


""" Query """
class Query(graphene.ObjectType):
    #all_categories = DjangoListField(CategoryType)
    all_categories = DjangoListField(CategoryNode)

    def resolve_all_categories(root,info):
        return Category.objects.all()


""" Mutation """
class Mutation(graphene.ObjectType):
    add_category = CategoryMutationAdd.Field()
    update_category = CategoryMutationUpdate.Field()
    django_form_mutation_PetForm = PetMutation.Field()
    django_form_mutation_MyForm = MyMutation.Field()
    my_product_mutation = MyProductMutation.Field()
    my_product_mutation_overriding = MyProductMutationOverriding.Field()
    relay_category = CategoryRelay.Field()









schema = graphene.Schema(query=Query,mutation=Mutation)
