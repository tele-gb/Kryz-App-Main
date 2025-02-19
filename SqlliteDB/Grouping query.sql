SELECT
*,
"5ks_Secs"/"5ks_Vol" as "5ks_pace",
"10ks_Secs"/"10ks_Vol" as "10ks_pace"
FROM
(
select
strftime('%Y',date) as YEAR,
strftime('%m',date) as MMONTH,
sum(case when round(distance/1000.0,0) = 5.0 then 1 else 0 end)  "5ks_Vol",  
sum(case when round(distance/1000.0,0) BETWEEN 6 AND 9 then 1 else 0 end) "Between5&10k_Vol",   
sum(case when round(distance/1000.0,0) = 10.0 then 1 else 0 end)  "10ks_Vol",  
sum(case when round(distance/1000.0,0) > 10  then 1 else 0 end) "10ks+_Vol",
sum(case when round(distance/1000.0,0) = 5.0 then distance else 0 end)  "5ks_Dist",  
sum(case when round(distance/1000.0,0) BETWEEN 6 AND 9 then distance else 0 end) "Between5&10k_Dist",   
sum(case when round(distance/1000.0,0) = 10.0 then distance else 0 end)  "10ks_Dist",  
sum(case when round(distance/1000.0,0) > 10  then distance else 0 end) "10ks+_Dist",
sum(case when round(distance/1000.0,0) = 5.0 then Elapsed_Time else 0 end)  "5ks_Secs",  
sum(case when round(distance/1000.0,0) BETWEEN 6 AND 9 then Elapsed_Time else 0 end) "Between5&10k_Secs",   
sum(case when round(distance/1000.0,0) = 10.0 then Elapsed_Time else 0 end)  "10ks_Secs",  
sum(case when round(distance/1000.0,0) > 10  then Elapsed_Time else 0 end) "10ks+_Secs"
from all_runs
group by 1,2
order by 1,2)
;
