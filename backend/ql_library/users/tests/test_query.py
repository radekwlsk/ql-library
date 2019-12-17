import pytest

from ql_library.users.tests.factories import UserFactory


@pytest.mark.django_db
class TestUserQuery:
    query = """
    { 
        getUsers {
            id
            username
        }
    }
    """

    def test_get_users_query(self, gql_client):
        users = UserFactory.create_batch(5)
        result = gql_client().execute(self.query)
        assert 'errors' not in result
        assert len(result['data']['getUsers']) == len(users)

    def test_get_user_query(self, gql_client):
        users = UserFactory.create_batch(5)
        query = f"""
        {{
            getUser(username: \"{users[0].username}\") {{
                id
                email
            }}
        }}
        """

        result = gql_client().execute(query)
        assert 'errors' not in result
        assert result['data']['getUser']['email'] == users[0].email
