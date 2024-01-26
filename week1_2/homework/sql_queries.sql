--Q3 - Count records
select 
    count(*) 
from 
    green_taxi_data
where
    date(lpep_pickup_datetime) = '2019-09-18' and date(lpep_dropoff_datetime) = '2019-09-18'

--Q4 - Largest trip for each day
--Sol1
select 
    lpep_pickup_datetime
    , max(trip_distance) 
from 
    green_taxi_data 
group by 1 
order by 2 desc 
limit 3; 

--Sol2
select 
    lpep_pickup_datetime
    , dense_rank() over(order by trip_distance desc) as rank 
from 
    green_taxi_data 
order by 2 
limit 3;  


--Q5 - Three biggest pick up Boroughs

select 
    z."Borough"
    , sum(g.total_amount) as total 
from 
    green_taxi_data g 
inner join 
    zones_data z 
        on g."PULocationID" = z."LocationID"  
where 
    z."Borough" != 'Unknown' and date(g.lpep_pickup_datetime) = '2019-09-18' 
group by z."Borough";


-- Q6 - Largest tip

Select
    drope."Zone"
     , dense_rank() over (order by g.tip_amount desc) as rank
 from 
     green_taxi_data g 
 inner join 
     zones_data pick 
     on g."PULocationID" = pick."LocationID" 
 inner join
     zones_data drope
     on g."DOLocationID" =  drope."LocationID"
 where 
      date(g.lpep_pickup_datetime) between '2019-09-01' and '2019-09-30' and  pick."Zone" = 'Astoria'
 limit 4;