from src.util.dao import DAO

def test_connection():
    dao = DAO("task")   
    assert dao is not None