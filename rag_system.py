import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from tabulate import tabulate
import subprocess
import re

# -----------------------------------
# 1. Load database
# -----------------------------------
df = pd.read_csv("courses_all.csv").fillna("")

documents = (df["title"] + " " + df["description"]).tolist()

# -----------------------------------
# 2. Vectorize
# -----------------------------------
vectorizer = TfidfVectorizer(
    max_features=5000,
    ngram_range=(1, 2)
)
doc_vectors = vectorizer.fit_transform(documents)

# -----------------------------------
# 3. Query
# -----------------------------------
query = input("🔍 عبارت جستجو را وارد کنید: ").strip()
query_words = re.findall(r"\w+", query.lower())

query_vector = vectorizer.transform([query])
similarities = cosine_similarity(query_vector, doc_vectors).flatten()

# -----------------------------------
# 4. Filtering (IMPORTANT PART)
# -----------------------------------
SIM_THRESHOLD = 0.15  # آستانه شباهت

valid = []

for i, score in enumerate(similarities):
    text = (df.iloc[i]["title"] + " " + df.iloc[i]["description"]).lower()

    # شرط ۱: شباهت معنایی
    if score < SIM_THRESHOLD:
        continue

    # شرط ۲: حداقل یکی از کلمات کوئری داخل متن باشد
    if not any(word in text for word in query_words):
        continue

    valid.append((i, score))

# اگر هیچی نبود
if not valid:
    print("\n❌ هیچ نتیجه مرتبطی یافت نشد.")
    exit()

# -----------------------------------
# 5. Sort & select top
# -----------------------------------
valid = sorted(valid, key=lambda x: x[1], reverse=True)[:5]

results = []
for rank, (idx, score) in enumerate(valid, start=1):
    results.append([
        rank,
        df.iloc[idx]["title"],
        df.iloc[idx]["description"][:150],
        df.iloc[idx]["source"],
        df.iloc[idx]["url"]
    ])

# -----------------------------------
# 6. Show table
# -----------------------------------
headers = ["رتبه", "عنوان دوره", "بخشی از توضیح", "منبع", "لینک"]

print("\n📊 نتایج جستجوی معنایی:\n")
print(tabulate(results, headers=headers, tablefmt="grid"))

# -----------------------------------
# 7. RAG prompt
# -----------------------------------
context = ""
for r in results:
    context += f"- {r[1]} ({r[3]}): {r[2]}\n"

prompt = f"""
تو یک سیستم RAG هستی.
فقط از اطلاعات زیر استفاده کن.
اگر داده مرتبط وجود ندارد، صریح بگو وجود ندارد.

اطلاعات:
{context}

سوال:
{query}

پاسخ:
"""

result = subprocess.run(
    ["ollama", "run", "qwen2.5:7b"],
    input=prompt.encode("utf-8"),
    stdout=subprocess.PIPE
)

print("\n🧠 پاسخ نهایی سیستم:\n")
print(result.stdout.decode("utf-8", errors="ignore"))
