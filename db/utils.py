def dict_factory(cursor, row):
    return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}

def fetch_one_as_json(cursor):
    #cursor.execute(query, params)
    print("in fetch one")
    columns = [desc[0] for desc in cursor.description]
    results = cursor.fetchone()
    if(results==None):
        return {}
    json_list = []
    print(results)
    print('type:',type(results))
    #for row in results:
    json_item = {}
    for idx, col in enumerate(columns):
        json_item[col] = results[idx]
        json_list.append(json_item)

    return json_list[0]
def fetch_all_as_json(cursor):
    #cursor.execute(query, params)
    columns = [desc[0] for desc in cursor.description]
    results = cursor.fetchall()
    json_list = []

    for row in results:
        json_item = {}
        for idx, col in enumerate(columns):
            json_item[col] = row[idx]
        json_list.append(json_item)

    return json_list
def fetch_all_as_json1(cursor):
    rows = cursor.fetchall()
    print(cursor.description)
    for onerow in rows:
        print("onerow",onerow)
    #print(rows)
    #print(type(rows))

    return dict_factory(cursor,rows)
