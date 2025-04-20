ЦЕЛЬ

Сравнить стратегии скидок двух крупнейших российских маркетплейсов.

МЕТОДЫ

Python с библиотеками pandas, sqlite3, matplotlib, seaborn, numpy

Столбчатая диаграмма: Показывает средний процент скидки по категориям для каждой платформы. Сохранена как avg_discount_bar.png.

Ящик с усами: Иллюстрирует распределение процентов скидок по платформам, включая медиану, квартили и выбросы. Сохранён как discount_boxplot.png.

SQL-ЗАПРОСЫ 

Запрос 1: Рассчитана средняя скидка по платформам и категориям товаров:

SELECT platform, category, AVG(discount_percent) as avg_discount
FROM discounts
GROUP BY platform, category

Запрос 2: Определены топ-5 товаров с максимальной скидкой для каждой платформы:

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

В КОНСОЛЬ ВЫВЕДЕНЫ

Сводная таблица средних скидок.

Список топ-5 товаров с максимальной скидкой для каждой платформы.

Визуализация: столбчатые диаграммы и boxplot

ОСНОВНЫЕ РЕЗУЛЬТАТЫ

Яндекс Маркет:

Больший диапазон скидок (10-60%)

Выше средние значения скидок

Более агрессивная скидочная политика

Wildberries:

Умеренные скидки (5-50%)

Более стабильное ценообразование

Равномерное распределение скидок по категориям

По всем категориям товаров Яндекс Маркет предлагает более высокие скидки

Наибольшая разница в скидках наблюдается в категориях "Техника" и "Декор"

Топовые скидки на Яндекс Маркет достигают максимального значения (60%), на Wildberries - 50%
