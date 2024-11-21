from django.test import TestCase
from graphene_django.utils.testing import GraphQLTestCase
from mixer.backend.django import mixer
import graphene
import json
from django.contrib.auth import get_user_model

from hacker_news.schema import schema
from language.models import Language

# Create your tests here.
GET_ALL_LANGUAGES = '''
query {
  languages {
    id
    language
  }
}
'''

GET_LANGUAGES_WITH_WILDCARD = '''
query {
  languages(search: "*") {
    id
    language
  }
}
'''

GET_FILTERED_LANGUAGES = '''
query GetFilteredLanguages($search: String!) {
  languages(search: $search) {
    id
    language
  }
}
'''

CREATE_USER_MUTATION = '''
 mutation createUserMutation($email: String!, $password: String!, $username: String!) {
     createUser(email: $email, password: $password, username: $username) {
         user {
            username
            password
         }
     }
 }
'''

LOGIN_USER_MUTATION = '''
 mutation TokenAuthMutation($username: String!, $password: String!) {
     tokenAuth(username: $username, password: $password) {
        token
     }
 }
'''

class LanguageTestCase(GraphQLTestCase):
    GRAPHQL_URL = "http://localhost:8000/graphql/"
    GRAPHQL_SCHEMA = schema

    def setUp(self):
        response_user = self.query(
            CREATE_USER_MUTATION,
            variables={'email': 'adsoft@live.com.mx', 'username': 'adsoft', 'password': 'adsoft'}
        )
        print('user mutation ')
        content_user = json.loads(response_user.content)
        print(content_user['data'])

        response_token = self.query(
            LOGIN_USER_MUTATION,
            variables={'username': 'adsoft', 'password': 'adsoft'}
        )

        content_token = json.loads(response_token.content)
        token = content_token['data']['tokenAuth']['token']
        print(token)
        self.headers = {"AUTHORIZATION": f"JWT {token}"}

        # Crear usuario y asociar registros
        self.user = get_user_model().objects.get(username="adsoft")
        self.language1 = mixer.blend(Language, posted_by=self.user)
        self.language2 = mixer.blend(Language, posted_by=self.user)
