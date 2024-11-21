import graphene
from graphene_django import DjangoObjectType
from .models import WorkExperience, Archivement
from users.schema import UserType
from django.db.models import Q

class ArchivementType(DjangoObjectType):
    class Meta:
        model = Archivement

class WorkExperienceType(DjangoObjectType):
    archivements = graphene.List(ArchivementType)

    class Meta:
        model = WorkExperience

class Query(graphene.ObjectType):
    work_experiences = graphene.List(WorkExperienceType, search=graphene.String())
    work_experienceById = graphene.Field(WorkExperienceType, idWork=graphene.Int())

    def resolve_work_experiences(self,info, search=None, **kwargs):
        user = info.context.user  
        if user.is_anonymous:
            raise Exception('Not logged in!')
        print(user)

        if search == "*":
            ilter = Q(posted_by=user)
            return WorkExperienceType.objects.filter(filter)[:10]
        else:
            filter = Q(posted_by=user) & (Q(position__icontains=search) | Q(company__icontains=search))
            return WorkExperience.objects.filter(filter)
 
    def resolve_work_experienceById(self, info, idWork, **kwargs):
        user = info.context.user  
        if user.is_anonymous:
            raise Exception('NOt looged in!')
        print(user)

        filter = Q(posted_by=user) & Q(id=idWork)
        return WorkExperience.objects.filter(filter).first()
    
class CreateWorkExperience(graphene.Mutation):
    idWork = graphene.Int()
    position = graphene.String()
    company = graphene.String()
    start_date = graphene.Date()
    end_date = graphene.Date()
    location = graphene.String()
    archivements = graphene.List(graphene.String)
    posted_by = graphene.Field(UserType)

    class Arguments:
        idWork = graphene.Int()
        position = graphene.String()
        company = graphene.String()
        start_date = graphene.Date()
        end_date = graphene.Date()
        location = graphene.String()
        archivements = graphene.List(graphene.String)

    def mutate(self, info, idWork, position, company, start_date, end_date, location, archivements=None):
        user = info.context.user or None
        print(user)

        currentWork = WorkExperience.objects.filter(id=idWork).first()
        print(currentWork)

        work_experience = WorkExperience(
            position=position,
            company=company,
            start_date=start_date,
            end_date=end_date,
            location=location,
            posted_by=user
        )  

        if currentWork:
            work_experience.id = currentWork.id
        
        work_experience.save()

        archivements_objects = []
        if archivements:
            for description in archivements:
                archivement = Archivement(
                    description=description,
                    work_experience=work_experience,
                )
                archivement.save()
                archivements_objects.append(archivement)

        return CreateWorkExperience(
            idWork=work_experience.id,
            position=work_experience.position,
            company=work_experience.company,
            start_date=work_experience.start_date,
            end_date=work_experience.end_date,
            location=work_experience.location,
            archivements=archivements_objects,
            posted_by=work_experience.posted_by
        )
    
class DeleteWorkExperience(graphene.Mutation):
    idWork = graphene.Int()

    class Argument:
        idWork = graphene.Int()

    def mutate(self, info, idWork):
        user = info.context.user or None

        if user.is_anonymous:
            raise Exception('Not logged in!')
        print(user)

        currentWork = WorkExperience.objects.filter(idWork=idWork).first()
        print(currentWork)

        if not currentWork:
            raise Exception('INvalid WorkExperience id!')
        
        currentWork.delete()

        return DeleteWorkExperience(
            idWork=idWork,
        )
    
class Mutation(graphene.ObjectType):
    create_work_experience = CreateWorkExperience.Field()
    delete_work_experience = DeleteWorkExperience.Field()
