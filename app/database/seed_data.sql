DELETE FROM doctor_locations;
DELETE FROM doctors;
DELETE FROM locations;
DELETE FROM doctor_availability;

INSERT INTO doctors(id, first_name, last_name) VALUES (0, 'Jane', 'Wright');
INSERT INTO doctors(id, first_name, last_name) VALUES (1, 'Joseph', 'Lister');

INSERT INTO locations(id, address) VALUES (0, '1 Park St');
INSERT INTO locations(id, address) VALUES (1, '2 University Ave');

INSERT INTO doctor_locations(id, doctor_id, location_id) VALUES (0, 0, 0);
INSERT INTO doctor_locations(id, doctor_id, location_id) VALUES (1, 1, 0);
INSERT INTO doctor_locations(id, doctor_id, location_id) VALUES (2, 1, 1);

-- Insert availabilities
INSERT INTO doctor_availability(id, doctor_id, day_of_week, location_id, start_time, end_time, is_available)
VALUES (0, 0, 'Monday', 0, '09:00', '12:00', 1);
INSERT INTO doctor_availability(id, doctor_id, day_of_week, location_id, start_time, end_time, is_available)
VALUES (1, 1, 'Monday', 1, '14:00', '17:00', 1);
INSERT INTO doctor_availability(id, doctor_id, day_of_week, location_id, start_time, end_time, is_available)
VALUES (2, 0, 'Tuesday', 0, '10:00', '13:00', 1);
