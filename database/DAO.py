from database.DB_connect import DBConnect
from model.order import Order


class DAO():

    @staticmethod
    def getAllStores():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = "SELECT store_id FROM stores"
        cursor.execute(query)
        for row in cursor:
            result.append(row["store_id"])
        cursor.close()
        conn.close()
        return result


    @staticmethod
    def getAllNodes(store):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """SELECT * FROM orders 
                    where store_id = %s"""
        cursor.execute(query, (store,))
        for row in cursor:
            result.append(Order(**row))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getArchi(store, k, idMap):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select distinct o1.order_id as o1 , o2.order_id as o2, (sum(oi1.quantity)+sum(oi2.quantity)) as p
                    from orders o1, orders o2, order_items oi1, order_items oi2
                    where o1.store_id = o2.store_id 
                    and o1.store_id = %s
                    and o1.order_date > o2.order_date 
                    and datediff(o1.order_date, o2.order_date) < %s 
                    and o1.order_id = oi1.order_id
                    and o2.order_id = oi2.order_id 
                    group by o1.order_id, o2.order_id """
        cursor.execute(query, (store, k))
        for row in cursor:
            result.append((idMap[row["o1"]], idMap[row["o2"]], row["p"]))
        cursor.close()
        conn.close()
        return result