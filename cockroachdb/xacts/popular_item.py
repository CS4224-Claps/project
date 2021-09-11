from collections import defaultdict
import logging

from utils.decorators import validate_command


@validate_command("I")
def execute(conn, io_line):
    # Retrieve Data from IO Line
    w_id, d_id, L = map(int, io_line[1:])

    with conn.cursor() as cur:
        get_next_avail_order_num = """
            SELECT D_NEXT_O_ID
            FROM District
            WHERE D_W_ID = (%s) AND D_ID = (%s)
        """
        cur.execute(get_next_avail_order_num, (w_id, d_id))
        N = cur.fetchone()[0]

        # Step (2) and output 3b)
        get_last_L_orders = """
            SELECT O_ID, O_ENTRY_D,
                concat_ws(' ', C_FIRST, C_MIDDLE, C_LAST) AS C_NAME
            FROM Orders
            INNER JOIN CUSTOMER ON O_C_ID = C_ID AND C_W_ID = (%(w_id)s) AND C_D_ID = (%(d_id)s)
            WHERE O_W_ID = (%(w_id)s) AND O_D_ID = (%(d_id)s) AND O_ID < (%(upper)s) AND O_ID >= (%(lower)s)
        """
        cur.execute(
            get_last_L_orders,
            {
                "w_id": w_id,
                "d_id": d_id,
                "lower": N - L,
                "upper": N,  # non inclusive
            },
        )
        last_L_orders = cur.fetchall()

        logging.debug(f"last_L_orders({w_id}, {d_id}, {N}, {N-L}): {last_L_orders}")

        # We also store I_ID because I_NAME might be the same.
        # (I_ID, I_NAME) -> appearance
        popular_items_appearance = defaultdict(int)
        # O_ID -> (I_NAME, OL_QUANITTY)
        popular_order_items = defaultdict(list)

        # (3) For each order, get popular items
        for o_id, *_ in last_L_orders:
            get_popular_items = """
                SELECT I_ID, I_NAME, OL_QUANTITY
                FROM Orderline
                INNER JOIN Item ON I_ID = OL_I_ID
                WHERE OL_W_ID = (%(w_id)s) AND OL_D_ID = (%(d_id)s) AND OL_O_ID = (%(o_id)s)
                    AND OL_QUANTITY = (
                        SELECT MAX(OL_QUANTITY)
                        FROM Orderline
                        WHERE OL_W_ID = (%(w_id)s) AND OL_D_ID = (%(d_id)s) AND OL_O_ID = (%(o_id)s)
                    )
            """
            cur.execute(
                get_popular_items,
                {
                    "w_id": w_id,
                    "d_id": d_id,
                    "o_id": o_id,
                },
            )
            results = cur.fetchall()
            logging.debug(f"get_popular_items({w_id}, {d_id}, {o_id}): {results}")

            items_seen = set()
            for item_id, item_name, ol_quantity in results:
                popular_order_items[o_id].append((item_name, ol_quantity))

                # make sure item_id is only added once per order,
                # as there might repeating items in different order lines
                if item_id not in items_seen:
                    items_seen.add(item_id)
                    popular_items_appearance[(item_id, item_name)] += 1

        logging.debug(f"popular_items_appearance: {popular_items_appearance}")
        logging.debug(f"popular_order_items: {popular_order_items}")

        # (4) Output the following information:
        print("1. District: ", w_id, d_id)
        print("2. Number of last orders: ", L)
        print("3. For each order: ")

        for o_id, o_entry_d, c_name in last_L_orders:
            print("Order: ", o_id, o_entry_d)
            print("Customer: ", c_name)
            print("Popular items: ", *popular_order_items[o_id])
            print()

        print(f"4. Percentage of popular items in last {L} orders: ")
        print(
            {
                item[1]: f"{str(appearance / L * 100)}%"
                for item, appearance in popular_items_appearance.items()
            }
        )

        logging.debug("payment: status message: %s", cur.statusmessage)

    conn.commit()
