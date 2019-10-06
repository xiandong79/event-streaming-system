import logging
import traceback
import redis
import mysql.connector
from decimal import Decimal


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="MyNewPass",
    database="credit_card_transactions",
    # auth_plugin='mysql_native_password'
)
mycursor = mydb.cursor()


def sub_and_store():
    # Set-up a pub/sub system to capture those events
    try:
        # Connect to local Redis instance
        r = redis.StrictRedis(host='localhost', port=6379)

        # See https://github.com/andymccurdy/redis-py/#publish--subscribe
        p = r.pubsub()
        # Subscribe to startScripts channel
        p.subscribe('credit_card_transactions')
        RUNNING = True

        while RUNNING:
            # Will stay in loop until START message received
            logging.info("Sub is starting...")

            # Checks for message
            message = p.get_message()
            if message:
                # Get data from message
                msg = message['data']
                # print(msg)

                if type(msg) == bytes:
                    sql = "INSERT INTO transactions (user_id, transaction_amount, transaction_time) VALUES (%s, %s, %s)"
                    msg = msg.decode("utf-8").split(',')
                    mycursor.execute(sql, (msg[0], msg[1], Decimal(msg[2])))
                    print('user_id: {}, transaction_amount: {}, transaction_time: {}'.format(msg[0], msg[1], Decimal(msg[2])))

                    mydb.commit()
                    logging.info(mycursor.rowcount, "transaction record inserted")

    except Exception as e:
        logging.critical(f"!!!!!! EXCEPTION !!!! {str(e)}")
        print(traceback.format_exc())


if __name__ == '__main__':
    sub_and_store()
