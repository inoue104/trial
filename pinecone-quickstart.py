#
# Pineconeのクイックスタートのコード
# https://docs.pinecone.io/docs/quickstart
#
# 実行する前にstarterのアカウントを作成して、api_keyとenvironmentの値をコピーする。
# 443

import pinecone
import time

pinecone.init(api_key="e29ee453-3784-4f12-axxx-fd9c148fdc91", environment="gcp-starter")

pinecone.create_index("quickstart", dimension=8, metric="euclidean")
pinecone.describe_index("quickstart")

index = pinecone.Index("quickstart")

index.upsert(
  vectors=[
    {"id": "vec1", "values": [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]},
    {"id": "vec2", "values": [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]},
    {"id": "vec3", "values": [0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3]},
    {"id": "vec4", "values": [0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4]}
  ],
  namespace="ns1"
)

index.upsert(
  vectors=[
    {"id": "vec5", "values": [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]},
    {"id": "vec6", "values": [0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6]},
    {"id": "vec7", "values": [0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7]},
    {"id": "vec8", "values": [0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8]}
  ],
  namespace="ns2"
)

time.sleep(20)

stats = index.describe_index_stats()
print(stats)

que1 = index.query(
  namespace="ns1",
  vector=[0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3],
  top_k=3,
  include_values=True
)
print(que1)

que2 = index.query(
  namespace="ns2",
  vector=[0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7],
  top_k=3,
  include_values=True
)
print(que2)

pinecone.delete_index("quickstart")

