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
    print(f"Error initializing database: {e}")


#index_name = "games"

#if not es.indices.exists(index=index_name):
#    es.indices.create(
#        index=index_name,
#        body={
#            "mappings": {
#                "properties": {
#                    "id": {"type": "integer"},
#                    "name": {"type": "text"},
#                    "price": {"type": "integer"},
#                    "is_in_stock": {"type": "boolean"}
#                }
#            }
#        }
#    )
#    print(f"Index '{index_name}' created.")

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

    # Get data from PostgreSQL
    session = SessionLocal()
    games = session.query(GameModel).all()

    # Index data into Elasticsearch
    for game in games:
        es.index(
            index="games",  # Elasticsearch index name
            id=game.id,      # The ID of the document in Elasticsearch
            body={
                "name": game.name,
                "price": game.price,
                "is_in_stock": game.is_in_stock
            }
        )

    session.close()
    print("Data synchronized to Elasticsearch.")


def get_es():
    yield es