CREATE OR REPLACE FUNCTION "shop"."reports_to_json"("users" varchar(100)[], "start_date" date, "end_date" date)
RETURNS JSONB
LANGUAGE plpgsql
AS
$$
DECLARE
	u varchar(100);
	reports JSONB := '[]'::JSONB;
BEGIN
	foreach u in array "users"
	loop
		 reports = reports || (SELECT ROW_TO_JSON(t) :: JSONB FROM (SELECT * FROM shop.create_report(u, "start_date", "end_date")) t);
	end loop;

	RETURN reports;
END;
$$