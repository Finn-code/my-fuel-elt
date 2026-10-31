-- Prices are announced roughly weekly. Any gap longer than 10 days
-- means announcements are missing from the source.
-- (10, not 7, because announcement days vary, e.g. Tuesday 2025-09-30.)
{{ config(severity = 'warn') }}

-- Prices are announced roughly weekly. Gaps longer than 10 days are flagged.
-- Known, legitimate gaps: mid-2018 to mid-2019, when prices were frozen after
-- GE14 and announced monthly. Any NEW gap outside that period needs investigating.
with ordered as (

    select
        price_date,
        lag(price_date) over (order by price_date) as previous_date
    from {{ ref('stg_fuel_prices') }}

)

select
    previous_date,
    price_date,
    price_date - previous_date as gap_days
from ordered
where price_date - previous_date > 10