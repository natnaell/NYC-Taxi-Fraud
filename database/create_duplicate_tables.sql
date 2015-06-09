CREATE TABLE taxi.dup_trips AS
 SELECT *
 FROM taxi.trips_all
 WHERE (medallion, hack_license, pickupdatetime) IN
 (SELECT medallion, hack_license, pickupdatetime
 FROM taxi.trips_all t2
 GROUP BY medallion, hack_license, pickupdatetime
 HAVING COUNT(*) > 1
 );

CREATE TABLE taxi.dup_fares AS
 SELECT *
 FROM taxi.fares_all
 WHERE (medallion, hack_license, pickupdatetime) IN
 (SELECT medallion, hack_license, pickupdatetime
 FROM taxi.fares_all t2
 GROUP BY medallion, hack_license, pickupdatetime
 HAVING COUNT(*) > 1
 );
