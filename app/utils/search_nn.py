from annoy import AnnoyIndex
import pandas as pd
from graph_db.fetcher import GraphFetcher


class Search:
    def emb_average(df, emb_col):
        average_emb = []
        for col_index, col in enumerate(df[emb_col][0]):
            sum = 0
            for row_index in df[emb_col].index:
                sum += df[emb_col][row_index][col_index]
            average = sum/len(df[emb_col])
            average_emb.append(average)
        return average_emb

    def annoy(query_emb):

        df_all = GraphFetcher.load_artist_emb()

        t = AnnoyIndex(50, 'angular')
        t.add_item(0, query_emb)
        for i in range(len(df_all['artist_emb'])):
            t.add_item(i+1, df_all['artist_emb'][i])
        t.build(10)

        nns = t.get_nns_by_item(0, 11, search_k=-1, include_distances=False)
        nns = [x - 1 for x in nns]
        nns.pop(0)

        return df_all[["id", "nameJa", "nameEn"]].iloc[nns, :]
