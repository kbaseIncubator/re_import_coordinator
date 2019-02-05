import plyvel
import json
import requests
import sys
import os


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
    max_count = int(os.environ.get('MAX_COUNT', 0))
    count = 0
    for key, status in db_statuses:
        if max_count and count >= max_count:
            print(f'hit max count of {max_count} exiting')
            sys.exit(0)
        if status == b'completed':
            print('skipping..')
            continue
        wsid = int.from_bytes(key, byteorder='big')
        resp = req_import(wsid)
        if resp.get('error'):
            print(f'error on {wsid}')
            db_statuses.put(key, b'error')
            db_errs.put(key, str(resp['error'])[0:512].encode())
        else:
            print(f'completed {wsid}')
            db_statuses.put(key, b'completed')
            db_errs.delete(key)
        count += 1
