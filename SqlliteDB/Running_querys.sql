select
strftime('%Y',date) as YEAR,
strftime('%m',date) as MMONTH,
round(distance/1000,0) as RND_DISTANCE,
count(*) as vol,
SUM(DISTANCE) AS DISTANCE_RAN
from all_runs
group by 1,2,3
order by 1,2;


