import graphene
from riistvara.models import Author
from graphene_django.types import DjangoObjectType


class AuthorType(DjangoObjectType):
     class Meta:
          model = Author

class Query(graphene.AbstractType):
     all_authors = graphene.List(AuthorType)
     author = graphene.Field(AuthorType, id=graphene.Int())

     def resolve_all_authors(self, args, context, info):
          return Author.objects.all()

     def resolve_author(self, args, context, info):
          id = args.get('id')
          if id is not None:
               return Author.objects.get(pk=id)
          return None
