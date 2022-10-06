from pymongo import MongoClient
from loguru import logger
import yaml
from yaml.loader import SafeLoader


class database:
    # Класс, объединяющий в себе весь функционал работы с БД Mongo необходимый для работы сервиса Freedom_Gate.
    def __init__(self):
        with open('conn.yml') as f:
            data = yaml.load(f, Loader=SafeLoader)
            db_params = data['db_conn'][0]
        self.url = db_params['url']
        self.db = db_params['db']
        self.user = db_params['user']
        self.passwd = db_params['passwd']
        self.first_doc = db_params['fd']
        self.collections = db_params['collections']

    def connection_to_mongo(self):
        # Функция создает подключение к БД Mongo.
        connection_string = 'mongodb://' + self.user + ':' + self.passwd + '@' + self.url + '/' + \
                            '?authSource=admin&retryWrites=true&w=majority'
        client = MongoClient(connection_string)
        return client

    def db_init(self):
        # Функция инициализирует БД в случае необходимости и создает коллекции.
        from pymongo.errors import DuplicateKeyError
        freedom_db = self.connection_to_mongo()[self.db]
        for collection in self.collections:
            collection_init = freedom_db[collection]
            try:
                collection_init.insert_one(self.first_doc)
                logger.debug(f'Attention: Collection {collection} was inserted in freedom_gate database')
            except DuplicateKeyError:
                logger.error(f'It seems that such a collection {collection} already exists.')

    def mongo_export(self, export_dict: dict, proxy_type: str):
        # Функция принимает словарь с данными из парсера и строковое значение типа прокси.
        # Проверяет в БД наличие таких же записей, если запись есть - проверяет статус прокси
        # (если в нём были изменения - обновляет), если записи нет - добавляет запись.
        from pymongo.errors import DuplicateKeyError
        freedom_db = self.connection_to_mongo()[self.db]
        try:
            freedom_db[proxy_type].insert_one(export_dict)
        except DuplicateKeyError:
            logger.info(f'It seems that such a document already exists: {export_dict["_id"]}')
            status_proxy = freedom_db[proxy_type].find_one({'_id': export_dict['_id']})['status']
            if export_dict['status'] == status_proxy:
                logger.info(f'The document {export_dict["_id"]} does not need to be updated')
            else:
                freedom_db[proxy_type].replace_one({'_id': export_dict['_id']}, export_dict, upsert=False)
                logger.info('Document update')
