MUTATION

With Graphene-Django we can take advantage of pre-existing Django features to quickly build CRUD functionality, while still
using the core graphene mutation features to add custom mutations to a Django project.

1) Simple Example

            * create model, register, migrate

                            """"
                                class Category(models.Model):
                                    topic = models.CharField(max_length=250)

                                    def __str__(self):
                                        return self.topic
                            """"

            * write schema

                            """"
                                class CategoryType(DjangoObjectType):
                                    class Meta:
                                        model = Category
                                        fields = ("topic",)
                            """"

            * add mutations

                        ( adding new Category )

                                    """"
                                        class CategoryMutationAdd(graphene.Mutation):
                                            class Arguments:
                                                topic = graphene.String(required=True)       # passing all the arguments present in the
                                                                                                        particular model to fetch data
                                            category = graphene.Field(CategoryType)         # connecting to the schema field

                                            @classmethod
                                            def mutate(cls, root,info,topic):
                                                category = Category(topic=topic)
                                                category.save()                             # saving new category
                                                return CategoryMutationAdd(category=category)
                                    """"

                        ( updating existing elements in the Category Field )

                                    """"
                                        class CategoryMutationUpdate(graphene.Mutation):
                                            class Arguments:
                                                id = graphene.ID()
                                                topic = graphene.String(required=True)

                                            category = graphene.Field(CategoryType)

                                            @classmethod
                                            def mutate(cls,root,info,topic,id):
                                                category = Category.objects.get(pk=id)
                                                category.topic = topic
                                                category.save()

                                                return CategoryMutationUpdate(category=category)
                                    """"

            * register your mutations

                             """"
                                class Mutation(graphene.ObjectType):
                                    add_category = CategoryMutationAdd.Field()
                                    update_category = CategoryMutationUpdate.Field()
                             """"


                ( run query to add category )

                            """"
                                mutation
                                    {
                                      addCategory(topic:"<category_name>"){
                                        category{
                                          topic
                                          id
                                        }
                                      }
                                    }
                            """"

                ( run query to update category )
                            """"
                                mutation{
                                  updateCategory(id:4,topic:"laguages"){
                                    category{
                                      topic
                                    }
                                  }
                                }
                            """"

2) Django Forms

            * DjangoFormMutation ( without model )

                            Graphene-Django comes with mutation classes that will convert the
                            fields on Django forms into inputs on a mutation.

                                    """"
                                        from graphene_django.forms.mutation import DjangoFormMutation

                                            class MyForm(forms.Form):
                                                name = forms.CharField()

                                            class MyMutation(DjangoFormMutation):
                                                class Meta:
                                                    form_class = MyForm
                                    """"

                            * create mutation object
                                       'django_form_mutation_MyForm = MyMutation.Field()''


                             Note: but this will require a save attribute for form

                                    ( query : )

                                            """"
                                                 mutation{
                                                    djangoFormMutationMyform(input:{name:"Meow",}) {
                                                      name
                                                    }
                                                  }
                                            """"

            * DjangoModelFormMutation ( with model )

                            DjangoModelFormMutation will pull the fields from a ModelForm.

                            1) create model
                                        """"
                                            class Pet(models.Model):
                                                name = models.CharField(max_length=100)

                                                def __str__(self):
                                                    return self.name
                                        """"

                            2) create form
                                        """"
                                            class PetForm(forms.ModelForm):
                                                class Meta:
                                                    model = Pet
                                                    fields = ("name",)
                                        """"

                            3) write schema
                                        """"
                                            class PetType(DjangoObjectType):
                                                class Meta:
                                                    model = Pet
                                        """"

                            4) write mutation
                                        """"
                                            class PetMutation(DjangoModelFormMutation):
                                                pet = (PetType)
                                                class Meta:
                                                    form_class = PetForm
                                        """"
                            5) create mutation object
                                        ' django_form_mutation_PetForm = PetMutation.Field() '


                            (( PetMutation will grab the fields from PetForm and turn them into inputs.
                                If the form is valid then the mutation will lookup the DjangoObjectType for the Pet model and
                                return that under the key pet. Otherwise it will return a list of errors. ))



                            ( run query to create new object of Pet )
                                        """"
                                             mutation{
                                                djangoFormMutationPetform(input:{name:"Meow",}) {
                                                pet{
                                                  name
                                                }
                                              }
                                            }
                                        """"

                            You can change the input name (default is input) and the return field name (default is the model name lowercase).

                                        """"
                                            class PetMutation(DjangoModelFormMutation):
                                                class Meta:
                                                    form_class = PetForm
                                                    input_field_name = 'data'
                                                    return_field_name = 'my_pet'
                                        """"


            * Form Validation

                             Form mutations will call is_valid() on your forms.

                             If the form is valid then the class method perform_mutate(form, info) is called on the mutation.
                              Override this method to change how the form is saved or to return a different Graphene object type.

                             If the form is not valid then a list of errors will be returned. These errors have two fields:
                             field, a string containing the name of the invalid form field, and messages, a list of strings with the validation messages.

