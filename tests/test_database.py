import pytest
from unittest import mock
from app.config.db import get_db
from app.database.queries import DatabaseQueries

# Mock the get_db function
def mock_get_db():
    return mock.MagicMock()

@pytest.fixture
def database_queries():
    return DatabaseQueries()

# Test the _get_db_collection_manager method
def test_get_db_collection_manager(database_queries):
    db_name = "test_db"
    collection_name = "test_collection"

    with mock.patch('app.database.queries.get_db', side_effect=mock_get_db):
        collection = database_queries._get_db_collection_manager(db_name=db_name, collection_name=collection_name)

    assert collection is not None
    assert isinstance(collection, mock.MagicMock)

# Test the insert_one method
def test_insert_one(database_queries):
    db_name = "test_db"
    collection_name = "test_collection"
    data = {"key": "value"}

    with mock.patch('app.database.queries.get_db', side_effect=mock_get_db):
        collection = database_queries._get_db_collection_manager(db_name=db_name, collection_name=collection_name)

    with mock.patch('app.database.queries.get_db', side_effect=mock_get_db):
        database_queries.insert_one(db_name=db_name, collection_name=collection_name, data=data)
    
    assert collection.find_one(data) is not None

# Test the get_paginated_data method
def test_get_paginated_data(database_queries):
    db_name = "test_db"
    collection_name = "test_collection"
    page_no = 0
    data = {"key": "value"}

    with mock.patch('app.database.queries.get_db', side_effect=mock_get_db):
        collection = database_queries._get_db_collection_manager(db_name=db_name, collection_name=collection_name)

    with mock.patch('app.database.queries.get_db', side_effect=mock_get_db):
        database_queries.insert_one(db_name=db_name, collection_name=collection_name, data=data)

    with mock.patch('app.database.queries.get_db', side_effect=mock_get_db):
        data = database_queries.get_paginated_data(db_name=db_name, collection_name=collection_name, page_no=page_no)

    assert isinstance(data, list)
   

# Test the get_page_data method
def test_get_page_data(database_queries):
    db_name = "test_db"
    collection_name = "test_collection"
    filter_object = {"status": True}

    with mock.patch('app.database.queries.get_db', side_effect=mock_get_db):
        result = database_queries.get_page_data(db_name=db_name, collection_name=collection_name, filter_object=filter_object)

    assert isinstance(result, dict)