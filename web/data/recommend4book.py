import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# 추천 함수
def getRecommend(df, tfidf_matrix, isbn_list):
    isbn_list = isbn_list[-1:-4:-1]
    indices = pd.Series(df.index, index=df["isbn"])
    # 전달받은 책들의 인덱스 저장
    book_indices = [indices[isbn] for isbn in isbn_list]
    sim_scores = [[i, 0] for i in range(tfidf_matrix.shape[0])]
    tmp_sim_scores = np.zeros(tfidf_matrix.shape[0])

    for idx in book_indices:
        cos_sim = cosine_similarity(tfidf_matrix[idx], tfidf_matrix)
        # 가중치처리를 할 수 있을까?

        # 해당 책과 다른 책들의 점수를 더하기
        tmp_sim_scores += cos_sim[0]

    # 유사도 + 가중치 처리한 결과 더해줌
    for i in range(len(tmp_sim_scores)):
        sim_scores[i][1] = tmp_sim_scores[i]

    # 점수를 기준으로 내림차순 정렬
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    idxls = []
    for i in range(len(sim_scores)):
        if sim_scores[i][0] in book_indices:
            idxls.append(i)
    for i in idxls:
        sim_scores.remove(sim_scores[i])
    # 점수가 가장 높은 책 4권 추천
    sim_scores = sim_scores[2:6]

    # 가장 유사한 책 8권의 인덱스
    book_indices = [i[0] for i in sim_scores]

    return list(df.iloc[book_indices]["isbn"])
