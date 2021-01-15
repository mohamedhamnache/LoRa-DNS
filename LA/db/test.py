from db.models.db_network import DbNetwork
import datetime

print(DbNetwork.return_all_Networks())
# n = DbNetwork("mohamed.fr", "192.168.1.1", "ABCDEFDEADABCD", datetime.datetime.now())
# n.save_to_db()
