import pytest

from tests.helpers.API import API, ENDPOINTS
from tests.helpers.models import PostSchema
from tests.helpers.validators import validate_json
from tests.test_data.PostTestResponse import PostTestResponse

WITH_ID_AND_ALL_OTHER_FIELDS_XFAIL_MESSAGE = """API returned 201 for payload, that contains 'id' field, which already exists.
Should it even accept 'id' field?
For POST request, by doing which we generate new entries, it is logical, that system generates unique ID by itself.
And we should modify existing entries through PUT request.
In the guide on https://jsonplaceholder.typicode.com/guide/ 'id' field is omitted."""


class Test_API():

    def test_get_withhout_params(self, api: API):
        """All possible elements for GET request without parameters should equal 100"""

        response = api.get(ENDPOINTS.posts.value)

        assert len(response.json()) == 100
        assert response.status_code == 200

    def test_get_with_path_variable(self, api: API):
        """GET request to posts/{} should work just as well, as a request through query string."""

        endpoint_with_path_variable = ENDPOINTS.posts.value + "/1"
        response = api.get(endpoint_with_path_variable)

        assert response.status_code == 200

    # Pairwise testing of parameters
    @pytest.mark.parametrize("params", [
        pytest.param({"id": PostTestResponse.id.value}, id="Only id"),
        pytest.param(
            {"title": PostTestResponse.title.value, "body": PostTestResponse.body.value}, id="title and body"),
        pytest.param(
            {"userId": PostTestResponse.userId.value, "title": PostTestResponse.title.value}, id="userId and title"),
        pytest.param({"userid": PostTestResponse.userId.value,
                     "body": PostTestResponse.body.value}, id="userId and body"),
        pytest.param({"id": PostTestResponse.id.value, "userid": PostTestResponse.userId.value,
                     "body": PostTestResponse.body.value}, id="id, userId and body"),
        pytest.param({"id": PostTestResponse.id.value, "userid": PostTestResponse.userId.value,
                     "title": PostTestResponse.title.value}, id="id, userId and title"),
        pytest.param({"id": PostTestResponse.id.value, "body": PostTestResponse.body.value,
                     "title": PostTestResponse.title.value}, id="id, body and title")
    ])
    def test_get_posts(self, api: API, params: dict):
        """GET request on posts/ endpoint should return json with list of objects,
        which conform to 'post' schema. """

        response = api.get(ENDPOINTS.posts.value, params)
        errors = validate_json(response.json(), PostSchema)

        assert errors == None
        assert response.status_code == 200

    def test_get_post_that_does_not_exist(self, api: API):
        """POST request to entry, that does not exist should return empty array."""

        payload = {"id": 200}
        response = api.get(ENDPOINTS.posts.value, params=payload)

        assert response.json() == []
        assert response.status_code == 200

    def test_post_valid_entry(self, api: API):
        """POST request  on posts/ endpoint with valid payload should return 201 status code. As stated in jsonplaceholder.typicode.com/ guide,
        POST request does not actually create new entries, so we can't assert it's success by doing GET request afterwards."""

        payload = {"userId": PostTestResponse.userId.value,
                   "title": PostTestResponse.title.value,
                   "body": PostTestResponse.body.value}
        response = api.post(ENDPOINTS.posts.value, json=payload)
        payload.update({'id': 101})

        assert response.json() == payload
        assert response.status_code == 201

    @pytest.mark.parametrize("payload", [
        pytest.param({i.name: i.value for i in PostTestResponse},
                     id="With id and all other fields",
                     marks=pytest.mark.xfail(reason=WITH_ID_AND_ALL_OTHER_FIELDS_XFAIL_MESSAGE)),
        pytest.param({}, id="With empty payload",
                     marks=pytest.mark.xfail(reason="Should we be able to create totally empty entry?"))

    ])
    def test_post_invalid_entry(self, api: API, payload: dict):
        """POST request on posts/ endpoint with invalid payload should return 400 status code."""

        payload = {elem.name: elem.value for elem in PostTestResponse}
        response = api.post(ENDPOINTS.posts.value, json=payload)

        assert response.status_code == 201

    @pytest.mark.parametrize("id", [
        pytest.param("1", id="Existing id"),
        pytest.param("200", id="Nonexistent id")
    ])
    def test_delete_resource(self, api: API, id: str):
        """DELETE request should return status code 200"""

        response = api.delete(ENDPOINTS.posts.value, id)

        assert response.status_code == 200
