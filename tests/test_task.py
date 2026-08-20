from httpx import AsyncClient


async def test_create_task(client: AsyncClient):
    response = await client.post("/tasks/", json={"description": "test task"})

    assert response.status_code == 201
    data = response.json()
    assert data["description"] == "test task"
    assert not data["done"]
    assert "id" in data


async def test_update_task(client: AsyncClient):
    task = await client.post("/tasks/", json={"description": "test task"})

    assert task.status_code == 201
    task_id = task.json()["id"]
    response = await client.patch(
        f"/tasks/{task_id}", json={"description": "test update task", "done": True}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["description"] == "test update task"
    assert data["done"]


async def test_load_tasks(client: AsyncClient):
    task = await client.post("/tasks/", json={"description": "test task"})

    assert task.status_code == 201
    task_json = task.json()
    response = await client.get("/tasks/")
    data = response.json()

    assert response.status_code == 200
    assert task_json in data


async def test_delete_task(client: AsyncClient):
    task = await client.post("/tasks/", json={"description": "test task"})

    assert task.status_code == 201
    task_id = task.json()["id"]
    response = await client.delete(f"/tasks/{task_id}")
    deleted_task = response.json()

    assert response.status_code == 200
    assert task_id == deleted_task["id"]

    tasks_response = await client.get("/tasks/")
    assert deleted_task not in tasks_response.json()


async def test_update_nonexistent_task_404(client: AsyncClient):
    response = await client.patch("/tasks/888", json={"description": "I don't exist."})

    assert response.status_code == 404


async def test_delete_nonexistent_task_404(client: AsyncClient):
    response = await client.delete("/tasks/888")

    assert response.status_code == 404


async def test_update_task_without_description(client: AsyncClient):
    task = await client.post("/tasks/", json={"description": "test task"})

    assert task.status_code == 201
    task_id = task.json()["id"]
    response = await client.patch(f"/tasks/{task_id}", json={"done": True})

    assert response.status_code == 200
    assert response.json()["description"] == "test task"


async def test_task_create_large_description_422(client: AsyncClient):
    response = await client.post(
        "/tasks/",
        json={
            "description": "This is a test to ensure that it is impossible to a create a task with a description that exceeds the set limit of two hundred and fifty five characters. Attempting to create a task with a description with more than two hundred and fifty five characters should return a 422."
        },
    )

    assert response.status_code == 422


async def test_task_update_large_description_422(client: AsyncClient):
    task = await client.post("/tasks/", json={"description": "test task"})

    assert task.status_code == 201
    task_id = task.json()["id"]
    response = await client.patch(
        f"/tasks/{task_id}",
        json={
            "description": "This is a test to ensure that it is impossible to a update a task with a description that exceeds the set limit of two hundred and fifty five characters. Attempting to update a task with a description with more than two hundred and fifty five characters should return a 422."
        },
    )

    assert response.status_code == 422
