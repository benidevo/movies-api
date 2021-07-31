import graphene
from graphene_django.types import ObjectType, DjangoObjectType

from movies.models import Movie, Actor

# Create a GraphQL type for the Actor model
class ActorType(DjangoObjectType):
    class Meta:
        model = Actor


# Create a GraphQL type for the Movie model
class MovieType(DjangoObjectType):
    class Meta:
        model = Movie


class Query(ObjectType):
    '''
    Query Movies and Actors in the database
    '''
    actor = graphene.Field(ActorType, id=graphene.Int())
    movie = graphene.Field(MovieType, id=graphene.Int())
    actors = graphene.List(ActorType)
    movies = graphene.List(MovieType)

    def resolve_actor(self, info, **kwargs):
        '''
        Get an actor by ID
        '''
        id = kwargs.get('id')

        if id is not None:
            return Actor.objects.get(pk=id)

        return None
    
    def resolve_movie(self, inf0, **kwargs):
        '''
        Get a movie by ID
        '''
        id = kwargs.get('id')

        if id is not None:
            return Movie.objects.get(pk=id)

        return None

    def resolve_actors(self, inf0, **kwargs):
        '''
        get all actors
        '''
        return Actor.objects.all()

    def resolve_movies(self, inf0, **kwargs):
        '''
        get all movies
        '''
        return Movie.objects.all()
        