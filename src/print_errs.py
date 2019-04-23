import plyvel


if __name__ == '__main__':
    db_statuses = plyvel.DB('db/workspace_statuses', create_if_missing=False)
    db_errs = plyvel.DB('db/workspace_errors', create_if_missing=False)
    for key, val in db_statuses:
        if val == b'error':
            print('Error on', int.from_bytes(key, byteorder='big'))
            err = db_errs.get(key)
            print('Message:', err.decode())
    db_statuses.close()
    db_errs.close()
