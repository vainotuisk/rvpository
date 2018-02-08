import graphene
import riistvara.schema

class Query(riistvara.schema.Query, graphene.ObjectType):
     pass
schema = graphene.Schema(query=Query)
