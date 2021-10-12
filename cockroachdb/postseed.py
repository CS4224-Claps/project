import psycopg2
import time
from utils.cli import parse_cmdline


def add_c_id_to_orderline(opt):
    """
    Modified from: https://www.cockroachlabs.com/docs/v21.1/bulk-update-data.html
    """
    conn = psycopg2.connect(dsn=opt.dsn)

    with conn.cursor() as cur:
        cur.execute("ALTER TABLE orderline ADD COLUMN IF NOT EXISTS ol_c_id INTEGER;")

    for w_id in range(1, 11):
        for d_id in range(1, 11):
            print(f"Processing {w_id}, {d_id}...")

            while True:
                lastid = None
                with conn:
                    with conn.cursor() as cur:
                        cur.execute("SET TRANSACTION AS OF SYSTEM TIME '-5s'")
                        if lastid:
                            cur.execute(
                                "SELECT ol_o_id FROM orderline WHERE ol_w_id=(%s) AND ol_d_id=(%s) AND ol_o_id > %s AND ol_c_id IS NULL ORDER BY id LIMIT 50000",
                                (w_id, d_id, lastid),
                            )
                        else:
                            cur.execute(
                                "SELECT ol_o_id FROM orderline WHERE ol_w_id=(%s) AND ol_d_id=(%s) AND ol_c_id IS NULL ORDER BY ol_o_id LIMIT 50000",
                                (w_id, d_id),
                            )
                        pkvals = list(cur)
                if not pkvals:
                    break
                while pkvals:
                    batch = pkvals[:5000]
                    pkvals = pkvals[5000:]
                    with conn:
                        with conn.cursor() as cur:
                            cur.execute(
                                """
                                UPDATE orderline ol
                                SET ol_c_id = (
                                    SELECT o_c_id
                                    FROM orders o
                                    WHERE o.o_w_id=ol.ol_w_id AND o.o_d_id=ol.ol_d_id AND o.o_id=ol.ol_o_id
                                )
                                WHERE ol_w_id=(%s) AND ol_d_id=(%s) AND ol_o_id=ANY (%s) RETURNING ol_o_id
                                """,
                                (w_id, d_id, batch),
                            )
                            # print(cur.statusmessage)
                            if not pkvals:
                                lastid = cur.fetchone()[0]
                del batch
                del pkvals

                time.sleep(5)

    conn.close()
    print("DONE")


if __name__ == "__main__":
    opt = parse_cmdline()
    add_c_id_to_orderline(opt)
