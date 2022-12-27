from fastapi.testclient import TestClient
from schemas.foo import FooItem, FooItemCreate
from main import app

client = TestClient(app)

def test_create_item():
    # Setup the test data
    test_item = FooItemCreate(description="Test", public=True)

    # Send the request
    response = client.post("/foos/", json={"description": test_item.description, "public": test_item.public})

    # Get response data
    item_response = FooItem.parse_obj(response.json())

    # Assert response data
    assert response.status_code == 201
    assert item_response.description == test_item.description
    assert isinstance(item_response.description, str)
    assert isinstance(item_response.id, int)
    assert isinstance(item_response, FooItem)

def test_create_item_bad():
    # Setup the test data
    description = 1
    public = 2

    # Send the request
    response = client.post("/foos/", json={"description": description, "public": public})
    print(response.json())
    
    # Assert response data
    assert response.status_code == 422

def test_read_item():
    # Setup the test data
    id = 5
    auth_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJwcnVlYmEiLCJleHAiOjE2NjE1NjQ4NjB9.PYdBuqVenOQJ42Xb836q5NrG0sP11Muehe6knwjbSyU"

    # Send the request
    response = client.get(f"/foos/{id}", headers={"Authorization": f"Bearer {auth_token}"})

    # Get response data
    item_response = FooItem.parse_obj(response.json())

    # Assert response data
    assert response.status_code == 200
    assert isinstance(item_response.description, str)
    assert isinstance(item_response.id, int)
    assert isinstance(item_response, FooItem)

def test_read_inexistent_item():
    # Setup the test data
    id = 0
    auth_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJwcnVlYmEiLCJleHAiOjE2NjE1NjQ4NjB9.PYdBuqVenOQJ42Xb836q5NrG0sP11Muehe6knwjbSyU"

    # Send the request
    response = client.get(f"/foos/{id}", headers={"Authorization": f"Bearer {auth_token}"})

    # Get response data
    item_response = response.json()

    # Assert response data
    assert response.status_code == 404
    assert item_response["context"]["Message"] == f"No se ha encontrado ningun objeto con el id: {id}"

def test_read_all_items():
    # Setup the test data
    auth_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJwcnVlYmEiLCJleHAiOjE2NjE1NjQ4NjB9.PYdBuqVenOQJ42Xb836q5NrG0sP11Muehe6knwjbSyU"

    # Send the request
    response = client.get("/foos/", headers={"Authorization": f"Bearer {auth_token}"})

    # Get response data
    item_response = []
    for item in response.json():
        item_response.append(FooItem.parse_obj(item))

    # Assert response data
    assert response.status_code == 200
    assert isinstance(item_response, list)
    assert isinstance(item_response[0].description, str)
    assert isinstance(item_response[0].id, int)
    assert isinstance(item_response[0],FooItem)