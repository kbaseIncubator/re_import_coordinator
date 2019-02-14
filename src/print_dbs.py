import plyvel


db_statuses = plyvel.DB('db/workspace_statuses', create_if_missing=False)
db_errs = plyvel.DB('db/workspace_errors', create_if_missing=False)

if __name__ == '__main__':
    for key, val in db_statuses:
        print(int.from_bytes(key, byteorder='big'), val)
    for key, val in db_errs:
        print(int.from_bytes(key, byteorder='big'), val)
    db_statuses.close()
    db_errs.close()
