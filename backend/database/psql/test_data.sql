-- Additive table
INSERT INTO Additive (name, custom_expiry_modifier) VALUES 
('VITAMIN D', 0), 
('IRON', 0), 
('CALCIUM', 0), 
('PROBIOTIC ALPHA', 0), 
('OMEGA 3', 0) 
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
INSERT INTO Baby (id, name) VALUES 
(1, 'Emma Johnson'),
(2, 'Paul Johnson'),
(3, 'Liam Gonzalez'),
(4, 'Noah Ahmed'),
(5, 'Olivia Brown'),
(6, 'Sophia Li')
ON CONFLICT DO NOTHING;

-- Nurse table
INSERT INTO Nurse (id, name) VALUES 
(1, 'Nurse Joy'), 
(2, 'Nurse John'), 
(3, 'Nurse Evelyn'), 
(4, 'Nurse Bob'), 
(5, 'Nurse Clara')
ON CONFLICT DO NOTHING;

-- Milk table
INSERT INTO Milk (id, expiry, expressed, frozen, volume, fed, defrosted, donated_id, verified_id) VALUES 
('f1ea645f-4efa-4612-889c-0f271548bd83', '2024-01-15 12:00:00', '2023-12-10 08:00:00', TRUE, 200, FALSE, FALSE, NULL, 1),
('60253dad-74e8-4ec7-abb7-ec91bc7d39f7', '2024-02-20 14:00:00', '2023-12-11 09:00:00', TRUE, 200, FALSE, TRUE, NULL, 2),
('f67ea1e4-4aea-496b-b30b-41a76ba1394f', '2024-03-25 10:30:00', '2023-12-12 10:30:00', FALSE, 200, FALSE, FALSE, NULL, 3),
('be7e2418-37d4-42f3-bdb0-3fa3e7c95a84', '2024-04-30 08:00:00', '2023-12-13 11:00:00', FALSE, 200, FALSE, TRUE, NULL, 4),
('7301d088-aed2-4810-9412-4389a3965f44', '2024-05-10 11:15:00', '2023-12-14 12:15:00', TRUE, 200, FALSE, FALSE, NULL, 5),
('05ce303e-a473-4ef7-906a-ba6471f5a880', '2024-05-10 11:15:00', '2023-12-14 12:15:00', TRUE, 200, FALSE, FALSE, NULL, NULL),
('c749124d-cbb6-423e-a354-df6cc92786ae', '2024-05-10 11:15:00', '2023-12-14 12:15:00', TRUE, 200, FALSE, FALSE, NULL, NULL)
ON CONFLICT DO NOTHING;

-- Contains table
INSERT INTO Contains (milk_id, additive_name, amount) VALUES 
('f1ea645f-4efa-4612-889c-0f271548bd83', 'VITAMIN D', 100), 
('60253dad-74e8-4ec7-abb7-ec91bc7d39f7', 'IRON', 200), 
('f67ea1e4-4aea-496b-b30b-41a76ba1394f', 'CALCIUM', 150), 
('be7e2418-37d4-42f3-bdb0-3fa3e7c95a84', 'PROBIOTIC ALPHA', 250), 
('7301d088-aed2-4810-9412-4389a3965f44', 'OMEGA 3', 300)
ON CONFLICT DO NOTHING;

-- ExpressedBy table
INSERT INTO ExpressedBy (milk_id, mother_id) VALUES 
('f1ea645f-4efa-4612-889c-0f271548bd83', 1), 
('60253dad-74e8-4ec7-abb7-ec91bc7d39f7', 2), 
('f67ea1e4-4aea-496b-b30b-41a76ba1394f', 3), 
('be7e2418-37d4-42f3-bdb0-3fa3e7c95a84', 4), 
('7301d088-aed2-4810-9412-4389a3965f44', 5),
('05ce303e-a473-4ef7-906a-ba6471f5a880', 5),
('c749124d-cbb6-423e-a354-df6cc92786ae', 1)
ON CONFLICT DO NOTHING;

-- ExpressedFor table
INSERT INTO ExpressedFor (milk_id, baby_id) VALUES 
('f1ea645f-4efa-4612-889c-0f271548bd83', 1), 
('60253dad-74e8-4ec7-abb7-ec91bc7d39f7', 2), 
('f67ea1e4-4aea-496b-b30b-41a76ba1394f', 3), 
('be7e2418-37d4-42f3-bdb0-3fa3e7c95a84', 4), 
('7301d088-aed2-4810-9412-4389a3965f44', 5),
('05ce303e-a473-4ef7-906a-ba6471f5a880', 5),
('c749124d-cbb6-423e-a354-df6cc92786ae', 1)
ON CONFLICT DO NOTHING;

-- MotherOf table
INSERT INTO MotherOf (baby_id, mother_id) VALUES 
(1, 1), 
(2, 1),
(3, 2), 
(4, 3), 
(5, 4), 
(6, 5)
ON CONFLICT DO NOTHING;

-- AssignedTo table
INSERT INTO AssignedTo (baby_id, nurse_id) VALUES 
(1, 1), 
(2, 1), 
(3, 2), 
(4, 3), 
(5, 4), 
(6, 5)
ON CONFLICT DO NOTHING;
