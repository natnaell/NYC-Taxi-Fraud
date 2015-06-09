BEGIN;
ALTER TABLE taxi.combined ADD COLUMN hour_of_day integer;
UPDATE taxi.combined
SET hour_of_day = extract(hour from pickupdatetime);
ALTER TABLE taxi.combined ADD COLUMN day_of_week integer;
UPDATE taxi.combined
SET day_of_week = extract(isodow from pickupdatetime);
ALTER TABLE taxi.combined ADD COLUMN month integer;
UPDATE taxi.combined
SET month = extract(month from pickupdatetime);
COMMIT;
CREATE INDEX CONCURRENTLY hack_ix ON taxi.combined (hack_license);
CREATE INDEX CONCURRENTLY pickup_ix ON taxi.combined (pickupdatetime);
CREATE INDEX CONCURRENTLY hour_ix ON taxi.combined (hour_of_day);
CREATE INDEX CONCURRENTLY day_ix ON taxi.combined (day_of_week);
CREATE INDEX CONCURRENTLY month_ix ON taxi.combined (month);
