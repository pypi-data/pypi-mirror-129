#Библиотека для получения экземпляров сервисов
Библиотека нужна для получения доступа к сервисам без указания путей к сервисам и секретов 
(для работы нужно только знать url и token vault). Далее секреты автоматически достаются из vault, пути из consul
## Установка
from dvg_service_factory import factory

##Порядок работы:
1. Получить объект фабрики: fc = factory.Factory(vault_url=url, vault_token=token)
2. Получить объект сервиса (в kwargs передаются параметры не связанные с url и secrets):
   1. ch_client = fc.clickhouse_client(secure=True, database="db1", verify=False)
   2. kafka_p = fc.kafka_producer(value_serializer=lambda v: json.dumps(v).encode('utf-8'))
   3. По умолчанию, если ранее уже был создан объект сервиса, то при следующем запросе, будет возвращен ранее созданный.
   4. Для получения нового объекта (если ранее уже был получен экземпляр), требуется переддать параметр new=True: 
      1. kafka_p2 = fc.kafka_producer(value_serializer=lambda v: json.dumps(v).encode('utf-8'), ***new=True***)
   5. Для понимания, какие методы (классы сервисов) реализованы, следует вызвать метод info(), который возвратит след.информацию:
---------------------------------------------------------------------------------   
   Создание экземпляра:\
       ins = Factory(vault_url=url, vault_token=token)\
   Методы: \
      1 ins.vault_client(url: str, token: str)\
      2 ins.consul(**kwargs)\
      3 ins.kafka_producer(**kwargs)\
      4 ins.kafka_consumer(**kwargs)\
      5 ins.clickhouse_client(**kwargs)\
      6 ins.azure_container_client(**kwargs)\
      7 ins.loki_handler(**kwargs)\
   Для создания нового экземпляра укажите в kwargs: new=True\
   Пути настроек в consul:\
      {"clickhouse": "env/databases/clickhouse", "kafka": "env/databases/kafka", "ms-azure-se": "env/databases/ms-azure-se", "loki": "env/databases/loki"}
----------------------------------------------------------------------------------





