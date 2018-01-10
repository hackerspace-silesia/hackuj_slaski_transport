SELECT * FROM stops
WITH a AS (
SELECT min(trip_id) AS trip_id
FROM trips 
WHERE direction_id=0 AND service_id='WKDY' 
GROUP BY route_id
),
b AS (
SELECT the_geom, trip_id, stop_sequence, stop_id
FROM stop_times
WHERE trip_id IN (SELECT trip_id FROM a)
), 
c AS (
SELECT the_geom, trip_id, stop_sequence, 
  stop_sequence AS stop_sequence_true, stop_id
FROM b
UNION ALL
SELECT the_geom, trip_id, stop_sequence-1  AS stop_sequence, 
  stop_sequence AS stop_sequence_true, stop_id
FROM b
),
d AS (
SELECT ST_MakeLine(the_geom ORDER BY trip_id, stop_sequence_true ASC) AS the_geom, 
trip_id, stop_sequence AS stop_sequence_start, (stop_sequence+1) AS stop_sequence_end, 
array_agg(stop_id ORDER BY stop_sequence_true) AS stop_id_array
FROM c
GROUP BY trip_id, stop_sequence
),
e AS (
SELECT * 
FROM d
WHERE array_length(stop_id_array,1)>1
),
f AS (
SELECT the_geom, trip_id, stop_id_array, 
  ST_Azimuth(ST_Line_Interpolate_Point(the_geom,0), ST_Line_Interpolate_Point(the_geom,1))/(2*pi())*360 AS direction
FROM e
),
g AS (
SELECT the_geom, trip_id, stop_id_array, (direction > 0 AND direction < 180) AS reverse
FROM f
),
h AS (
SELECT the_geom, trip_id, stop_id_array, reverse, 
  row_number() over (PARTITION BY the_geom ORDER BY trip_id, reverse) as offset_id
FROM g
ORDER BY the_geom, trip_id
),
i AS (
SELECT COUNT(*) AS overlap_count, the_geom 
FROM h 
GROUP BY the_geom
),
j AS (
SELECT h.the_geom, h.trip_id, h.stop_id_array, h.reverse,
(-0.5*i.overlap_count+(h.offset_id-0.5)) AS offset_dist
FROM h 
JOIN i 
ON h.the_geom = i.the_geom
),
k AS (
SELECT *, offset_dist*(-1) AS offset_factor
FROM j
WHERE reverse=true
UNION ALL
SELECT *, offset_dist AS offset_factor
FROM j
WHERE reverse=false
),
l AS (
SELECT k.*, z.route_id
FROM k
LEFT JOIN trips z
ON k.trip_id = z.trip_id
)
SELECT *, ST_Transform(the_geom,3857) AS the_geom_webmercator
FROM l