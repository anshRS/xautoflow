import pytest
from uuid import uuid4
from app.models.task import TaskType, TaskStatus

@pytest.mark.asyncio
async def test_create_task(client, api_key_headers):
    response = await client.post(
        "/api/v1/tasks/",
        headers=api_key_headers,
        json={
            "task_type": "RESEARCH",
            "input_data": {
                "ticker": "AAPL",
                "timeframe": "1d",
                "start_date": "2024-01-01",
                "end_date": "2024-04-01"
            }
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["task_type"] == "RESEARCH"
    assert data["status"] == "PLANNING"
    assert "id" in data

@pytest.mark.asyncio
async def test_get_task(client, api_key_headers):
    # First create a task
    create_response = await client.post(
        "/api/v1/tasks/",
        headers=api_key_headers,
        json={
            "task_type": "RESEARCH",
            "input_data": {"ticker": "AAPL"}
        }
    )
    task_id = create_response.json()["id"]

    # Then get it
    response = await client.get(
        f"/api/v1/tasks/{task_id}",
        headers=api_key_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["task_type"] == "RESEARCH"

@pytest.mark.asyncio
async def test_approve_task_plan(client, api_key_headers):
    # First create a task
    create_response = await client.post(
        "/api/v1/tasks/",
        headers=api_key_headers,
        json={
            "task_type": "RESEARCH",
            "input_data": {"ticker": "AAPL"}
        }
    )
    task_id = create_response.json()["id"]

    # Then approve its plan
    response = await client.put(
        f"/api/v1/tasks/{task_id}/approve",
        headers=api_key_headers,
        json={
            "approved": True,
            "feedback": "Looks good"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "RUNNING"

@pytest.mark.asyncio
async def test_list_tasks(client, api_key_headers):
    response = await client.get(
        "/api/v1/tasks/",
        headers=api_key_headers,
        params={
            "task_types": ["RESEARCH"],
            "statuses": ["PLANNING", "RUNNING"],
            "limit": 10
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list) 