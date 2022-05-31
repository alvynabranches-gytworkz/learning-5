import json
from textwrap import indent
import graphene
from datetime import datetime


class User(graphene.ObjectType):
    id = graphene.ID()
    username = graphene.String()
    last_login = graphene.DateTime()

    

class Query(graphene.ObjectType):
    # is_staff = graphene.Boolean()

    # def resolve_is_staff(self, info):
    #     return True

    users = graphene.List(User, first=graphene.Int())

    def resolve_users(self, info, first):
        return [
            User(username="Alice", last_login=datetime.now()),
            User(username="Bob", last_login=datetime.now()),
            User(username="Steven", last_login=datetime.now())
        ][:first]


class CreateUser(graphene.Mutation):
    class Arguments:
        username = graphene.String()

    user = graphene.Field(User)

    def mutate(self, info, username):
        try:
            if info.context.get("is_vip"):
                username = username.upper()
        except Exception as e:
            pass
        user = User(username=username)
        return CreateUser(user=user)


class Mutations(graphene.ObjectType):
    create_user = CreateUser.Field()

schema = graphene.Schema(query=Query, mutation=Mutations) # , auto_camelcase=False

# result = schema.execute(
#     """
#     {
#         is_staff
#     }
#     """
# )

# result = schema.execute(
#     """
#     {
#         users(first: 1) {
#             username
#             last_login
#         }
#     }
#     """
# )

result = schema.execute(
    """
    mutation createUser {
        createUser(username: "Bob") {
            user {
                username
            }
        }
    }
    """
)

result = schema.execute(
    """
    mutation createUser($username: String) {
        createUser(username: $username) {
            user {
                username
            }
        }
    }
    """, 
    variable_values={"username": "Bob"}, 
    context = {"is_vip": False}
)

print(json.dumps(result.data, indent=4))