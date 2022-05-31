import graphene
from datetime import datetime

class User(graphene.ObjectType):
    id = graphene.ID()
    username = graphene.String()
    last_login = graphene.DateTime()

    def resolve_users(self, info):
        return [
            User(username="Alice", last_login=datetime.now()),
            User(username="Bob", last_login=datetime.now()),
            User(username="Steven", last_login=datetime.now())
        ]

class Query(graphene.ObjectType):
    is_staff = graphene.Boolean()

    def resolve_is_staff(self, info):
        return True


schema = graphene.Schema(query=Query, auto_camelcase=False)

# result = schema.execute(
#     """
#     {
#         is_staff
#     }
#     """
# )

result = schema.execute(
    """
    {
        users {
            username
            last_login
        }
    }
    """
)

print(result.data.items())