import pytest

from ql_library.users.tests.factories import UserFactory


@pytest.mark.django_db
class TestUserQuery:
    query = """
    { 
        users {
            id
            username
        }
    }
    """

    def test_get_users_query(self, gql_client):
        users = UserFactory.create_batch(5)
        result = gql_client().query(self.query)
        assert len(result.data["users"]) == len(users)

    def test_get_user_query(self, gql_client):
        users = UserFactory.create_batch(5)
        query = f"""
        {{
            user(pk: {users[0].id}) {{
                id
                email
            }}
        }}
        """

        result = gql_client().query(query)
        assert result.data["user"]["email"] == users[0].email
