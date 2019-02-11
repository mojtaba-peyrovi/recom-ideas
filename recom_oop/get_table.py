import db_connection.ihub as ihub
import db_connection.alice as alice
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

def get_table():
    import pandas as pd
    conn = ihub.iHub_engine('expedia').connection
    conn2 = alice.alice_engine('hqlive').connection
    try:
        with conn2.cursor() as cursor:
            query = """
                select
                hotel_id as Hotel_ID,
                d10_hotel_city_name as city,
                d15_hotel_name as hotel_name,
                hqlive.hotel.hotel_catg_id as stars,
                d25_hotel_location_latitude as lat,
                d26_hotel_location_longitude as lon,
                count(distinct order_id) as bookings,
                sum(datediff(m139_offer_checkout_date, m138_offer_checkin_date)) * room_cnt as RNS,
                round(sum(c1_selling_price),0) as GBV,
                round(sum(c1_selling_price),0) / sum(datediff(m139_offer_checkout_date, m138_offer_checkin_date)) as GBV_RNS
                from bi_export.order
                left join hqlive.hotel
                on 1=1
                and bi_export.order.hotel_id = hqlive.hotel.id
                where order.hotel_id <> -1
                and datediff('2018-12-01', date(m01_order_datetime_gmt0)) < 30
                and hotel_status_id = 1
                and d22_inventory_source_code = 'HQ01'
                group by 1,2,3,4
                order by GBV desc
            """
            cursor.execute(query)
            conn.commit()
            df = pd.read_sql(query, conn2)
    finally:
        conn2.close()
    return df
