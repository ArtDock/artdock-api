from typing import List
from fastapi import FastAPI, status
from graph_db.fetcher import GraphFetcher
import numpy as np
from utils.search_nn import Search
import json

app = FastAPI()

# start development server via this command
# source .venv/bin/activate
# cd app
# uvicorn main:app --reload


@app.get("/health",
         tags=["health_check"],
         summary="Perform a Health Check",
         response_description="Return HTTP Status Code 200 (OK)",
         status_code=status.HTTP_200_OK,)
def get_health():
    return {"message": "OK"}


@app.get("/artists",
         tags=["artist_list"],
         summary="Get Artist List",)
def get_artists():
    df_artist = GraphFetcher.load_artist_name()
    res = json.loads(df_artist.to_json(orient="records"))
    return {"artists": res}


@app.get("/artists/emb",
         tags=["search_nn"],
         summary="Search Nearest Neighbor Artists from Embedding",)
def search_nn(artist_id1: str = None, artist_id2: str = None, artist_id3: str = None, artist_id4: str = None, start_index: int = 0, num_neighbor: int = 11):
    artist_ids = [artist_id1, artist_id2, artist_id3, artist_id4]
    if artist_ids == [None, None, None, None]:
        return {"message": "None Parameter"}

    artist_ids = [id for id in artist_ids if id is not None]
    df_artist = GraphFetcher.load_artist_emb_by_id(artist_ids)

    average_emb = Search.emb_average(df=df_artist, emb_col="artist_emb")

    df_nn = Search.annoy(query_emb=average_emb,
                         num_neighbor=start_index+num_neighbor)
    df_nn = df_nn.reset_index(drop=True).reset_index()
    df_nn = df_nn.iloc[start_index:]
    print(df_nn)
    res = json.loads(df_nn.to_json(orient="records"))

    return {"artists": res}
