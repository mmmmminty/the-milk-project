-- Additive table
INSERT INTO Additive (name) VALUES 
('Vitamin D'), 
('Iron'), 
('Calcium'), 
('Probiotics'), 
('Omega-3') 
ON CONFLICT DO NOTHING;

-- Mother table
INSERT INTO Mother (id, name) VALUES 
(1, 'Alice Johnson'), 
(2, 'Maria Gonzalez'), 
(3, 'Fatima Ahmed'), 
(4, 'Keisha Brown'), 
(5, 'Mei Li')
ON CONFLICT DO NOTHING;

-- Baby table
INSERT INTO Baby (id, name, dob) VALUES 
(1, 'Emma Johnson', '2023-05-10 08:30:00'),
(2, 'Liam Gonzalez', '2022-11-20 14:45:00'),
(3, 'Noah Ahmed', '2023-02-15 09:00:00'),
(4, 'Olivia Brown', '2023-01-25 07:30:00'),
(5, 'Sophia Li', '2023-06-05 12:20:00')
ON CONFLICT DO NOTHING;

-- Nurse table
INSERT INTO Nurse (id, name) VALUES 
(1, 'Nurse Joy'), 
(2, 'Nurse John'), 
(3, 'Nurse Evelyn'), 
(4, 'Nurse Bob'), 
(5, 'Nurse Clara')
ON CONFLICT DO NOTHING;

-- DonatedMilk table
INSERT INTO DonatedMilk (id, milk_id) VALUES 
(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)
ON CONFLICT DO NOTHING;

-- Milk table
INSERT INTO Milk (id, expiry, expressed, frozen, defrosted, modified, donated_id, verified_id) VALUES 
(1, '2024-01-15 12:00:00', '2023-12-10 08:00:00', TRUE, FALSE, FALSE, 1, 1),
(2, '2024-02-20 14:00:00', '2023-12-11 09:00:00', TRUE, TRUE, TRUE, 2, 2),
(3, '2024-03-25 10:30:00', '2023-12-12 10:30:00', FALSE, TRUE, FALSE, 3, 3),
(4, '2024-04-30 08:00:00', '2023-12-13 11:00:00', FALSE, FALSE, TRUE, 4, 4),
(5, '2024-05-10 11:15:00', '2023-12-14 12:15:00', TRUE, FALSE, FALSE, 5, 5)
ON CONFLICT DO NOTHING;

-- Contains table
INSERT INTO Contains (milk_id, additive_name, amount) VALUES 
(1, 'Vitamin D', 100), 
(2, 'Iron', 200), 
(3, 'Calcium', 150), 
(4, 'Probiotics', 250), 
(5, 'Omega-3', 300)
ON CONFLICT DO NOTHING;

-- ExpressedBy table
INSERT INTO ExpressedBy (milk_id, mother_id) VALUES 
(1, 1), 
(2, 2), 
(3, 3), 
(4, 4), 
(5, 5)
ON CONFLICT DO NOTHING;

-- ExpressedFor table
INSERT INTO ExpressedFor (milk_id, baby_id) VALUES 
(1, 1), 
(2, 2), 
(3, 3), 
(4, 4), 
(5, 5)
ON CONFLICT DO NOTHING;

-- MotherOf table
INSERT INTO MotherOf (baby_id, mother_id) VALUES 
(1, 1), 
(2, 2), 
(3, 3), 
(4, 4), 
(5, 5)
ON CONFLICT DO NOTHING;

-- AssignedTo table
INSERT INTO AssignedTo (baby_id, nurse_id) VALUES 
(1, 1), 
(2, 2), 
(3, 3), 
(4, 4), 
(5, 5)
ON CONFLICT DO NOTHING;
