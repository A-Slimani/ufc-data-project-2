from UFCScraper.items import EventItem, FighterItem, FightItem
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
                url TEXT PRIMARY KEY,
                name TEXT,
                location_raw TEXT,
                date_raw TEXT,
                last_updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
            ) 
            """
        )
        conn.commit()
        cursor.close()
        conn.close()

    def process_item(self, item, spider):
        if isinstance(item, EventItem):
            conn = psycopg2.connect(os.getenv("DB_URI"))
            cursor = conn.cursor()
            cursor.execute("SELECT url FROM events WHERE url=%s", (item["url"],))
            existing_event = cursor.fetchone()

            if existing_event:
                # update the event
                update_query = """
                    UPDATE events
                    SET name = %s, location_raw = %s, date_raw = %s, last_updated_at = CURRENT_TIMESTAMP
                    WHERE url = %s
                """
                cursor.execute(
                    update_query,
                    (item["url"], item["name"], item["location_raw"], item["date_raw"]),
                )
                conn.commit()

            else:
                insert_query = """
                    INSERT INTO events (
                        url, name, location_raw, date_raw, last_updated_at
                    ) VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)
                """
                cursor.execute(
                    insert_query,
                    (item["url"], item["name"], item["location_raw"], item["date_raw"]),
                )
                conn.commit()

            conn.close()
            return item


class FighterPipeline:
    def __init__(self):
        conn = psycopg2.connect(os.getenv("DB_URI"))
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS fighters (
                url TEXT PRIMARY KEY,
                name TEXT,
                nickname TEXT,
                status TEXT,
                record_raw TEXT,
                wins SMALLINT, 
                losses SMALLINT,
                draws SMALLINT,
                weight_class TEXT,
                age SMALLINT,
                height SMALLINT,
                reach SMALLINT,
                leg_reach SMALLINT,
                hometown TEXT,
                trains_at TEXT,
                fighting_style TEXT,
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
            cursor.execute("SELECT url FROM fighters WHERE url=%s", (item["url"],))
            existing_event = cursor.fetchone()

            if existing_event:
                # update the event
                update_query = """
                    UPDATE fighters 
                    SET 
                        name = %s,
                        nickname = %s,
                        status = %s,
                        record_raw = %s,
                        wins = %s,
                        losses = %s,
                        draws = %s,
                        weight_class = %s,
                        age = %s,
                        height = %s,
                        reach = %s,
                        leg_reach = %s,
                        hometown = %s,
                        trains_at = %s,
                        fighting_style = %s,
                        last_updated_at = CURRENT_TIMESTAMP 
                    WHERE url = %s
                """
                cursor.execute(
                    update_query,
                    (
                        item["name"],
                        item["nickname"],
                        item["status"],
                        item["record_raw"],
                        item["wins"],
                        item["losses"],
                        item["draws"],
                        item["weight_class"],
                        item["age"],
                        item["height"],
                        item["reach"],
                        item["leg_reach"],
                        item["hometown"],
                        item["trains_at"],
                        item["fighting_style"],
                        item["url"]
                    ),
                )
                conn.commit()

            else:
                insert_query = """
                    INSERT INTO fighters 
                    (
                        url,
                        name,
                        nickname,
                        status,
                        record_raw,
                        wins,
                        losses,
                        draws,
                        weight_class,
                        age,
                        height,
                        reach,
                        leg_reach,
                        hometown,
                        trains_at,
                        fighting_style,
                        last_updated_at
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP) 
                """
                cursor.execute(
                    insert_query,
                    (
                        item["url"],
                        item["name"],
                        item["nickname"],
                        item["status"],
                        item["record_raw"],
                        item["wins"],
                        item["losses"],
                        item["draws"],
                        item["weight_class"],
                        item["age"],
                        item["height"],
                        item["reach"],
                        item["leg_reach"],
                        item["hometown"],
                        item["trains_at"],
                        item["fighting_style"],
                    ),
                )
                conn.commit()

            conn.close()
            return item


class FightPipeline:
    def __init__(self):
        conn = psycopg2.connect(os.getenv("DB_URI"))
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS fights (
                id SERIAL PRIMARY KEY,
                event_id TEXT,
                r_fighter_id TEXT,
                b_fighter_id TEXT,
                r_fighter_status TEXT,
                b_fighter_status TEXT,
                round SMALLINT,
                time TEXT, 
                method TEXT,
                bout_weight TEXT,
                last_updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
                FOREIGN KEY (event_id) REFERENCES events (url),
                FOREIGN KEY (r_fighter_id) REFERENCES fighters (url),
                FOREIGN KEY (b_fighter_id) REFERENCES fighters (url)
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
            cursor.execute(
                "SELECT event_id FROM fights WHERE event_id=%s AND r_fighter_id=%s AND b_fighter_id=%s",
                (item["url"], item["r_fighter"], item["b_fighter"]),
            )
            existing_event = cursor.fetchone()

            if existing_event:
                update_query = """
                    UPDATE fights 
                    SET 
                        r_fighter_id = %s,
                        b_fighter_id = %s,
                        r_fighter_status = %s,
                        b_fighter_status = %s,
                        round = %s,
                        time = %s,
                        method = %s,
                        bout_weight = %s,
                        last_updated_at = CURRENT_TIMESTAMP 
                    WHERE event_id = %s
                """
                cursor.execute(
                    update_query,
                    (
                        item["r_fighter"],
                        item["b_fighter"],
                        item["r_fighter_status"],
                        item["b_fighter_status"],
                        item["round"],
                        item["time"],
                        item["method"],
                        item["bout_weight"],
                        item["url"],
                    ),
                )
                conn.commit()

            else:
                insert_query = """
                    INSERT INTO fights
                    (
                        event_id, 
                        r_fighter_id,
                        b_fighter_id,
                        r_fighter_status,
                        b_fighter_status,
                        round,
                        time,
                        method,
                        bout_weight,
                        last_updated_at
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP) 
                """
                cursor.execute(
                    insert_query,
                    (
                        item["url"],
                        item["r_fighter"],
                        item["b_fighter"],
                        item["r_fighter_status"],
                        item["b_fighter_status"],
                        item["round"],
                        item["time"],
                        item["method"],
                        item["bout_weight"], 
                    ),
                )
                conn.commit()

            conn.close()
            return item
