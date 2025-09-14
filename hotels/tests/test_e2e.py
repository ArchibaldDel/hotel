import pytest
import requests
import time

BASE_URL = "http://web:9000"  # имя сервиса из docker-compose

@pytest.fixture(scope="session", autouse=True)
def wait_for_service():
    # ждём пока сервер поднимется
    for _ in range(10):
        try:
            r = requests.get(f"{BASE_URL}/health")
            if r.status_code == 200:
                return
        except Exception:
            pass
        time.sleep(2)
    pytest.fail("Service did not start in time")

def test_healthcheck():
    r = requests.get(f"{BASE_URL}/health")
    assert r.status_code == 200
    assert r.json()["status"] == "healthy"

def test_full_flow():
    # 1. Создаём комнату
    r = requests.post(f"{BASE_URL}/rooms/", json={"description": "E2E room", "price_per_night": "1234.00"})
    assert r.status_code == 201
    room_id = r.json()["id"]

    # 2. Создаём бронь
    booking_data = {"room": room_id, "date_start": "2025-09-15", "date_end": "2025-09-20"}
    r = requests.post(f"{BASE_URL}/bookings/", json=booking_data)
    assert r.status_code == 201
    booking_id = r.json()["id"]

    # 3. Проверяем список броней
    r = requests.get(f"{BASE_URL}/bookings/list/?room_id={room_id}")
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 1
    assert data[0]["id"] == booking_id

    # 4. Удаляем бронь
    r = requests.delete(f"{BASE_URL}/bookings/{booking_id}/")
    assert r.status_code == 204
