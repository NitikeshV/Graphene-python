import graphene
from graphene_django import DjangoObjectType
from graphene import relay, ObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django import DjangoListField


from .models import *

class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ("topic",)




class QuestionType(DjangoObjectType):
    class Meta:
        model = Question
        fields = ("question_text","category",)


""" write below two classes to print all questions inside categories """

class CategoryNode(DjangoObjectType):
    class Meta:
        model = Category
        filter_fields = ["topic","category"]
        interfaces = (relay.Node,)


class QuesNode(DjangoObjectType):
    class Meta:
        model = Question
        filter_fields = {"question_text": ['exact'],
                "answer_text" : ['exact']}
        interfaces = (relay.Node,)


""" Default QuerySet """
class QueryQuestionType(DjangoObjectType):
    class Meta:
        model = Question

    @classmethod
    def get_queryset(cls, queryset, info):
        if info.context.user.is_anonymous:
            return queryset.filter(published=True)
        return queryset

""" DjangoListField """

class QuestionListType(DjangoObjectType):
   class Meta:
      model = Question
      fields = ("question_text", "answer_text","category")

""" Custom resolvers """
class CategoryCustomResolver(DjangoObjectType):
    class Meta:
        model = Category
        fields = ("topic",)

    @classmethod
    def get_queryset(cls, queryset, info):
        # Filter out categories that has topic "Colors"
        return queryset.exclude(topic="Colors")



class Query(graphene.ObjectType):
    questions = graphene.List(QuestionType)
    question_by_id = graphene.Field(QuestionType, id=graphene.String())
    all_categories = graphene.List(CategoryType)
    query_ques = graphene.List(QueryQuestionType)
    ques_list_fields = DjangoListField(QuestionListType)
    cat_cust_resolver = DjangoListField(CategoryCustomResolver)

    # Query for questions within category

    cat = relay.Node.Field(CategoryNode)
    all_cat = DjangoFilterConnectionField(CategoryNode)

    ques = relay.Node.Field(QuesNode)
    all_ques = DjangoFilterConnectionField(QuesNode)



    def resolve_questions(root, info, **kwargs):
        # Querying a list
        return Question.objects.all()

    def resolve_question_by_id(root, info, id):
        # Querying a single question
        return Question.objects.get(pk=id)

    def resolve_all_categories(root,info):
        # will print all categories
        return Category.objects.all()

    def resolve_query_ques(root,info):
        return Question.objects.all()

    def resolve_cat_cust_resolver(parent,info):
        return Category.objects.all()


schema = graphene.Schema(query=Query)