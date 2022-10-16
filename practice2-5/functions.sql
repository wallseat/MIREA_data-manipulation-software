CREATE OR REPLACE FUNCTION "shop"."get_roles_list"()
RETURNS TABLE("role" TEXT)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY WITH RECURSIVE cte AS (
        SELECT oid FROM pg_roles WHERE rolname = current_user
        UNION ALL
        SELECT m.roleid
        FROM cte
        JOIN pg_auth_members m ON m.member = cte.oid
    )
    SELECT oid::regrole::text AS rolename FROM cte;
END;
$$;

CREATE OR REPLACE FUNCTION "shop"."process_check_completed"() 
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
    BEGIN
        IF (TG_OP = 'UPDATE') THEN
            IF (OLD.completed = True and 'admin' not in (SELECT "shop"."get_roles_list"())) THEN
                RAISE EXCEPTION 'Can not change completed task';
            END IF;
            NEW.close_date = current_date;
        END IF;
        RETURN NEW;
    END;
$$;

CREATE TRIGGER "check_completed"
BEFORE UPDATE ON "shop"."tasks"
    FOR EACH ROW EXECUTE PROCEDURE "shop"."process_check_completed"();


CREATE OR REPLACE FUNCTION "shop"."process_expire_complited_tasks"() 
RETURNS trigger
LANGUAGE plpgsql
    AS $$
        BEGIN
        DELETE FROM "shop"."tasks" WHERE close_date < current_date - INTERVAL '12 month';
        RETURN NEW;
    END;
$$;

CREATE TRIGGER expire_complited_tasks
AFTER INSERT OR UPDATE ON "shop"."tasks"
    FOR EACH ROW EXECUTE PROCEDURE "shop"."process_expire_complited_tasks"();

CREATE OR REPLACE FUNCTION "shop"."create_report"(user_ VARCHAR(100), date_start_ DATE, date_end_ DATE)
RETURNS TABLE(
    "user" VARCHAR(100),
    "date_start" DATE,
    "date_end" DATE,
    "task_count" INT,
    "completed_task_count" INT,
    "completed_out_of_date_task_count" INT,
    "not_completed_task_count" INT,
    "not_completed_out_of_date_task_count" INT
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY SELECT
        user_ as user,
        date_start_ as date_start,
        date_end_ as date_end,
        count(*) :: int as task_count,
        sum(case when completed and close_date <= due_date then 1 else 0 end) :: int as completed_task_count,
        sum(case when completed and close_date > due_date then 1 else 0 end) :: int as completed_out_of_date_task_count,
        sum(case when not completed and due_date >= current_date then 1 else 0 end) :: int as not_completed_task_count,
        sum(case when not completed and due_date < current_date then 1 else 0 end) :: int as not_completed_out_of_date_task_count
    FROM "shop"."tasks"
    WHERE executor = user_ and open_date between date_start_ and date_end_;
END;
$$;
