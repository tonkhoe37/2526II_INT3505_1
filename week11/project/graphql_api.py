import graphene
from db import courses


class CourseType(graphene.ObjectType):
    id = graphene.Int()
    title = graphene.String()


class Query(graphene.ObjectType):
    courses = graphene.List(CourseType)

    def resolve_courses(self, info):
        return courses


schema = graphene.Schema(query=Query)
