import asyncio
import json
import random
from aiocoap import Context, Message, resource
from aiocoap.numbers.codes import Code

class SensorResource(resource.Resource):
    async def render_get(self, request):
        temperature = random.uniform(20.0, 25.0)
        humidity = random.uniform(30.0, 50.0)
        
        payload = json.dumps({
            "temperature": round(temperature, 2),
            "humidity": round(humidity, 2)
        }).encode('utf-8')
        
        return Message(code=Code.CONTENT, payload=payload)

async def main():
    root = resource.Site()
    root.add_resource(['sensor'], SensorResource())
    
    context = await Context.create_server_context(root, bind=('localhost', 5683))
    
    try:
        print("CoAP server started on port 5683")
        await asyncio.get_event_loop().create_future()
    except KeyboardInterrupt:
        print("Stopping CoAP server...")
    finally:
        await context.shutdown()

if __name__ == "__main__":
    asyncio.run(main())
