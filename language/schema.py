import graphene
from graphene_django import DjangoObjectType
from .models import Language
from users.schema import UserType
from django.db.models import Q

class LanguageType(DjangoObjectType):
    class Meta:
        model = Language

class Query(graphene.ObjectType):
    languages = graphene.List(LanguageType, search=graphene.String(required=False))
    languageById = graphene.Field(LanguageType, idLanguage=graphene.Int())

    def resolve_languages(self, info, search=None, **kwargs):
        user = info.context.user 
        if user.is_anonymous:
            raise Exception('Not logged in!')
        print(user)

        if search == "*":
            filter = Q(posted_by=user)
            return Language.objects.filter(filter)[:10]
        else:
            filter = Q(posted_by=user) & Q(language__icontains=search)
            return Language.objects.filter(filter)
        
    def resolve_languageById(self, info, idLanguage, **kwargs):
        user = info.context.user  
        if user.is_anonymous:
            raise Exception('Not logged in!')
        print(user)

        filter = (
            Q(posted_by=user) & Q(id=idLanguage)
        )
        return Language.objects.filter(filter).first()
    
class CreateLanguage(graphene.Mutation):
    idLanguage = graphene.Int()
    language = graphene.String()
    posted_by = graphene.Field(UserType)

    class Arguments:
        idLanguage = graphene.Int()
        language = graphene.String()

    def mutate(self, info, idLanguage, language):
        user = info.context.user or None 
        print(user)

        currentLanguage = Language.objects.filter(id=idLanguage).first()
        print(currentLanguage)

        laguage = Language(
            language = language,
            posted_by = user
        )

        if currentLanguage:
            language.id = currentLanguage.id

        laguage.save()    

        return CreateLanguage(
            idLanguage = laguage.id,
            language = language.language,
            posted_by = language.posted_by
        )
    
class DeleteLanguage(graphene.Mutation):
    idLanguage = graphene.Int()

    class Arguments:
        idLanguage= graphene.Int()

    def mutate(self, info, idLanguage):
        user = info.context.user or None

        if user.is_anonymous:
            raise Exception('Not logged in!')
        print(user)

        currentLanguage = Language.objects.filter(id=idLanguage).first()
        print (currentLanguage)

        if not currentLanguage:
            raise Exception('Invalid Language id!')
        
        currentLanguage.delete()

        return CreateLanguage(
            idLanguage = idLanguage
        )
    
class Mutation(graphene.ObjectType):
    create_language = CreateLanguage.Field()
    delete_language = DeleteLanguage.Field()