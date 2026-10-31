-- Malaysian fuel prices should never be below RM0.50 or above RM10.
-- Anything outside that is almost certainly a data error (e.g. 21.5 instead of 2.15).

select price_date, ron95, ron97, diesel
from {{ ref('stg_fuel_prices') }}
where ron95  not between 0.5 and 10
   or ron97  not between 0.5 and 10
   or diesel not between 0.5 and 10