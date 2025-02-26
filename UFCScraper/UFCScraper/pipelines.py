from UFCScraper.items import FighterItem, FightItem
from psycopg2.errors import ForeignKeyViolation
from psycopg2.extras import Json
from dotenv import load_dotenv
import psycopg2
import os

load_dotenv()


class EventPipeline:
    def __init__(self):
        conn = psycopg2.connect(os.getenv("DB_URI"))
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY, 
                name TEXT,
                date TEXT,
                city TEXT,
                state TEXT,
                country TEXT,
                venue TEXT,
                last_updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
            ) 
            """
        )
        conn.commit()
        cursor.close()
        conn.close()

    def process_item(self, item, spider):
        conn = psycopg2.connect(os.getenv("DB_URI"))
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM events WHERE name=%s", (item["name"],))
        existing_event = cursor.fetchone()

        if existing_event:
            # update the event
            update_query = """
                UPDATE events
                SET name=%s, date=%s, city=%s, state=%s, country=%s, venue=%s, last_updated_at = CURRENT_TIMESTAMP
                WHERE id= %s
            """
            cursor.execute(
                update_query,
                (
                    item["name"],
                    item["date"],
                    item["city"],
                    item["state"],
                    item["country"],
                    item["venue"],
                    item["id"],
                ),
            )

            if cursor.rowcount > 0:
                print(f"Update successful. {cursor.rowcount} row(s) affected.")
            else:
                print("Update did not affect any rows.")

            conn.commit()

        else:
            ## warnings.warn(f"Event {item['name']} not found in database.... why....")
            insert_query = """
                INSERT INTO events (
                    id, name, date, city, state, country, venue, last_updated_at
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
            """
            cursor.execute(
                insert_query,
                (
                    item["id"],
                    item["name"],
                    item["date"],
                    item["city"],
                    item["state"],
                    item["country"],
                    item["venue"],
                ),
            )

            if cursor.rowcount > 0:
                print(f"Insert successful. {cursor.rowcount} row(s) affected.")
            else:
                print("Insert did not affect any rows.")

            conn.commit()

        cursor.close()
        conn.close()
        return item


class FighterPipeline:
    def __init__(self):
        conn = psycopg2.connect(os.getenv("DB_URI"))
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS fighters (
                id INTEGER PRIMARY KEY,
                first_name TEXT,
                last_name TEXT,
                nickname TEXT,
                status TEXT,
                wins SMALLINT, 
                losses SMALLINT,
                draws SMALLINT,
                weight_class TEXT,
                age SMALLINT,
                height SMALLINT,
                reach SMALLINT,
                leg_reach SMALLINT,
                hometown_city TEXT,
                hometown_state TEXT,
                hometown_country TEXT,
                trains_at_city TEXT,
                trains_at_state TEXT,
                trains_at_country TEXT,
                fighting_style TEXT,
                stance TEXT,
                url TEXT,
                last_updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
            ) 
        """
        )
        conn.commit()
        cursor.close()
        conn.close()

    def process_item(self, item, spider):
        if isinstance(item, FighterItem):
            conn = psycopg2.connect(os.getenv("DB_URI"))
            cursor = conn.cursor()
            insert_query = """
                INSERT INTO fighters (
                    id,
                    first_name, 
                    last_name,
                    nickname, 
                    wins, 
                    losses, 
                    draws, 
                    age, 
                    height, 
                    reach, 
                    hometown_city, 
                    hometown_state, 
                    hometown_country, 
                    trains_at_city, 
                    trains_at_state, 
                    trains_at_country, 
                    stance, 
                    url, 
                    last_updated_at
                ) VALUES (
                    %s, %s, %s, %s, %s, 
                    %s, %s, %s, %s, %s, 
                    %s, %s, %s, %s, %s, 
                    %s, %s, %s, 
                    CURRENT_TIMESTAMP
                ) 
                ON CONFLICT (id) DO UPDATE SET
                    first_name = EXCLUDED.first_name,
                    last_name = EXCLUDED.last_name,
                    wins = EXCLUDED.wins, 
                    losses = EXCLUDED.losses, 
                    draws = EXCLUDED.draws, 
                    age = EXCLUDED.age, 
                    height = EXCLUDED.height, 
                    reach = EXCLUDED.reach, 
                    hometown_city = EXCLUDED.hometown_city, 
                    hometown_state = EXCLUDED.hometown_state, 
                    hometown_country = EXCLUDED.hometown_country, 
                    trains_at_city = EXCLUDED.trains_at_city, 
                    trains_at_state = EXCLUDED.trains_at_state, 
                    trains_at_country = EXCLUDED.trains_at_country, 
                    stance = EXCLUDED.stance, 
                    url = EXCLUDED.url, 
                    last_updated_at = CURRENT_TIMESTAMP
            """
            cursor.execute(
                insert_query,
                (
                    item["id"],
                    item["first_name"],
                    item["last_name"],
                    item["nickname"],
                    item["wins"],
                    item["losses"],
                    item["draws"],
                    item["age"],
                    item["height"],
                    item["reach"],
                    item["hometown_city"],
                    item["hometown_state"],
                    item["hometown_country"],
                    item["trains_at_city"],
                    item["trains_at_country"],
                    item["trains_at_state"],
                    item["stance"],
                    item["url"],
                ),
            )
            conn.commit()

            if cursor.rowcount > 0:
                print(f"Insert successful. {cursor.rowcount} row(s) affected.")
            else:
                print("Insert did not affect any rows.")

            conn.close()
            return item


class FightPipeline:
    def __init__(self):
        conn = psycopg2.connect(os.getenv("DB_URI"))
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS fights (
                id INTEGER PRIMARY KEY,
                event_id INTEGER,
                r_fighter_id INTEGER,
                r_fighter_status TEXT,
                b_fighter_id INTEGER,
                b_fighter_status TEXT,
                round SMALLINT,
                time TEXT, 
                method TEXT,
                bout_weight TEXT,
                fight_stats JSONB,
                last_updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
                FOREIGN KEY (event_id) REFERENCES events (id),
                FOREIGN KEY (r_fighter_id) REFERENCES fighters (id),
                FOREIGN KEY (b_fighter_id) REFERENCES fighters (id)
            ) 
        """
        )
        conn.commit()
        cursor.close()
        conn.close()

    def process_item(self, item, spider):
        if isinstance(item, FightItem):
            conn = psycopg2.connect(os.getenv("DB_URI"))
            cursor = conn.cursor()
            try:
                insert_query = """
                    INSERT INTO fights
                    (
                        id,
                        event_id, 
                        r_fighter_id,
                        b_fighter_id,
                        r_fighter_status,
                        b_fighter_status,
                        round,
                        time,
                        method,
                        bout_weight,
                        url,
                        fight_stats,
                        last_updated_at
                    ) VALUES (
                        %s, %s, %s, %s, %s, 
                        %s, %s, %s, %s, %s, 
                        %s, %s,
                        CURRENT_TIMESTAMP
                    ) 
                    ON CONFLICT (id) DO UPDATE SET
                        id = EXCLUDED.id,
                        event_id = EXCLUDED.event_id,
                        r_fighter_id = EXCLUDED.r_fighter_id,
                        b_fighter_id = EXCLUDED.b_fighter_id,
                        r_fighter_status = EXCLUDED.r_fighter_status,
                        b_fighter_status = EXCLUDED.b_fighter_status,
                        round = EXCLUDED.round,
                        time = EXCLUDED.time,
                        method = EXCLUDED.method,
                        bout_weight = EXCLUDED.bout_weight,
                        url = EXCLUDED.url,
                        fight_stats = EXCLUDED.fight_stats,
                        last_updated_at = CURRENT_TIMESTAMP
                """
                cursor.execute(
                    insert_query,
                    (
                        item["id"],
                        item["event_id"],
                        item["r_fighter_id"],
                        item["b_fighter_id"],
                        item["r_fighter_status"],
                        item["b_fighter_status"],
                        item["round"],
                        item["time"],
                        item["method"],
                        item["bout_weight"],
                        item["url"],
                        Json(item["fight_stats"]),
                    ),
                )
                conn.commit()

                if cursor.rowcount > 0:
                    print(f"Insert successful. {cursor.rowcount} row(s) affected.")
                else:
                    print("Insert did not affect any rows.")

            except ForeignKeyViolation as e:
                with open('error_list_fights.log', 'a') as file:
                    file.write(f"{item['id']} :: {str(e.diag.message_detail)} \n")



            conn.close()
            return item
