<h1> Queries & ObjectTypes </h1>

Graphene-Django offers a host of features for performing GraphQL queries.

Graphene-Django ships with a special DjangoObjectType that automatically transforms a Django Model into a ObjectType for you.

* Specifying which fields to include

                By default, DjangoObjectType will present all fields on a Model through GraphQL.
                If you only want a subset of fields to be present, you can do so using fields or exclude.

             1) fields

                        * Show only these fields on the model:

                                    """"
                                        from graphene_django import DjangoObjectType
                                            from .models import Question

                                            class QuestionType(DjangoObjectType):
                                                class Meta:
                                                    model = Question
                                                    fields = ("id", "question_text")
                                    """"

                                   (run query)
                                            """"
                                            query {
                                              questions{
                                                id
                                                questionText
                                              }
                                            }
                                            """"


                        * show  me all fields on the model

                                    """"
                                        class QuestionType(DjangoObjectType):
                                            class Meta:
                                                model = Question
                                                fields = "__all__"
                                    """"

                                    (run query)
                                            """"
                                            query {
                                              questions{
                                                id
                                                questionText
                                                answerText
                                              }
                                            }
                                            """"

                        * Show all fields except those in exclude:

                                    """"
                                        class QuestionType(DjangoObjectType):
                                            class Meta:
                                                model = Question
                                                exclude = ("question_text",)
                                    """"

                                    (run query)
                                            """"
                                            query {
                                              questions{
                                                id
                                                answerText
                                              }
                                            }
                                            """"

             2) Customising fields

                        You can completely overwrite a field, or add new fields, to a DjangoObjectType using a Resolver:

                                """"
                                    class QuestionType(DjangoObjectType):
                                        class Meta:
                                            model = Question
                                            fields = ("id", "question_text")

                                        extra_field = graphene.String()

                                        def resolve_extra_field(self, info):
                                            return "hello!"
                                """"

                                ( run query )
                                        """"
                                            query {
                                              questions{
                                                id
                                                questionText
                                                extraField
                                              }
                                            }
                                        """"

             3) Related Models

                        lets say you have the following models connected using foreignkey

                                    """"
                                        class Category(models.Model):
                                            topic = models.CharField(max_length=250)
                                            def __str__(self):
                                                return self.topic

                                        class Question(models.Model):
                                            question_text = models.TextField()
                                            answer_text = models.TextField(max_length=150, null=False, default='')
                                            category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                                                            related_name='category',null=True )
                                            def __str__(self):
                                                return self.question_text
                                    """"

                        in schema file, When Question is published as a DjangoObjectType and you want to add Category as a query-able field like so:

                                    """"
                                        class QuestionType(DjangoObjectType):
                                            class Meta:
                                                model = Question
                                                fields = ("question_text","category",)
                                    """"

                        Then all query-able related models must be defined as DjangoObjectType subclass, or they will fail to show
                        if you are trying to query those relation fields. You only need to create the most basic class for this to work:

                                    """"
                                        class CategoryType(DjangoObjectType):
                                            class Meta:
                                                model = Category
                                                fields = ("topic",)
                                    """"


                            (run below query to print all categories )
                                    """"
                                        query{
                                          allCategories{
                                            topic
                                          }
                                        }
                                    """"

                            ( run below query to print all questions with its category )
                                    """"
                                        query{
                                          questions{
                                            questionText
                                                category{
                                              topic
                                            }
                                          }
                                        }
                                    """"

                        to print all questions of a particular category, we need to use relay and graphene django-filters
                                   * pip install django-filters
                                   * import the following in schema
                                            from graphene import relay, ObjectType
                                            from graphene_django.filter import DjangoFilterConnectionField
                                   * write schema
                                            """"
                                                class CategoryNode(DjangoObjectType):
                                                    class Meta:
                                                        model = Category
                                                        # we defined "category" as the related name for Category in Question model
                                                        filter_fields = ["topic","category"]
                                                        interfaces = (relay.Node,)

                                                class QuesNode(DjangoObjectType):
                                                    class Meta:
                                                        model = Question
                                                        filter_fields = {"question_text": ['exact'],
                                                                "answer_text" : ['exact']}
                                                        interfaces = (relay.Node,)
                                            """"

                                   * write query
                                            """"
                                                cat = relay.Node.Field(CategoryNode)
                                                all_cat = DjangoFilterConnectionField(CategoryNode)

                                                ques = relay.Node.Field(QuesNode)
                                                all_ques = DjangoFilterConnectionField(QuesNode)
                                            """"

                               ( run query )
                                        """"
                                            query{
                                              allCat{
                                                edges{
                                                  node{
                                                    topic
                                                    category{
                                                      edges{
                                                        node{
                                                          questionText
                                                          answerText
                                                        }
                                                      }
                                                    }
                                                  }
                                                }
                                              }
                                            }
                                        """"

             4) Default QuerySet

                        If you are using DjangoObjectType you can define a custom get_queryset method. Use this to control
                        filtering on the ObjectType level instead of the Query object level.

                        """"
                            class QueryQuestionType(DjangoObjectType):
                                class Meta:
                                    model = Question

                                @classmethod
                                def get_queryset(cls, queryset, info):
                                    if info.context.user.is_anonymous:
                                        return queryset.filter(published=True)
                                    return queryset
                        """"

                        add query object and resolve function

                        ( run query; this will print all the questions and answers inside queryQues )
                                """"
                                    query{
                                      queryQues{
                                        questionText
                                        answerText
                                        category {
                                          id
                                        }
                                      }
                                    }
                                """"

             5) Resolvers

                        When a GraphQL query is received by the Schema object, it will map it to a “Resolver” related to it.

                        This resolve method should follow this format:
                                    "def resolve_foo(parent, info, **kwargs):"

                        “foo” is the name of the field declared in the Query object.
                                    """"
                                        class Query(graphene.ObjectType):
                                            foo = graphene.List(QuestionType)

                                            def resolve_foo(root, info, **kwargs):
                                                id = kwargs.get("id")
                                                return Question.objects.get(id)
                                    """"

                        ** Arguments

                                    Additionally, Resolvers will receive any arguments declared in the field definition.
                                    This allows you to provide input arguments in your GraphQL server and can be useful for custom queries.

                                                """"
                                                    class Query(graphene.ObjectType):
                                                        question = graphene.Field(
                                                            QuestionType,
                                                            foo=graphene.String(),
                                                            bar=graphene.Int()
                                                        )

                                                        def resolve_question(root, info, foo, bar):
                                                            # If `foo` or `bar` are declared in the GraphQL query they will be here, else None.
                                                            return Question.objects.filter(foo=foo, bar=bar).first()
                                                """"
                        ** Info
                                    The info argument passed to all resolve methods holds some useful information.
                                    For Graphene-Django, the info.context attribute is the HTTPRequest object that would be familiar to any
                                    Django developer. This gives you the full functionality of Django’s HTTPRequest in your resolve methods,
                                    such as checking for authenticated users:

                                                """"
                                                    class Query(graphene.ObjectType):
                                                        questions = graphene.List(QuestionType)

                                                    def resolve_questions(root, info):
                                                        # See if a user is authenticated
                                                        if info.context.user.is_authenticated():
                                                            return Question.objects.all()
                                                        else:
                                                            return Question.objects.none()
                                                """"

             6) DjangoListField (similar to graphene.List)

                        DjangoListField allows you to define a list of DjangoObjectType‘s. By default it will resolve
                        the default queryset of the Django model.

                                    """"
                                        from graphene_django import DjangoListField

                                        class QuestionListType(DjangoObjectType):
                                           class Meta:
                                              model = Question
                                              fields = ("question_text", "answer_text","category")

                                        class Query(ObjectType):
                                           recipes = DjangoListField(QuestionListType)
                                    """"

             7) Custom Resolvers

                        If your DjangoObjectType has defined a custom get_queryset method, when resolving a DjangoListField
                        it will be called with either the return of the field resolver (if one is defined) or
                        the default queryset from the Django model.

                        For example the following schema will resolve all categories except topic = "Colors" :

                                """"
                                    class CategoryCustomResolver(DjangoObjectType):
                                        class Meta:
                                            model = Category
                                            fields = ("topic",)

                                        @classmethod
                                        def get_queryset(cls, queryset, info):
                                            # Filter out categories that has topic "Colors"
                                            return queryset.exclude(topic="Colors")
                                """"






