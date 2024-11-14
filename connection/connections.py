from connection.MySqlConnection import MySqlConnection
from connection.RedisConnection import RedisConnection
from settings import DB_CONFIG, REDIS_CONN

db_connection = MySqlConnection(DB_CONFIG)

redis_connection = RedisConnection(REDIS_CONN)