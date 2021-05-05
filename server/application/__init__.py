connect = None
DictCursor = None
MAX_BOOKING_RANGE = 7
MAX_NUM_DISEASES = 5

def default(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()
def my_jsonify(rows, multiple=True):
    if multiple:
        ret = []
        for row in rows:
            cur = {}
            for k in row.keys():
                cur[k] = row[k]
            ret.append(cur)
        return ret
    else:
        cur = {}
        for k in rows.keys():
            cur[k] = rows[k]
        return cur