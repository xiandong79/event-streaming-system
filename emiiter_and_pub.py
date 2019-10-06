import logging
import traceback
import redis
import random
import time

logging.basicConfig(
    filename='transactions.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p')


def emitter_and_pub(num_users=3):
    # Build a fake emitter of credit card transactions with random time intervals
    # Connect to local Redis instance
    r = redis.StrictRedis(host='localhost', port=6379)
    logging.info("Starting emitter_and_pub scripts...")

    while True:
        try:
            # Generate random integers between 0 and 'num_users'
            user_id = random.randrange(num_users)
            transaction_amount = random.randint(-1 * 10e10, 1 * 10e10)
            transaction_time = time.time()
            msg = ','.join(
                [str(user_id), str(transaction_amount), str(transaction_time)])

            # PUBLISH message on 'cedit_card_transactions' channel
            r.publish('credit_card_transactions', msg)
            logging.info(f'pub_transactions: {msg}')

            time.sleep(random.randint(0, 5))
        except Exception as e:
            logging.critical(f"emitter_and_pub is down: {str(e)}")
            print(traceback.format_exc())


if __name__ == '__main__':
    emitter_and_pub(num_users=5)
