DROP SCHEMA IF EXISTS shop CASCADE;

CREATE SCHEMA "shop";

CREATE TABLE "shop"."organizations"(
    "id" SERIAL PRIMARY KEY,
    "name" VARCHAR(100) NOT NULL,
    "location" VARCHAR(100) NOT NULL,
    "postal_code" VARCHAR(20),
    "first_contract_date" DATE
);

CREATE INDEX "ix_organizations_name" ON "shop"."organizations" ("name");

CREATE INDEX "ix_organizations_location" ON "shop"."organizations" ("location");

CREATE TABLE "shop"."contact_persons"(
    "id" SERIAL PRIMARY KEY,
    "first_name" VARCHAR(100) NOT NULL,
    "second_name" VARCHAR(100) NOT NULL,
    "email" VARCHAR(100) NOT NULL,
    "tel" VARCHAR(15),
    "organization_id" INT REFERENCES "shop"."organizations"("id") NOT NULL,
    UNIQUE("first_name", "second_name", "email")
);

CREATE INDEX "ix_contact_persons_first_name_second_name" ON "shop"."contact_persons" ("first_name", "second_name");

CREATE TABLE "shop"."equipment_positions" (
    "id" SERIAL PRIMARY KEY,
    "name" VARCHAR(100) NOT NULL,
    "description" TEXT,
    "price" NUMERIC(10, 2) NOT NULL
);

CREATE TABLE "shop"."equipment_balance" (
    "id" SERIAL PRIMARY KEY,
    "position_id" INT REFERENCES "shop"."equipment_positions"("id") NOT NULL,
    "serial_number" VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE "shop"."contract_type" (
    "id" SERIAL2 PRIMARY KEY,
    "type" VARCHAR(25) NOT NULL UNIQUE
);

CREATE TABLE "shop"."contract" (
    "id" SERIAL PRIMARY KEY,
    "name" VARCHAR(100) NOT NULL,
    "description" TEXT,
    "type_id" INT2 REFERENCES "shop"."contract_type" ("id") NOT NULL,
    "organization_id" INT REFERENCES "shop"."organizations" ("id") NOT NULL
);

CREATE TABLE "shop"."contract_equipment" (
    "id" SERIAL PRIMARY KEY,
    "contract_id" INT REFERENCES "shop"."contract" ("id") NOT NULL,
    "concrete_equipment_id" INT REFERENCES "shop"."equipment_balance" ("id") NOT NULL
);

CREATE TABLE "shop"."task_type" (
    "id" SERIAL2 PRIMARY KEY,
    "type" VARCHAR(25) NOT NULL UNIQUE
);

CREATE TABLE "shop"."priority" (
    "id" SERIAL2 PRIMARY KEY,
    "priority" VARCHAR(25) NOT NULL UNIQUE
);

CREATE TABLE "shop"."tasks" (
    "id" SERIAL PRIMARY KEY,
    "title" VARCHAR(100) NOT NULL,
    "description" TEXT,
    "priority_id" INT2 REFERENCES "shop"."priority" ("id") NOT NULL DEFAULT 0,
    "type_id" INT2 REFERENCES "shop"."task_type" ("id") NOT NULL,
    "open_date" DATE NOT NULL DEFAULT current_date,
    "close_date" DATE,
    "due_date" DATE,
    "completed" BOOLEAN NOT NULL DEFAULT False,
    "author" VARCHAR(100) NOT NULL,
    "executor" VARCHAR(100) NOT NULL,
    "contract_id" INT REFERENCES "shop"."contract" ("id"),
    "contact_person_id" INT REFERENCES "shop"."contact_persons" ("id") NOT NULL
);