import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model

class UserType(DjangoObjectType):
    class Meta:
        model=get_user_model()

class Query(graphene.ObjectType):
    user=graphene.Field(UserType, id=graphene.Int(required=True))
    me=graphene.Field(UserType)

    def resolve_me(self,info):
        user=info.context.user
        if user.is_anonymous:
            raise Exception("Not Logged In")
        return user
    
    def resolve_user(self, info, id):
        return get_user_model().objects.get(id=id)

class CreateUser(graphene.Mutation):
    user=graphene.Field(UserType)
    class Arguments:
        username=graphene.String(required=True)
        email=graphene.String(required=True)
        password=graphene.String(required=True)

    def mutate(self, info, username, email, password):
        user=get_user_model()(
            username=username,
            email=email
        )
        user.set_password(password)
        user.save()
        return CreateUser(user=user)

class Mutation(graphene.ObjectType):
    create_user=CreateUser.Field()