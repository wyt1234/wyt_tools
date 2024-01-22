from typing import List

import hnswlib
import numpy as np
import pickle

from src.database import example_sentences
from src.dispatcher_service.gte_emb_interface import embed_sentences
from src.dispatcher_service.schemas import ExampleSentenceInDBBase, DialogueResp

MAX_DIST = 0.15  # 最大距离


def init_hnsw_index(data: List[ExampleSentenceInDBBase]):
    """
    初始化hnsw索引
    :return:
    """
    print('初始化hnsw索引')

    global p, example_sentences_list
    example_sentences_list = data

    dim = 1024
    data = [eval(x['vector_embedding']) for x in data]

    num_elements = len(data)
    ids = np.arange(num_elements)

    # Declaring index
    p = hnswlib.Index(space='l2', dim=dim)  # possible options are l2, cosine or ip

    # Initializing index - the maximum number of elements should be known beforehand
    p.init_index(max_elements=num_elements, ef_construction=200, M=16)

    # Element insertion (can be called several times):
    p.add_items(data, ids)

    print(f"Parameters passed to constructor:  space={p.space}, dim={p.dim}")
    print(f"Index construction: M={p.M}, ef_construction={p.ef_construction}")
    print(f"Index size is {p.element_count} and index capacity is {p.max_elements}")
    print(f"Search speed/quality trade-off parameter: ef={p.ef}")

    return


def search_hnsw(query):
    # 请求gte向量
    vector_embedding = embed_sentences([query]).get('text_embedding')
    vector_embedding = np.array(vector_embedding)

    # Query dataset, k - number of the closest elements (returns 2 numpy arrays)
    labels, distances = p.knn_query(vector_embedding, k=5)

    intention_result_list = []
    for i, num in enumerate(list(labels[0])):
        dist = distances[0][i]
        if dist < MAX_DIST:
            hit = dict(example_sentences_list[num])
            print(f"命中意图：{hit['sentence']} {dist}")
            intention_result_list.append(DialogueResp(intent=hit['intent'], weight=1 - dist, mode="sentence"))

    return intention_result_list
