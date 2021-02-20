import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model

class UserType(DjangoObjectType):
    class Meta:
        model=get_user_model()

#-------------For All Users--------
# class Query(graphene.ObjectType):
#     users=graphene.List(UserType)
#     def resolve_users(self,info):
#         return get_user_model().objects.all()

#-------------Query with Id-----------
class Query(graphene.ObjectType):
    users=graphene.Field(UserType, id=graphene.Int(required=True))
    

    def resolve_users(self, info, id):
        user=info.context.user
        if user.is_anonymous:
            raise Exception("Not Logged in")
        return get_user_model().objects.get(id=id)





class CreateUser(graphene.Mutation):
    user=graphene.Field(UserType)
    class Arguments:
        username=graphene.String(required=True)
        email=graphene.String(required=True)
        password=graphene.String(required=True)

    def mutate(self,info,username, email, password):
        user=get_user_model()(username=username, email=email)
        user.set_password(password)
        user.save()
        return CreateUser(user=user)


class Mutation(graphene.ObjectType):
    create_user=CreateUser.Field()