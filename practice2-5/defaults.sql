DO
$body$
    DECLARE
        organization_id INTEGER;
        contract_id INTEGER;
    BEGIN
        --- ENUMS
        INSERT INTO
            "shop"."contract_type" ("type")
        VALUES
            ('supply'),
            ('installation'),
            ('service'),
            ('warranty repair'),
            ('post-warranty repair')
        ON CONFLICT DO NOTHING;

        INSERT INTO
            "shop"."task_type" ("type")
        VALUES
            ('call'),
            ('email'),
            ('meeting'),
            ('contract service')
        ON CONFLICT DO NOTHING;

        INSERT INTO
            "shop"."priority" ("priority")
        VALUES
            ('low'),
            ('medium'),
            ('high')
        ON CONFLICT DO NOTHING;

        --- Organization, eqipment, contact persons, contract
        INSERT INTO
            "shop"."organizations" ("name", "location", "postal_code", "first_contract_date")
        VALUES
            ('ООО Рога и Копыта', 'г. Москва, ул. Пушкина д. 5к1с1', '188213', current_date)
        RETURNING id INTO organization_id;

        INSERT INTO
            "shop"."contact_persons" ("first_name", "last_name", "email", "tel", "organization_id")
        VALUES 
            ('Иван', 'Иванов', 'ivanov.ivan@org.id', '+79995551122', organization_id);

        INSERT INTO
            "shop"."contract" ("name", "description", "type_id", "organization_id")
        VALUES
            ('Договор поставки оборудования 111147299', '', (SELECT id FROM "shop"."contract_type" WHERE "type" = 'supply'), organization_id)
        RETURNING id INTO contract_id;
        
        INSERT INTO 
            "shop"."equipment_positions" ("name", "description", "price")
        VALUES 
            ('Принтер', 'Принтер для печати документов', 10000),
            ('Сканер', 'Сканер для сканирования документов', 20000),
            ('Компьютер', 'Компьютер для работы с документами', 30000),
            ('МФУ', 'МФУ для печати и сканирования документов', 40000),
            ('Сервер', 'Сервер для хранения документов', 50000);

        INSERT INTO 
            "shop"."equipment_balance" ("position_id", "serial_number")
        VALUES 
            ((SELECT id FROM "shop"."equipment_positions" WHERE "name" = 'Принтер'), '000000001'),
            ((SELECT id FROM "shop"."equipment_positions" WHERE "name" = 'Сканер'), '000000002'),
            ((SELECT id FROM "shop"."equipment_positions" WHERE "name" = 'Компьютер'), '000000003'),
            ((SELECT id FROM "shop"."equipment_positions" WHERE "name" = 'МФУ'), '000000004'),
            ((SELECT id FROM "shop"."equipment_positions" WHERE "name" = 'Сервер'), '000000005'),
            ((SELECT id FROM "shop"."equipment_positions" WHERE "name" = 'Сервер'), '100000005');

        INSERT INTO
            "shop"."contract_equipment" ("contract_id", "concrete_equipment_id")
        VALUES 
            (contract_id, (SELECT id FROM "shop"."equipment_balance" WHERE serial_number = '100000005')),
            (contract_id, (SELECT id FROM "shop"."equipment_balance" WHERE serial_number = '000000003'));

        --- Manager user
        CREATE USER default_worker1 IN ROLE worker ENCRYPTED PASSWORD '1234';
        CREATE USER default_worker2 IN ROLE worker ENCRYPTED PASSWORD '1234';
        CREATE USER default_manager1 IN ROLE manager ENCRYPTED PASSWORD '1234';
        CREATE USER default_manager2 IN ROLE manager ENCRYPTED PASSWORD '1234';

        --- Create tasks
        INSERT INTO
            "shop"."tasks" ("title", "description", "priority_id", "type_id", "due_date", "author", "executor", "contract_id", "contact_person_id")
        VALUES 
            ('Задача 1', 'Описание задачи 1', (SELECT id FROM "shop"."priority" WHERE "priority" = 'low'), (SELECT id FROM "shop"."task_type" WHERE "type" = 'meeting'), current_date + 1, 'default_manager1', 'default_worker1', contract_id, (SELECT id FROM "shop"."contact_persons" WHERE "first_name" = 'Иван')),
            ('Задача 2', 'Описание задачи 2', (SELECT id FROM "shop"."priority" WHERE "priority" = 'medium'), (SELECT id FROM "shop"."task_type" WHERE "type" = 'call'), current_date + 2, 'default_manager1', 'default_worker2', contract_id, (SELECT id FROM "shop"."contact_persons" WHERE "first_name" = 'Иван')),
            ('Задача 3', 'Описание задачи 3', (SELECT id FROM "shop"."priority" WHERE "priority" = 'high'), (SELECT id FROM "shop"."task_type" WHERE "type" = 'email'), current_date + 3, 'default_manager2', 'default_worker1', contract_id, (SELECT id FROM "shop"."contact_persons" WHERE "first_name" = 'Иван')),
            ('Задача 4', 'Описание задачи 4', (SELECT id FROM "shop"."priority" WHERE "priority" = 'low'), (SELECT id FROM "shop"."task_type" WHERE "type" = 'contract service'), current_date + 4, 'default_manager2', 'default_worker2', contract_id, (SELECT id FROM "shop"."contact_persons" WHERE "first_name" = 'Иван'));

    END;
$body$
LANGUAGE 'plpgsql'; 