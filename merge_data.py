import pandas as pd

# فرادرس (همون 5تایی که قبلاً داشتی)
df_f = pd.read_csv("courses_faradars.csv")

# سبزلرن
df_s = pd.read_csv("courses_sabzlearn.csv")

df_all = pd.concat([df_f, df_s], ignore_index=True)

df_all.to_csv("courses_all.csv", index=False, encoding="utf-8-sig")

print("✅ مرج انجام شد")
print("فرادرس:", len(df_f))
print("سبزلرن:", len(df_s))
print("کل دیتابیس:", len(df_all))
