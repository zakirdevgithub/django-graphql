import graphene
from graphene_django import DjangoObjectType
from .models import Track,Like
from users.schema import UserType
from django.db.models import Q

class TrackType(DjangoObjectType):
    class Meta:
        model=Track

class LikeType(DjangoObjectType):
    class Meta:
        model=Like

class Query(graphene.ObjectType):
    tracks=graphene.List(TrackType, search=graphene.String())
    likes=graphene.List(LikeType)

    def resolve_tracks(self,info, search=None):
        if search:
            # return Track.objects.filter(title__startswith=search)
            # return Track.objects.filter(title__endswith=search)
            # return Track.objects.filter(title__contains=search)
            # return Track.objects.filter(title__icontains=search)
            filter=(
                Q(title__icontains=search)|
                Q(description__icontains=search)|
                Q(url__icontains=search)|
                Q(posted_by__username__icontains=search)

            )
            return Track.objects.filter(filter)
        return Track.objects.all()
    
    def resolve_likes(self,info):
        return Like.objects.all()

class CreateTrack(graphene.Mutation):
    track=graphene.Field(TrackType)
    class Arguments:
        title=graphene.String()
        description=graphene.String()
        url=graphene.String()

    def mutate(self,info,title,description,url):
        user=info.context.user
        if user.is_anonymous:
            raise Exception("Log in to create Track")
        track=Track(title=title, description=description, url=url, posted_by=user)
        track.save()
        return CreateTrack(track=track)

class UpdateTrack(graphene.Mutation):
    track=graphene.Field(TrackType)
    class Arguments:
        track_id=graphene.Int(required=True)
        title=graphene.String()
        description=graphene.String()
        url=graphene.String()
    
    def mutate(self,info,title,description,url,track_id):
        user=info.context.user
        if user.is_anonymous:
            raise Exception("Log in to update")
        track=Track.objects.get(id=track_id)
        if track.posted_by !=user:
            raise Exception("You not permitted to update")
        track.title=title
        track.description=description
        track.url=url
        track.save()
        return UpdateTrack(track=track)

class DeleteTrack(graphene.Mutation):
    track_id=graphene.Int()
    class Arguments:
        track_id=graphene.Int(required=True)

    def mutate(self,info,track_id):
        user=info.context.user
        if user.is_anonymous:
            raise Exception("Log in to delete")
        track=Track.objects.get(id=track_id)
        if track.posted_by !=user:
            raise Exception("You are not permitted to delete")
        track.delete()
        return DeleteTrack(track_id=track_id)

class CreateLike(graphene.Mutation):
    user=graphene.Field(UserType)
    track=graphene.Field(TrackType)
    class Arguments:
        track_id=graphene.Int(required=True)
    
    def mutate(self,info,track_id):
        user=info.context.user
        if user.is_anonymous:
            raise Exception("Log in to like")

        track=Track.objects.get(id=track_id)
        if not track:
            raise Exception("Track not found with this id")

        Like.objects.create(
            user=user,
            track=track
        )

        return CreateLike(user=user, track=track)


class Mutation(graphene.ObjectType):
    create_track=CreateTrack.Field()
    update_track=UpdateTrack.Field()
    delete_track=DeleteTrack.Field()
    create_like=CreateLike.Field()