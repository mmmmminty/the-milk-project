CREATE SCHEMA IF NOT EXISTS public;

CREATE TABLE IF NOT EXISTS Additive (
    name VARCHAR(255) PRIMARY KEY NOT NULL,
    custom_expiry_modifier INTEGER
);

CREATE TABLE IF NOT EXISTS Mother (
    id INTEGER PRIMARY KEY NOT NULL,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS Baby (
    id UUID PRIMARY KEY NOT NULL,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS Nurse (
    id INTEGER PRIMARY KEY NOT NULL,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS DonatedMilk (
    id INTEGER PRIMARY KEY NOT NULL
);

CREATE TABLE IF NOT EXISTS Milk (
    id UUID PRIMARY KEY NOT NULL, 
    expiry TIMESTAMP,
    expressed TIMESTAMP,
    volume INTEGER,
    frozen BOOLEAN NOT NULL,
    defrosted BOOLEAN NOT NULL,
    fed BOOLEAN NOT NULL,
    donated_id INTEGER,
    verified_id INTEGER,
    FOREIGN KEY (verified_id) REFERENCES Nurse(id) ON DELETE SET NULL,
    FOREIGN KEY (donated_id) REFERENCES DonatedMilk(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Contains (
    milk_id UUID NOT NULL,
    additive_name VARCHAR(255) NOT NULL,
    amount INTEGER NOT NULL,
    FOREIGN KEY (milk_id) REFERENCES Milk(id) ON DELETE CASCADE,
    FOREIGN KEY (additive_name) REFERENCES Additive(name),
    PRIMARY KEY (milk_id, additive_name)
);

CREATE TABLE IF NOT EXISTS ExpressedBy (
    milk_id UUID NOT NULL,
    mother_id INTEGER NOT NULL,
    FOREIGN KEY (milk_id) REFERENCES Milk(id) ON DELETE CASCADE,
    FOREIGN KEY (mother_id) REFERENCES Mother(id) ON DELETE CASCADE,
    PRIMARY KEY (milk_id, mother_id)
);

CREATE TABLE IF NOT EXISTS ExpressedFor (
    milk_id UUID NOT NULL,
    baby_id UUID NOT NULL,
    FOREIGN KEY (milk_id) REFERENCES Milk(id) ON DELETE CASCADE,
    FOREIGN KEY (baby_id) REFERENCES Baby(id) ON DELETE CASCADE,
    PRIMARY KEY (milk_id, baby_id)
);

CREATE TABLE IF NOT EXISTS MotherOf (
    baby_id UUID NOT NULL,
    mother_id INTEGER NOT NULL,
    FOREIGN KEY (baby_id) REFERENCES Baby(id) ON DELETE CASCADE,
    FOREIGN KEY (mother_id) REFERENCES Mother(id) ON DELETE CASCADE,
    PRIMARY KEY (baby_id, mother_id)
);

CREATE TABLE IF NOT EXISTS AssignedTo (
    baby_id UUID NOT NULL,
    nurse_id INTEGER NOT NULL,
    FOREIGN KEY (baby_id) REFERENCES Baby(id) ON DELETE CASCADE,
    FOREIGN KEY (nurse_id) REFERENCES Nurse(id) ON DELETE CASCADE,
    PRIMARY KEY (baby_id, nurse_id)
);

-- CREATE VIEW sorted_milk AS SELECT * FROM Milk ORDER BY expiry ASC;
CREATE VIEW unverified_milk AS
SELECT *
FROM Milk
WHERE verified_id IS NULL;
