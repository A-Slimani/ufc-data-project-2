-- updating the event table with the api data
ALTER TABLE events
ADD COLUMN event_date TEXT,
ADD COLUMN city TEXT,
ADD COLUMN country TEXT,
ADD COLUMN venue TEXT,
DROP COLUMN date_raw,
DROP COLUMN location_raw,
DROP CONSTRAINT events_pkey, 
ADD PRIMARY KEY (name)