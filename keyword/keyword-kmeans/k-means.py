import json
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# 1. 키워드 데이터 준비
keywords = [
    "커피", "아메리카노", "라떼", "카페", "디저트", "케이크", "쿠키", "책", "소설",
    "에세이", "영화", "드라마", "액션", "로맨스", "여행", "바다", "산", "음악", "팝", "클래식"
]

# 2. 키워드 벡터화 (TF-IDF)
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(keywords)

# 3. 최적의 클러스터 개수 찾기 (Elbow Method - 생략 가능)
# ... (Elbow Method 코드 생략)

# 4. K-means 클러스터링
kmeans = KMeans(n_clusters=5, random_state=0)  # 클러스터 개수 (K) 설정
kmeans.fit(X)

# 5. 클러스터별 키워드 출력
clusters = {}
for i, label in enumerate(kmeans.labels_):
    if label not in clusters:
        clusters[label] = []
    clusters[label].append(keywords[i])
print(clusters)

# 6. 유사도 기반 연결 관계 생성
similarity_matrix = cosine_similarity(X)
edges = []
for i, keyword in enumerate(keywords):
    for j, other_keyword in enumerate(keywords):
        if i != j and similarity_matrix[i, j] > 0.5:  # 유사도 임계값 설정
            edges.append({"from": keyword, "to": other_keyword})

# 7. Vis.js 데이터 생성
nodes = [{"id": keyword, "label": keyword} for keyword in keywords]
graph_data = {"nodes": nodes, "edges": edges}

# 8. JSON 파일로 저장
with open("mindmap_data.json", "w") as f:
    json.dump(graph_data, f)

# 9. HTML 파일 생성 (Vis.js 포함)
html_content = """
<!DOCTYPE html>
<html>
<head>
  <title>Keyword Mindmap</title>
  <script type="text/javascript" src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
  <style type="text/css">
    #mynetwork {
      width: 900px;
      height: 600px;
      border: 1px solid lightgray;
    }
  </style>
</head>
<body>
  <div id="mynetwork"></div>
  <script type="text/javascript">
    // JSON 데이터 로드
    var graphData = %s;

    // Vis.js 네트워크 생성
    var container = document.getElementById('mynetwork');
    var network = new vis.Network(container, graphData);
  </script>
</body>
</html>
""" % json.dumps(graph_data)

with open("mindmap.html", "w") as f:
    f.write(html_content)
