import graphene
from graphene_django import DjangoObjectType
from .models import Track

class TrackType(DjangoObjectType):
    class Meta:
        model=Track

class Query(graphene.ObjectType):
    tracks=graphene.List(TrackType)

    def resolve_tracks(self,info):
        return Track.objects.all()

class CreateTrack(graphene.Mutation):
    tracks=graphene.Field(TrackType)
    class Arguments:
        title=graphene.String()
        description=graphene.String()
        url=graphene.String()

    def mutate(self,info,title,description,url):
        # user=info.context.user or None
        user=info.context.user
        if user.is_anonymous:
            raise Exception("Log in to add track")
        tracks=Track(title=title, description=description, url=url, posted_by=user)
        tracks.save()
        return CreateTrack(tracks=tracks)

class Mutation(graphene.ObjectType):
    create_track=CreateTrack.Field()

