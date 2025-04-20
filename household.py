import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

np.random.seed(42)
platforms = ['Wildberries', 'Яндекс Маркет']
categories = ['Кухонная утварь', 'Бытовая химия', 'Декор', 'Техника']
products = [
    'Сковорода с антипригарным покрытием', 'Блендер', 'Кофеварка', 'Сушилка для посуды',
    'Мешки для пылесоса', 'Капсулы для стирки', 'Швабра', 'Набор губок',
    'Картина на стену', 'Декоративная подушка', 'Настольная лампа', 'Ваза',
    'Тостер', 'Электрический чайник', 'Микроволновка', 'Аэрогриль'
]

data = []
for i in range(200):
    platform = np.random.choice(platforms)
    category = np.random.choice(categories)
    product = np.random.choice(products)
    original_price = np.random.randint(1000, 20000)
    discount_percent = np.random.uniform(5, 50) if platform == 'Wildberries' else np.random.uniform(10, 60)
    discounted_price = original_price * (1 - discount_percent / 100)
    data.append([platform, product, category, original_price, discounted_price, discount_percent])

df = pd.DataFrame(data, columns=['platform', 'product_name', 'category', 'original_price', 'discounted_price', 'discount_percent'])

conn = sqlite3.connect(':memory:')
df.to_sql('discounts', conn, index=False, if_exists='replace')

query1 = """
SELECT platform, category, AVG(discount_percent) as avg_discount
FROM discounts
GROUP BY platform, category
"""
avg_discounts = pd.read_sql_query(query1, conn)

query2 = """
SELECT platform, product_name, discount_percent
FROM (
    SELECT platform, product_name, discount_percent
    FROM discounts
    WHERE platform = 'Wildberries'
    ORDER BY discount_percent DESC
    LIMIT 5
) AS wb
UNION
SELECT platform, product_name, discount_percent
FROM (
    SELECT platform, product_name, discount_percent
    FROM discounts
    WHERE platform = 'Яндекс Маркет'
    ORDER BY discount_percent DESC
    LIMIT 5
) AS ym
"""
top_discounts = pd.read_sql_query(query2, conn)

pivot_table = avg_discounts.pivot(index='category', columns='platform', values='avg_discount')

plt.style.use('seaborn-v0_8')

fig1, ax1 = plt.subplots(figsize=(10, 6))
pivot_table.plot(kind='bar', ax=ax1)
ax1.set_title('Средний процент скидки по категориям и платформам')
ax1.set_xlabel('Категория')
ax1.set_ylabel('Средняя скидка (%)')
ax1.legend(title='Платформа')
plt.tight_layout()
plt.savefig('avg_discount_bar.png')
plt.close()

fig2, ax2 = plt.subplots(figsize=(8, 6))
sns.boxplot(x='platform', y='discount_percent', data=df,

 ax=ax2)
ax2.set_title('Распределение процентов скидки по платформам')
ax2.set_xlabel('Платформа')
ax2.set_ylabel('Процент скидки (%)')
plt.tight_layout()
plt.savefig('discount_boxplot.png')
plt.close()

print("Средние скидки по платформам и категориям:")
print(pivot_table)
print("\nТоп-5 товаров с максимальной скидкой по платформам:")
print(top_discounts)

conn.close()

