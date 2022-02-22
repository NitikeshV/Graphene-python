import graphene
from graphene_django import DjangoObjectType
from .models import *


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = "__all__"



class QuestionType(DjangoObjectType):
    class Meta:
        model = Question
        fields = ("id", "question_text")

    extra_field = graphene.String()

    def resolve_extra_field(self, info):
        return "hello!"





class Query(graphene.ObjectType):
    questions = graphene.List(QuestionType)
    question_by_id = graphene.Field(QuestionType, id=graphene.String())
    categories = graphene.List(CategoryType)

    def resolve_questions(root, info, **kwargs):
        # Querying a list
        return Question.objects.all()

    def resolve_question_by_id(root, info, id):
        # Querying a single question
        return Question.objects.get(pk=id)

    def resolve_categories(root,info):
        return Category.objects.all()


schema = graphene.Schema(query=Query)