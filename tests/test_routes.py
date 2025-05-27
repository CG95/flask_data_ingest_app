import os
from pathlib import Path
import time
from flask import Flask
import pytest
from app import create_app, db, cache
from app.ingest import ingest_csv
from app.models import Sales


@pytest.fixture(scope='module')
def test_app():
    """Create a new Flask app instance for testing."""
    
    database_url = os.environ.get("TEST_POSTGRES_URL")
    if not database_url:
        raise RuntimeError("TEST_POSTGRES_URL environment variable not set")
    
    redis_host = os.environ.get("TEST_REDIS_URL")
    if not redis_host:
        raise RuntimeError("TEST_REDIS_URL environment variable not set")
    
    from app.config import Config
    # override the config for testing
    Config.SQLALCHEMY_DATABASE_URI = database_url
    Config.CACHE_REDIS_HOST = redis_host

    app=create_app()
    
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": database_url,
        "CACHE_REDIS_URL": redis_host,
    })
    
    with app.app_context():
        # ingest a modest sized CSV to allow measurable durations
        ingest_csv(os.path.join("data", "sales_data.csv"))
    yield app

    # drop all tables
    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(test_app):
    """Return a test client."""
    return test_app.test_client()

# -------------------------
# helper methods
#-------------------------

def parse_data(resp):
    assert resp.status_code == 200
    payload = resp.get_json()
    assert "data" in payload
    return payload["data"]


def measure(client, path):
    start = time.perf_counter()
    resp = client.get(path)
    elapsed = time.perf_counter() - start
    data = parse_data(resp)
    return data, elapsed



# -----------------------------------------------------------------------------
# Tests: monthly-summary
# -----------------------------------------------------------------------------

def test_monthly_summary_no_cache_missing_param(client):
    resp = client.get("/analytics/monthly-summary/no-cache")
    assert resp.status_code == 400



def test_monthly_summary_performance(client):
    uncached = "/analytics/monthly-summary/no-cache?year=2024"
    cached = "/analytics/monthly-summary?year=2024"

    data1, t1 = measure(client, uncached)
    client.get(cached)
    data2, t2 = measure(client, cached)

    assert data1 == data2
    assert t2 < t1


# -----------------------------------------------------------------------------
# Tests: top-products
# -----------------------------------------------------------------------------

def test_top_products_no_cache_missing_param(client):
    resp = client.get("/analytics/top-products/no-cache")
    assert resp.status_code == 400

def test_top_products_invalid_year(client):
    resp = client.get("/analytics/top-products/no-cache?start_date=20AA-01-01&end_date=20BB-12-31")
    assert resp.status_code == 400




def test_top_products_performance(client):
    uncached = "/analytics/top-products/no-cache?start_date=2024-01-01&end_date=2024-12-31"
    cached = "/analytics/top-products?start_date=2024-01-01&end_date=2024-12-31"

    data1, t1 = measure(client, uncached)
    
    client.get(cached)
    data2, t2 = measure(client, cached)

    assert data1 == data2
    assert t2 < t1



# -----------------------------------------------------------------------------
# Tests: sales-summary
# -----------------------------------------------------------------------------

def test_sales_summary_missing_dates(client):
    resp = client.get("/analytics/sales-summary")
    assert resp.status_code == 400

def test_sales_summary_invalid_date_format(client):
    resp = client.get("/analytics/sales-summary?start_date=2024-01-xx&end_date=2024-12-31")
    assert resp.status_code == 400

def test_sales_summary_no_filters(client):
    url = "/analytics/sales-summary?start_date=2024-01-01&end_date=2024-12-31"
    data = parse_data(client.get(url))
    assert isinstance(data, list)

def test_sales_summary_with_region_and_product(client):
    # pick a region and product_id known in sample_sales.csv
    url = "/analytics/sales-summary?start_date=2024-01-01&end_date=2024-12-31&region=North&product_id=1"
    data = parse_data(client.get(url))
    # all returned regions start with 'NORTH'
    assert all(item["region"].startswith("NORTH") for item in data)
    assert all(item["product_id"] == 1 for item in data)



def test_sales_summary_performance(client):
    uncached = "/analytics/sales-summary/no-cache?start_date=2024-01-01&end_date=2024-12-31"
    cached = "/analytics/sales-summary?start_date=2024-01-01&end_date=2024-12-31"

    data1, t1 = measure(client, uncached)
    client.get(cached)
    data2, t2 = measure(client, cached)

    assert data1 == data2
    assert t2 < t1
