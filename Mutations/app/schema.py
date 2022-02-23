import graphene
from graphene_django import DjangoObjectType
from graphene_django import DjangoListField
from .models import Category,Pet
from .forms import MyForm,PetForm

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
    def mutate(cls, root,info,topic):
        category = Category(topic=topic)
        category.save()                             # saving new category
        return CategoryMutationAdd(category=category)







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






""" Query """
class Query(graphene.ObjectType):
    all_categories = DjangoListField(CategoryType)

    def resolve_all_categories(root,info):
        return Category.objects.all()


""" Mutation """
class Mutation(graphene.ObjectType):
    add_category = CategoryMutationAdd.Field()
    update_category = CategoryMutationUpdate.Field()
    django_form_mutation_PetForm = PetMutation.Field()
    django_form_mutation_MyForm = MyMutation.Field()









schema = graphene.Schema(query=Query,mutation=Mutation)