import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

headers = {"User-Agent": "Mozilla/5.0"}

sitemap_url = "https://faradars.org/sitemap.xml"

r = requests.get(sitemap_url, headers=headers)
soup = BeautifulSoup(r.text, "xml")

courses = []

for loc in soup.find_all("loc"):
    url = loc.text.strip()

    if "/courses/" in url:
        cr = requests.get(url, headers=headers)
        cs = BeautifulSoup(cr.text, "html.parser")

        title = cs.find("h1")
        desc = cs.find("meta", {"name": "description"})

        courses.append({
            "title": title.text.strip() if title else "نامشخص",
            "description": desc["content"] if desc else "بدون توضیح",
            "source": "faradars",
            "url": url
        })

        time.sleep(1)

        if len(courses) == 5:
            break

df = pd.DataFrame(courses)
df.to_csv("courses_faradars.csv", index=False, encoding="utf-8-sig")

print("✅ خزش فرادرس از Sitemap انجام شد")
print("تعداد دوره‌ها:", len(courses))
