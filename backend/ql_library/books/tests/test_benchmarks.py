from django.urls import reverse

import pytest


@pytest.fixture(autouse=True)
def authors(author_factory):
    return author_factory.create_batch(with_books=True, size=100)


author_simple_fragment = """fragment authorFields on AuthorType {
    id
    name
}"""

author_full_fragment = """fragment authorFields on AuthorType {
    id
    name
    birthday
    country {
        name
    }
    books(pagination: {limit: 10}) {
        id
        title
        pages
        category
        language
    }
}"""

authors_simple_query = f"""query {{
    authors {{
        ...authorFields
    }}
}}
{author_simple_fragment}"""

authors_simple_query_pagination = f"""query {{
    authors(pagination: {{limit: 10}}) {{
        ...authorFields
    }}
}}
{author_simple_fragment}"""

authors_query = f"""query {{
    authors {{
        ...authorFields
    }}
}}
{author_full_fragment}"""

authors_query_pagination = f"""query {{
    authors(pagination: {{limit: 10}}) {{
        ...authorFields
    }}
}}
{author_full_fragment}"""

books_simple_query = """query {
    books {
        id
        title
        category
    }
}"""

books_simple_query_pagination = """query {
    books(pagination: {limit: 10}) {
        id
        title
        category
    }
}"""

books_query = """query {
    books {
        id
        author {
            id
            name
            country {
                name
            }
        }
        title
        pages
        category
        language
    }
}"""

books_query_pagination = """query {
    books(pagination: {limit: 10}) {
        id
        author {
            id
            name
            country {
                name
            }
        }
        title
        pages
        category
        language
    }
}"""


def gql_request(client, query):
    url = reverse("graphql")
    body = {"query": query}
    response = client.post(url, data=body, content_type="application/json")
    return response.json()


@pytest.mark.django_db
@pytest.mark.parametrize(
    "query",
    [
        pytest.param(books_simple_query, id="simple"),
        pytest.param(books_simple_query_pagination, id="simple-pagination"),
        pytest.param(books_query, id="full"),
        pytest.param(books_query_pagination, id="full-pagination"),
    ],
)
def test_books(query, client, benchmark):
    result = benchmark(gql_request, client=client, query=query)
    assert "errors" not in result
    assert result["data"] is not None


@pytest.mark.django_db
@pytest.mark.parametrize(
    "query",
    [
        pytest.param(authors_simple_query, id="simple"),
        pytest.param(authors_simple_query_pagination, id="simple-pagination"),
        pytest.param(authors_query, id="full"),
        pytest.param(authors_query_pagination, id="full-pagination"),
    ],
)
def test_authors(query, client, benchmark):
    result = benchmark(gql_request, client=client, query=query)
    assert "errors" not in result
    assert result["data"] is not None
