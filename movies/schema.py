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

# Input object types
class ActorInput(graphene.ObjectInput):
    id = graphene.ID()
    name = graphene.String()


class MovieInput(graphene.ObjectInput):
    id = graphene.ID()
    title = graphene.String()
    actors = graphene.List(ActorType)
    year = graphene.Int()


class CreateActor(graphene.Mutation):
    '''
    Add actors to database
    '''
    class Arguments:
        input = ActorInput(required=True)
    
    ok = graphene.Boolean()
    actor = graphene.Field(ActorType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        actor_instance = Actor(name=input.name)
        actor_instance.save()
        return CreateActor(ok=ok, actor=actor_instance)


class UpdateActor(graphene.Mutation):
    '''
    Edit actor entry in the database
    '''
    class Arguments:
        id = graphene.Int(required=True)
        input = ActorInput(required=True)

    ok = graphene.Boolean()
    actor = graphene.Field(ActorType)

    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        actor_instance = Actor.objects.get(pk=id)
        if actor_instance:
            ok = True
            actor_instance.name = input.name
            actor_instance.save()
            return UpdateActor(ok=ok, actor=actor_instance)
        return UpdateActor(ok=ok, actor=None)


class CreateMovie(graphene.Mutation):
    '''
    Add new movie to the database
    ''' 
    class Arguments:
        input = MovieInput(required=True)
    
    ok = graphene.Boolean()
    movie = graphene.Field(MovieType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        actors = []

        for actor_input in input.actors:
            actor = Actor.objects.get(pk=actor_input.id)
            if actor is None:
                return CreateMovie(ok=False, movie=None)
            actors.append(actor)
        
        movie_instance = Movie(
            title=input.title,
            year=input.year
        )
        movie_instance.save()
        movie_instance.actors.set(actors)

        return CreateMovie(ok=True, movie=movie_instance)


class UpdateMovie(graphene.Mutation):
    '''
    Edit movie entry in the database
    '''
    class Arguments:
        id = graphene.ID(required=True)
        input = MovieInput(required=True)

    ok = graphene.Boolean()
    movie = graphene.Field(MovieType)

    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        movie_instance = Movie.objects.get(pk=id)

        if movie_instance:
            ok = True
            actors = []
            for actor_input in input.actors:
                actor = Actor.objects.get(pk=actor_input.id)
                if actor is None:
                    return UpdateMovie(ok=False, movie=None)

                actors.append(actor)

            movie_instance.title=input.title
            movie_instance.year=input.year
            movie_instance.save()
            movie_instance.actors.set(actors)
            return UpdateMovie(ok=ok, movie=movie_instance)

        return UpdateMovie(ok=False, movie=None)


class Mutation(graphene.ObjectType):
    create_actor = CreateActor.Field()
    update_actor = UpdateActor.Field()
    create_movie = CreateMovie.Field()
    update_movie = UpdateMovie.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
