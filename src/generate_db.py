import plyvel


db_status = plyvel.DB('db/workspace_statuses', create_if_missing=True)
db_errs = plyvel.DB('db/workspace_errors', create_if_missing=True)

if __name__ == '__main__':
    for wsid in range(1, 50000):
        db_status.put(wsid.to_bytes(4, byteorder='big'), b'pending')
    db_status.close()
    db_errs.close()
