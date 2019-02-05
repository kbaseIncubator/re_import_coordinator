import plyvel
import json
import requests
import sys

# file that saves all pending workspaces
# move workspace id from pending file to success or error file
# save the error


def req_import(wsid):
    return requests.post(
        'https://kbase.us/dynserv/bbf73eeab74478490e0f8c8225f69664862da587.relation-engine-sync',  # noqa
        data=json.dumps({
            'method': 'import_range',
            'params': {
                'start': wsid,
                'stop': wsid + 1
            }
        })
    ).json()


if __name__ == '__main__':
    db_statuses = plyvel.DB('db/workspace_statuses', create_if_missing=False)
    db_errs = plyvel.DB('db/workspace_errors', create_if_missing=False)
    for key, status in db_statuses:
        if status == b'completed':
            print('skipping..')
            continue
        wsid = int.from_bytes(key, byteorder='big')
        resp = req_import(wsid)
        if resp.get('error'):
            db_statuses.put(key, b'error')
            db_errs.put(key, str(resp['error'])[0:512].encode())
        else:
            db_statuses.put(key, b'completed')
            db_errs.delete(key)
        sys.exit(1)  # TODO continue
