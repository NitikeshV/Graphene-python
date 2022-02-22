<h1>Relay</h1>

Graphene has complete support for Relay and offers some utils to make integration from Python easy.
*Nodes

           A Node is an Interface provided by graphene.relay that contains a single field id (which is a ID!).
           Any object that inherits from it has to implement a get_node method for retrieving a Node by an id.<br><br>

            1) example :
                        class Ship(graphene.ObjectType):
                        '''A ship in the Star Wars saga'''
                        class Meta:
                            interfaces = (relay.Node, )

                        name = graphene.String(description='The name of the ship.')

                        @classmethod
                        def get_node(cls, info, id):
                            return get_ship(id)

             The id returned by the Ship type when you query it will be a scalar which contains enough info for the server to know its type and its id.

            2) Custom Nodes

                        You can use the predefined relay.Node or you can subclass it, defining custom ways of
                        how a node id is encoded (using the to_global_id method in the class) or how we can retrieve a Node
                        given a encoded id (with the get_node_from_global_id method).

                        example:  """"
                                        class CustomNode(Node):
                                            class Meta:
                                                name = 'Node'

                                            @staticmethod
                                            def to_global_id(type_, id):
                                                return f"{type_}:{id}"

                                            @staticmethod
                                            def get_node_from_global_id(info, global_id, only_type=None):
                                                type_, id = global_id.split(':')
                                                if only_type:
                                                    # We assure that the node type that we want to retrieve
                                                    # is the same that was indicated in the field type
                                                    assert type_ == only_type._meta.name, 'Received not compatible node.'

                                                if type_ == 'User':
                                                    return get_user(id)
                                                elif type_ == 'Photo':
                                                    return get_photo(id)


                        ( The get_node_from_global_id method will be called when CustomNode.Field is resolved. )

            3) Accessing node types

                            If we want to retrieve node instances from a global_id (scalar that identifies an instance
                            by it’s type name and id), we can simply do Node.get_node_from_global_id(info, global_id).

                            In the case we want to restrict the instance retrieval to a specific type, we can do:
                            Node.get_node_from_global_id(info, global_id, only_type=Ship). This will raise an error
                            if the global_id doesn’t correspond to a Ship type.

            4) Node Root field

                            As is required in the Relay specification, the server must implement a root
                            field called node that returns a Node Interface.
                            For this reason, graphene provides the field relay.Node.Field, which links to any type
                            in the Schema which implements Node. Example usage:

                                        """"
                                            class Query(graphene.ObjectType):
                                                # Should be CustomNode.Field() if we want to use our custom Node.
                                                node = relay.Node.Field()
                                        """"


* Connections

            A connection is a vitaminized version of a List that provides ways of slicing and paginating through it.
            The way you create Connection types in graphene is using relay.Connection and relay.ConnectionField.

            1) Quick example

                            If we want to create a custom Connection on a given node, we have to subclass the Connection class.
                            In the following example, extra will be an extra field in the connection,
                            and other an extra field in the Connection Edge.

                                        """"
                                            class ShipConnection(Connection):
                                                extra = String()

                                                class Meta:
                                                    node = Ship

                                                class Edge:
                                                    other = String()
                                        """"

                            The ShipConnection connection class, will have automatically a pageInfo field,
                            and a edges field (which is a list of ShipConnection.Edge). This Edge will have a node field
                            linking to the specified node (in ShipConnection.Meta) and the field other that we defined in the class.

            2) Connection Field

                            You can create connection fields in any Connection, in case any ObjectType that
                            implements Node will have a default Connection.

                            """"
                                class Faction(graphene.ObjectType):
                                    name = graphene.String()
                                    ships = relay.ConnectionField(ShipConnection)

                                    def resolve_ships(root, info):
                                        return []
                            """"


* Mutations

            Most APIs don’t just allow you to read data, they also allow you to write.

            In GraphQL, this is done using mutations. Just like queries, Relay puts some additional requirements on
            mutations, but Graphene nicely manages that for you. All you need to do is make your mutation a subclass of relay.ClientIDMutation.

                        """"
                            class IntroduceShip(relay.ClientIDMutation):
                                class Input:
                                    ship_name = graphene.String(required=True)
                                    faction_id = graphene.String(required=True)

                                ship = graphene.Field(Ship)
                                faction = graphene.Field(Faction)

                                @classmethod
                                def mutate_and_get_payload(cls, root, info, **input):
                                    ship_name = input.ship_name
                                    faction_id = input.faction_id
                                    ship = create_ship(ship_name, faction_id)
                                    faction = get_faction(faction_id)
                                    return IntroduceShip(ship=ship, faction=faction)
                        """"
            1) Accepting Files

                        Mutations can also accept files, that’s how it will work with different integrations:

                        """"
                            class UploadFile(graphene.ClientIDMutation):
                                 class Input:
                                     pass
                                     # nothing needed for uploading file

                                 # your return fields
                                 success = graphene.String()

                                @classmethod
                                def mutate_and_get_payload(cls, root, info, **input):
                                    # When using it in Django, context will be the request
                                    files = info.context.FILES
                                    # Or, if used in Flask, context will be the flask global request
                                    # files = context.files

                                    # do something with files

                                    return UploadFile(success=True)
                        """"




1) create project, app, models, register and migrate
3) pip install django-filter ( bcoz we are using this library in our schema)
2) write schema
        ( Note that the above Query class is marked as ‘abstract’. This is because we will now create a
        project-level query which will combine all our app-level queries.)

3) create a parent project-level schema.py and  write in it
4) update settings
        add 'graphene_django' in settings
        add GRAPHENE dictionary
5) write url for graphql
6) test your graphql schema

7) run query
            """"
                query{
                  allIngredients{
                    edges{
                      node{
                        id
                        name
                      }
                    }

                  }
                }
            """"

            The above will return the names & IDs for all ingredients. But perhaps you want a specific ingredient:

            """"
                query {
                  ingredients(id: "SW5ncmVkaWVudE5vZGU6MQ==") {                     # Graphene creates globally unique IDs for all objects. You may need to copy this value from the results of the first query
                    name
                  }
                }
            """"

            You can also get each ingredient for each category:

            """"
                query {
                  allCategories {
                    edges {
                      node {
                        name,
                        ingredients {
                          edges {
                            node {
                              name
                            }
                          }
                        }
                      }
                    }
                  }
                }
            """"

            Or you can get only ‘Dairy’ ingredients containing the letter ‘b’:

            """"
                query {
                  # You can also use `category: "CATEGORY GLOBAL ID"`
                  allIngredients(name_Icontains: "b", category_Name: "Dairy") {
                    edges {
                      node {
                        name
                      }
                    }
                  }
                }

8) We have created a GraphQL endpoint that will work with Relay, but for Relay to work it needs access to a (non python) schema. Instructions to export the schema can be found on the "Introspection Schema" part of this guide.





