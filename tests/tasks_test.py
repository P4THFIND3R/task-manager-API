from httpx import AsyncClient


async def get_headers(ac: AsyncClient) -> dict:
    response = await ac.post("/auth/login", data={
        "username": "user_test",
        "password": "password_test"
    })
    my_headers = {'access_token': response.cookies.get('access_token'),
                  'refresh_token': response.cookies.get('refresh_token')}
    return my_headers


async def test_add_task(ac: AsyncClient):
    my_headers = await get_headers(ac)

    json = {
        "title": "test",
        "description": "test",
        "username": "user_test",
        "status": "planned",
    }
    response = await ac.post(
        "/tasks/",
        json=json, headers=my_headers
    )
    assert response.status_code == 201
    for k, v in json.items():
        assert response.json()[k] == v


async def test_get_task(ac: AsyncClient):
    my_headers = await get_headers(ac)

    task_id = 1
    response = await ac.get(
        "/tasks/?task_id={}".format(task_id), headers=my_headers
    )
    assert response.status_code == 200
    assert response.json()


async def test_update_task(ac: AsyncClient):
    my_headers = await get_headers(ac)

    task_id = 1
    response = await ac.patch(
        "/tasks/?task_id={}".format(task_id), json={'status': 'pending'}, headers=my_headers
    )
    assert response.status_code == 200
    assert response.json()['status'] == 'pending'


async def test_delete_task(ac: AsyncClient):
    my_headers = await get_headers(ac)

    task_id = 1
    response = await ac.delete(
        "/tasks/?task_id={}".format(task_id), headers=my_headers
    )
    assert response.json()['status'] == 'deleted'
