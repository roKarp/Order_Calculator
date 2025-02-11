import pytest
import requests

url = "http://localhost:8000/api/v1/delivery-order-price"

tests = [
    ("?venue_slug=home-assignment-venue-helsinki&cart_value=700&user_lat=60.17094&user_lon=24.93087", 
    {"cart_value":700,"delivery":{"distance":176.5,"fee":190.0},"small_order_surcharge":300,"total_price":1190.0})
    ]

tests_err = ["?venue_slug=home-assignment-venue-helsinki&cart_value=700&user_lat=60.17094",
            "?venue_slug=home-assignment-venue-helsinki&cart_value=700&user_lat=hi&user_lon=24.93087"]

def test_endpoint():
    for test, output in tests:
        response = requests.get(url + test)
        assert response.status_code == 200


def test_output():
    for test, output in tests:
        response = requests.get(url + test)
        assert response.json() == output


def test_invalid_query():
    for test in tests_err:
        response = requests.get(url + test)
        assert response.status_code == 400