import asyncio
from hbmqtt.broker import Broker

config = {
    'listeners': {
        'default': {
            'type': 'tcp',
            'bind': '127.0.0.1:1883'
        }
    },
    'sys_interval': 10,
    'auth': {
        'allow-anonymous': True,
        'plugins': ['auth_anonymous']
    }
}

broker = Broker(config)

asyncio.get_event_loop().run_until_complete(broker.start())
asyncio.get_event_loop().run_forever()
