import graphene
from graphene_django import DjangoObjectType
from .models import Archivements
from users.schema import UserType
from django.db.models import Q

class ArchivementsType(DjangoObjectType):
    class Meta:
        model = Archivements

class Query(graphene.ObjectType):
    archivements = graphene.List(ArchivementsType, search=graphene.String())
    archivementsById = graphene.Field(ArchivementsType, idArchivement=graphene.Int())

    def resolve_archivements(self, info, search=None, **kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')
        print(user)

        if search == "*":
            filter = Q(posted_by=user)
            return Archivements.objects.filter(filter)[:10]
        else:
            filter = Q(posted_by=user) & Q(degree__icontains=search)
            return Archivements.objects.filter(filter)
        
    def resolve_archivementsById(self, info, idArchivement, **kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')
        print(user)

        filter = (
            Q(posted_by=user) & Q(id = idArchivement)
        )
        return Archivements.objects.filter(filter).first()
    
class CreateArchivement(graphene.Mutation):
    idArchivement = graphene.Int()
    archivement_name = graphene.String()
    year = graphene.Int()
    posted_by = graphene.Field(UserType)

    class Arguments:
        idArchivement = graphene.Int()
        archivement_name = graphene.String()
        year = graphene.Int()

    def mutate(self, info, idArchivement, archivement_name, year):
        if year <= 0:
            raise Exception('El año debe ser positivo')
        
        user = info.context.user or None
        print(user)

        currentArchivement = Archivements.objects.filter(id=idArchivement).first()
        print(currentArchivement)

        archivement = Archivements(
            archivement_name=archivement_name,
            year=year,
            posted_by=user        
        )

        if currentArchivement:
            archivement.id = currentArchivement.id

        archivement.save()

        return CreateArchivement(
            idArchivement=archivement.id,
            archivement_name=archivement.archivement_name,
            year = archivement.year,
            posted_by=archivement.posted_by
        )
    
class DeleteArchivement(graphene.Mutation):
    idArchivement = graphene.Int()

    class Arguments:
        idArchivement = graphene.Int()

    def mutate(self, info,idArchivement):
        user = info.context.user or None

        if user.is_anonymous:
            raise Exception('Not logged in!')
        print (user) 

        currentArchivement = Archivements.objects.filter(id=idArchivement).first()
        print(currentArchivement)

        if not currentArchivement:
            raise Exception('Invalid Archivement id!')
        
        currentArchivement.delete()

        return CreateArchivement(
            idArchivement = idArchivement
        )

class Mutation(graphene.ObjectType):
    create_archivement = CreateArchivement.Field()
    delete_mutation = DeleteArchivement.Field()
        