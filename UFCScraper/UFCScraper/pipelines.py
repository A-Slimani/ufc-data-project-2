from dotenv import load_dotenv
from UFCScraper.items import EventItem, FighterItem
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
                id SERIAL PRIMARY KEY,
                name TEXT,
                location_raw TEXT,
                date_raw TEXT,
                url TEXT NOT NULL
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
                    SET name = %s, location_raw = %s, date_raw = %s
                    WHERE url = %s
                """
                cursor.execute(
                    update_query,
                    (item["name"], item["location_raw"], item["date_raw"], item["url"]),
                )
                conn.commit()

            else:
                insert_query = """
                    INSERT INTO events (
                        name, location_raw, date_raw, url 
                    ) VALUES (%s, %s, %s, %s)
                """
                cursor.execute(
                    insert_query,
                    (item["name"], item["location_raw"], item["date_raw"], item["url"]),
                )
                conn.commit()

            conn.close()
            return item
        else:
            print(f"Invalid item :: {type(item)}")


class FighterPipeline:
    def __init__(self):
        conn = psycopg2.connect(os.getenv("DB_URI"))
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS fighters (
                id SERIAL PRIMARY KEY,
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
                url TEXT,
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
                ),
            )
            conn.commit()

        else:
            insert_query = """
                INSERT INTO fighters 
                (
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
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP) 
            """
            cursor.execute(
                insert_query,
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
                ),
            )
            conn.commit()

        conn.close()
        return item
