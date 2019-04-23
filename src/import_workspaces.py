import time
import plyvel
import json
import requests
import sys
import os


def req_import(wsid):
    resp = requests.post(
        'https://kbase.us/dynserv/4b29b6d68535c391efd907813bf3d770c89ecfc9.relation-engine-sync',  # noqa
        # 'https://kbase.us/dynserv/bbf73eeab74478490e0f8c8225f69664862da587.relation-engine-sync',  # noqa
        data=json.dumps({
            'method': 'import_range',
            'params': {
                'start': wsid,
                'stop': wsid + 1
            }
        })
    )
    try:
        return resp.json()
    except Exception:
        return {'error': resp.text}


def handle_import(wsid, db_statuses, db_errs):
    key = wsid.to_bytes(4, byteorder='big')
    resp = req_import(wsid)
    if resp.get('error'):
        print(f'error on {wsid}')
        db_statuses.put(key, b'error')
        db_errs.put(key, str(resp['error'])[0:512].encode())
    else:
        print(f'completed {wsid}')
        db_statuses.put(key, b'completed')
        db_errs.delete(key)


if __name__ == '__main__':
    db_statuses = plyvel.DB('db/workspace_statuses', create_if_missing=False)
    db_errs = plyvel.DB('db/workspace_errors', create_if_missing=False)
    max_count = int(os.environ.get('MAX_COUNT', 0))
    retry_errors = os.environ.get('RETRY_ERRORS', False)
    count = 0
    if len(sys.argv) > 1:
        ws_ids = [int(wsid) for wsid in sys.argv[1:]]
        for wsid in ws_ids:
            handle_import(wsid, db_statuses, db_errs)
        sys.exit(0)
    for key, status in db_statuses:
        if max_count and count >= max_count:
            print(f'hit max count of {max_count} exiting')
            sys.exit(0)
        wsid = int.from_bytes(key, byteorder='big')
        if status == b'completed':
            print(f'skipping {wsid}')
            continue
        # Skip wsids that previously error'd if retry_errors is false
        if not retry_errors and status == b'error':
            print(f'error on {wsid}')
            continue
        handle_import(wsid, db_statuses, db_errs)
        count += 1
        time.sleep(3)
