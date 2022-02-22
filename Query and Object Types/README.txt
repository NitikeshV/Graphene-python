<h1> Queries & ObjectTypes </h1>

Graphene-Django offers a host of features for performing GraphQL queries.

Graphene-Django ships with a special DjangoObjectType that automatically transforms a Django Model into a ObjectType for you.

* Specifying which fields to include

                By default, DjangoObjectType will present all fields on a Model through GraphQL. If you only want a subset of fields to be present, you can do so using fields or exclude.

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







