CREATE EXTENSION IF NOT EXISTS ltree;

CREATE TABLE units (
    id          SERIAL PRIMARY KEY,
    name        TEXT NOT NULL,
    unit_type   TEXT NOT NULL,  -- 'campus' | 'division' | 'department'
    path        LTREE NOT NULL UNIQUE
);

CREATE INDEX units_path_idx ON units USING GIST (path);

CREATE TABLE subpurposes (
    id              SERIAL PRIMARY KEY,
    name            TEXT NOT NULL,
    path            LTREE NOT NULL UNIQUE
);

CREATE TABLE funds (
    id              SERIAL PRIMARY KEY,
    fund_name       TEXT NOT NULL,
    unit_id         INTEGER NOT NULL,
    subpurpose_id   INTEGER NOT NULL,
    capacity_min    NUMERIC NOT NULL,
    fund_terms      TEXT,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),

    CONSTRAINT fk_funds_unit
        FOREIGN KEY (unit_id) REFERENCES units(id) ON DELETE RESTRICT,
    CONSTRAINT fk_funds_subpurposes
        FOREIGN KEY (subpurpose_id) REFERENCES subpurposes(id) ON DELETE RESTRICT,
    CONSTRAINT chk_capacity_nonnegative
        CHECK (capacity_min >= 0)
);