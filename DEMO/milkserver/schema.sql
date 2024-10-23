CREATE TABLE IF NOT EXISTS Mother (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    age INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS Baby (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    allergens TEXT
);

CREATE TABLE IF NOT EXISTS Is_Mother_Of (
    mother_id SERIAL NOT NULL,
    baby_id SERIAL NOT NULL,
    PRIMARY KEY (mother_id, baby_id),
    FOREIGN KEY (mother_id) REFERENCES Mother(id),
    FOREIGN KEY (baby_id) REFERENCES Baby(id)
);

CREATE TABLE IF NOT EXISTS Milk (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    volume INTEGER NOT NULL,
    additives TEXT,
    expiry TIMESTAMP NOT NULL,
    expressed_at TIMESTAMP NOT NULL,
    expressed_by SERIAL NOT NULL,
    FOREIGN KEY (expressed_by) REFERENCES Mother(id)
);

CREATE TABLE IF NOT EXISTS Feed (
    baby SERIAL NOT NULL,
    milk SERIAL NOT NULL,
    FOREIGN KEY (baby) REFERENCES Baby(id),
    FOREIGN KEY (milk) REFERENCES Milk(id),
    PRIMARY KEY (baby, milk),
    volume INTEGER NOT NULL,
    feed_time TIMESTAMP NOT NULL
);