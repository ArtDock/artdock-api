from neo4j import GraphDatabase
import pandas as pd
import os
from dotenv import load_dotenv
load_dotenv()

URI = os.environ.get("DATABASE_URI")
DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")
DATABASE_USER = os.environ.get("DATABASE_USER")
AUTH = (DATABASE_USER, DATABASE_PASSWORD)

print(URI)
driver = GraphDatabase.driver(URI, auth=AUTH)


def fetch_data(query, params={}):
    with driver.session() as session:
        print(query, params)
        result = session.run(query, params)
        return pd.DataFrame([r.values() for r in result], columns=result.keys())


class GraphFetcher:
    def load_artist_name():
        query = """MATCH (a:Artist) RETURN a.id AS id, a.nameJa AS nameJa, a.nameEn AS nameEn"""
        df_artist = fetch_data(query)
        return df_artist

    def load_artist_emb():
        query = """MATCH (a:Artist) RETURN a.id AS id, a.nameJa AS nameJa, a.nameEn AS nameEn, a.embedding AS artist_emb"""
        df_artist = fetch_data(query)
        return df_artist

    def load_artist_emb_by_id(ids):
        query = """MATCH (a:Artist) WHERE a.id in $data RETURN a.id AS id, a.nameJa AS nameJa, a.nameEn AS nameEn, a.embedding AS artist_emb"""
        df_artist = fetch_data(query, {'data': ids})
        return df_artist
