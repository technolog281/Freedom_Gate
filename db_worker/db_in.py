from pymongo import MongoClient
from loguru import logger


def mongo_export(export_dict: dict):
    client = MongoClient('localhost', 27017)
    db = client['freedom_gate']
    collection = db['http']
    collection.insert_one(export_dict)
    client.close()


def mongo_update(export_dict: dict):
    client = MongoClient('localhost', 27017)
    db = client['freedom_gate']
    collection = db['http']
    collection.replace_one(export_dict,
                           {'_id': export_dict['_id'],
                            'ip': export_dict['ip'],
                            'port': export_dict['port'],
                            'location': export_dict['location'],
                            'timing': export_dict['timing'],
                            'proxy_type': export_dict['proxy_type'],
                            'last_check': export_dict['last_check']
                            })
    client.close()


def hidemy_export():
    from proxy_finder.hidemy_name_parser import parse_all as hidemy
    list_of_proxy = hidemy()
    for string in list_of_proxy:
        for item in string:
            item_to_mongo = {
                '_id': item,
                'ip': item,
                'port': string[item][0],
                'location': string[item][1],
                'timing': string[item][2],
                'proxy_type': string[item][3],
                'last_check': string[item][5]
            }
            from pymongo.errors import DuplicateKeyError
            try:
                mongo_export(item_to_mongo)
                logger.info('Try to push dictionary to MongoDB, wait...')
            except DuplicateKeyError:
                mongo_update(item_to_mongo)
                logger.info('It seems that dictionary in MongoDB yet, update document, wait...')


hidemy_export()




