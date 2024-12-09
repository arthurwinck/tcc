import pytest, asyncio
from tcc.api.dynamic_function_creator import DynamicFunctionCreator

# @pytest.mark.asyncio
# async def test_create_dynamic_function_real_request():
#     # Instance of the creator
#     creator = DynamicFunctionCreator

#     # Inputs for real request
#     url_path = "https://jsonplaceholder.typicode.com/posts"
#     method = "GET"
#     params = {}
#     responses = {200: {"description": "Request successful"}}

#     # Create the dynamic function
#     endpoint = creator._create_dynamic_function(url_path, method, params, responses)

#     # Call the dynamic function
#     response = await endpoint.func()

#     # Assertions for the real response
#     assert response["status_code"] == 200
#     assert isinstance(response["data"], list)  # Expecting a list of posts

#     print(response)


@pytest.mark.asyncio
async def test_create_dynamic_function_with_param():
    # Instance of the creator
    creator = DynamicFunctionCreator

    # Inputs for the request
    url_path = "https://jsonplaceholder.typicode.com/posts/{id}"
    method = "GET"
    params = {"id": {"type": "int"}}
    responses = {200: {"description": "Request successful"}}

    # Create the dynamic function
    endpoint_function = creator._create_dynamic_function(
        url_path, method, params, responses, "json_placeholder", "/posts/{id}"
    )

    # Call the dynamic function, passing a dynamic parameter
    response = await endpoint_function(
        params={"id": 1}
    )  # Pass `id` as a dynamic parameter

    # Assertions for the real response
    # assert response["status_code"] == 200
    # assert response["message"] == "Request successful"
    # assert isinstance(response["data"], dict)  # Expecting a single post
    # assert response["data"]["id"] == 1  # Validate the post ID

    print(response)


if __name__ == "__main__":
    # asyncio.run(test_create_dynamic_function_real_request())
    asyncio.run(test_create_dynamic_function_with_param())
