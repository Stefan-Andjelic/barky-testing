# how would I test Barky?
# First, I wouldn't test barky, I would test the reusable modules barky relies on:
# commands.py and database.py

# we will use pytest: https://docs.pytest.org/en/stable/index.html

# should we test quit? No, its behavior is self-evident and not logic dependent
def test_quit_command():
    pass

# okay, should I test the other commands?
# not really, they are tighly coupled with sqlite3 and its use in the database.py module

from database import DatabaseManager
import os
from datetime import datetime
import sqlite3
import pytest


@pytest.fixture
def database_manager() -> DatabaseManager:
    """
    What is a fixture? https://docs.pytest.org/en/stable/fixture.html#what-fixtures-are
    """
    filename = "test_bookmarks.db"
    dbm = DatabaseManager(filename)
    yield dbm
    dbm.__del__()           # explicitly release the database manager
    os.remove(filename)


def test_add_bookmark_command(database_manager):
    # arrange
    database_manager.create_table(
        "bookmarks",
        {
            "id": "integer primary key autoincrement",
            "title": "text not null",
            "url": "text not null",
            "notes": "text",
            "date_added": "text not null",
        },
    )

    data = {
        "title": "test_title",
        "url": "http://example.com",
        "notes": "test notes",
        "date_added": datetime.utcnow().isoformat()        
    }

    # act
    database_manager.add("bookmarks", data)

    # assert
    conn = database_manager.connection
    cursor = conn.cursor()
    cursor.execute(''' SELECT * FROM bookmarks WHERE title='test_title' ''')    
    # print(cursor.fetchone())
    assert cursor.fetchone()[0] == 1 


def test_list_bookmark_command(database_manager):
    # arrange
    database_manager.create_table(
        "bookmarks",
        {
            "id": "integer primary key autoincrement",
            "title": "text not null",
            "url": "text not null",
            "notes": "text",
            "date_added": "text not null",
        },
    )

    data = {
        "title": "test_title",
        "url": "http://example.com",
        "notes": "test notes",
        "date_added": datetime.utcnow().isoformat()        
    }

    data2 = {
        "title": "test_title",
        "url": "http://example.com",
        "notes": "test notes",
        "date_added": datetime.utcnow().isoformat()        
    }

    # act
    database_manager.add("bookmarks", data)
    database_manager.add("bookmarks", data2)

    # assert
    conn = database_manager.connection
    cursor = conn.cursor()
    cursor.execute(''' SELECT * FROM bookmarks WHERE title='test_title' ''')    
    # print(len(list(cursor)))
    # assert cursor.fetchall() == 2
    assert len(list(cursor)) == 2


# def test_edit_bookmark_command(database_manager):
#     # arrange
#     database_manager.create_table(
#         "bookmarks",
#         {
#             "id": "integer primary key autoincrement",
#             "title": "text not null",
#             "url": "text not null",
#             "notes": "text",
#             "date_added": "text not null",
#         },
#     )

#     data = {
#         "title": "test_title",
#         "url": "http://example.com",
#         "notes": "test notes",
#         "date_added": datetime.utcnow().isoformat()        
#     }

#     # act
#     database_manager.add("bookmarks", data)

#     # assert
#     conn = database_manager.connection
#     cursor = conn.cursor()
#     cursor.execute(''' SELECT * FROM bookmarks WHERE title='test_title' ''')    
#     # print(len(list(cursor)))
#     # assert cursor.fetchall() == 2
#     assert len(list(cursor)) == 2