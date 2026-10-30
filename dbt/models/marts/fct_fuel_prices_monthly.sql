-- Average fuel prices per month.

select
    date_trunc('month', price_date)::date  as price_month,
    round(avg(ron95), 2)                   as avg_ron95,
    round(avg(coalesce(ron95_budi95, ron95)), 2)  as avg_ron95_citizen,
    round(avg(ron97), 2)                   as avg_ron97,
    round(avg(diesel), 2)                  as avg_diesel,
    round(avg(diesel_east_my), 2)          as avg_diesel_east_my,
    count(*)                               as weeks_recorded
from {{ ref('stg_fuel_prices') }}
group by 1
order by 1