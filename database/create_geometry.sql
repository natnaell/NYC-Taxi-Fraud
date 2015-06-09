ALTER TABLE taxi.combined ADD COLUMN geom geometry(Point,26918);
UPDATE taxi.combined SET geom = ST_Transform(ST_SetSRID(ST_MakePoint(pickup_longitude, pickup_latitude), 4326),26918);
ALTER TABLE taxi.combined RENAME COLUMN geom TO pickup_point;
ALTER TABLE taxi.combined ADD COLUMN dropoff_point geometry(Point,26918);
UPDATE taxi.combined SET dropoff_point = ST_Transform(ST_SetSRID(ST_MakePoint(dropoff_longitude, dropoff_latitude), 4326),26918);
--ALTER TABLE taxi.combined ADD COLUMN pickup_dropoff_multipoint geometry(MULTIPOINT, 26918);
--UPDATE taxi.combined SET pickup_dropoff_multipoint = ST_Transform(ST_SetSRID(ST_MakePoint(dropoff_longitude, dropoff_latitude), 4326),26918);
