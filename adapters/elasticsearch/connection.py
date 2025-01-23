from elasticsearch import Elasticsearch
from adapters.database.models import GameModel
from adapters.database.database import SessionLocal

"""
Establishes and returns a connection to the Elasticsearch server.
"""
try:
    es = Elasticsearch(
        hosts=["http://localhost:9200"],
        timeout=30,
        max_retries=10,
        retry_on_timeout=True
    )
except Exception as e:
    print(f"Error initializing Elasticsearch: {e}")


def sync_data_to_elasticsearch():

    index_name = "games"

    if not es.indices.exists(index=index_name):
        es.indices.create(
            index=index_name,
            body={
                "mappings": {
                    "properties": {
                        "id": {"type": "integer"},
                        "name": {"type": "text"},
                        "price": {"type": "integer"},
                        "is_in_stock": {"type": "boolean"}
                    }
                }
            }
        )
        print(f"Index '{index_name}' created.")

    print("Synchronizing data to Elasticsearch...")
    # Получаем данные из PostgreSQL
    session = SessionLocal()
    games = session.query(GameModel).all()

    # Записываем данные в Elasticsearch
    for game in games:
        es.index(
            index="games",
            id=game.id,
            body={
                "name": game.name,
                "price": game.price,
                "is_in_stock": game.is_in_stock
            }
        )

    session.close()
    print("Data synchronized.")


def get_es():
    yield es