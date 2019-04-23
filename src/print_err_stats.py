import plyvel


if __name__ == '__main__':
    db_statuses = plyvel.DB('db/workspace_statuses', create_if_missing=False)
    db_errs = plyvel.DB('db/workspace_errors', create_if_missing=False)
    err_count = 0
    success_count = 0
    error_counts = {}  # type: dict
    for key, val in db_statuses:
        if val == b'error':
            err_count += 1
            err = db_errs.get(key)
            if err not in error_counts:
                error_counts[err] = 1
            else:
                error_counts[err] += 1
        elif val == b'completed':
            success_count += 1
    print('Total error count:', err_count)
    print('Success count:', success_count)
    print('Error count by message:', error_counts)
    db_statuses.close()
    db_errs.close()
