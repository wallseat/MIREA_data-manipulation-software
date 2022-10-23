
DROP ROLE IF EXISTS "admin";
CREATE ROLE "admin" LOGIN CREATEROLE ENCRYPTED PASSWORD 'supersecret';

DROP ROLE IF EXISTS "manager";
CREATE ROLE "manager" INHERIT;

DROP ROLE IF EXISTS "worker";
CREATE ROLE "worker" INHERIT;

REVOKE ALL ON schema public FROM public;
REVOKE ALL ON schema shop from manager, worker, public;

GRANT USAGE ON SCHEMA shop TO manager, worker;
GRANT SELECT ON ALL TABLES IN SCHEMA "shop" TO manager, worker, admin;

GRANT INSERT, UPDATE ON "shop"."tasks" TO manager;
GRANT UPDATE ("close_date", "completed") ON "shop"."tasks" TO worker;

GRANT EXECUTE ON FUNCTION "shop"."process_check_completed"() TO manager, worker;

GRANT ALL ON SCHEMA shop TO "admin";
