import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

headers = {"User-Agent": "Mozilla/5.0"}

base = "https://sabzlearn.ir"
url = "https://sabzlearn.ir/courses/"

r = requests.get(url, headers=headers, timeout=15)
soup = BeautifulSoup(r.text, "html.parser")

courses = []
visited = set()

for a in soup.find_all("a", href=True):
    href = a["href"]

    if "/course/" not in href:
        continue

    course_url = href if href.startswith("http") else base + href

    if course_url in visited:
        continue
    visited.add(course_url)

    try:
        cr = requests.get(course_url, headers=headers, timeout=10)
        cs = BeautifulSoup(cr.text, "html.parser")

        title = cs.find("h1")
        desc = cs.find("meta", {"name": "description"})

        if not title or not desc:
            continue

        courses.append({
            "title": title.text.strip(),
            "description": desc["content"].strip(),
            "source": "sabzlearn",
            "url": course_url
        })

        print(f"✅ اضافه شد: {title.text.strip()}")

        time.sleep(0.3)

        # فقط 5 تا
        if len(courses) == 5:
            break

    except Exception:
        continue

df = pd.DataFrame(courses)
df.to_csv("courses_sabzlearn.csv", index=False, encoding="utf-8-sig")

print("\n🎯 خزش سبزلرن تمام شد")
print("تعداد دوره‌ها:", len(df))
