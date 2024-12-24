-- Initialize the database.
-- Drop any existing data and create empty tables.

DROP TABLE IF EXISTS doctors;
DROP TABLE IF EXISTS locations;
DROP TABLE IF EXISTS doctor_locations;
DROP TABLE IF EXISTS doctor_availability;

CREATE TABLE doctors (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  first_name TEXT NOT NULL,
  last_name TEXT NOT NULL
);

CREATE TABLE locations (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  address TEXT NOT NULL
);

CREATE TABLE doctor_locations (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  doctor_id INTEGER NOT NULL,
  location_id INTEGER NOT NULL,
  FOREIGN KEY (doctor_id) REFERENCES doctors (id),
  FOREIGN KEY (location_id) REFERENCES locations (id)
);

-- The problem can also be solved in many ways like using anothe table in addition to below for storing
-- appointment detail. But I have just focused on the availability aspect. And minimum code changes that are required to 
-- handle this particular case of availability;
CREATE TABLE doctor_availability (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  doctor_id INTEGER NOT NULL,
  day_of_week TEXT NOT NULL CHECK (day_of_week IN ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')),
  location_id INTEGER NOT NULL,
  start_time TEXT NOT NULL,
  end_time TEXT NOT NULL,
  is_available INTEGER NOT NULL DEFAULT 1 CHECK (is_available IN (0, 1)),
  FOREIGN KEY (doctor_id) REFERENCES doctors (id)
  FOREIGN KEY (location_id) REFERENCES locations (id)
);

