ALTER TABLE "shop"."tasks" ENABLE ROW LEVEL SECURITY;

CREATE POLICY M__W__update ON "shop"."tasks"
    FOR UPDATE
	TO manager, worker
    USING (true)
	WITH CHECK (author = current_user or executor = current_user);

CREATE POLICY M__W__select ON "shop"."tasks" 
    FOR SELECT
	TO manager, worker 
    USING (author = current_user or executor = current_user);


CREATE POLICY A__all ON "shop"."tasks"
    TO "admin"
    USING (true)
    WITH CHECK (true);