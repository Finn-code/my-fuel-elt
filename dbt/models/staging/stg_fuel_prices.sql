-- One row per week: official retail fuel prices in RM.
-- Only 'level' rows (actual prices); 'change_weekly' rows are excluded.

with source as (

    select *
    from {{ source('raw', 'fuelprice') }}
    where series_type = 'level'

)

select
    record_date                                     as price_date,
    (payload ->> 'ron95')::numeric(6, 2)            as ron95,
    (payload ->> 'ron97')::numeric(6, 2)            as ron97,
    (payload ->> 'diesel')::numeric(6, 2)           as diesel,
    (payload ->> 'diesel_eastmsia')::numeric(6, 2)  as diesel_east_my,
    (payload ->> 'ron95_budi95')::numeric(6, 2)     as ron95_budi95,
    (payload ->> 'ron95_skps')::numeric(6, 2)       as ron95_skps,
    (payload ->> 'diesel_budi')::numeric(6, 2)      as diesel_budi,
    (payload ->> 'diesel_skds')::numeric(6, 2)      as diesel_skds,
    loaded_at
from source