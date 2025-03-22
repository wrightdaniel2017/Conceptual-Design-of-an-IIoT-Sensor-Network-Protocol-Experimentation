from asyncua import ua, Server
import asyncio
import random

async def main():
    server = Server()
    await server.init()
    server.set_endpoint("opc.tcp://0.0.0.0:4840/freeopcua/server/")
    
    uri = "http://examples.freeopcua.github.io"
    idx = await server.register_namespace(uri)
    
    # get_objects_node() is a synchronous method; remove the await
    objects = server.get_objects_node()
    
    myobj = await objects.add_object(idx, "MyObject")
    temperature = await myobj.add_variable(idx, "Temperature", 0.0)
    humidity = await myobj.add_variable(idx, "Humidity", 0.0)
    
    await temperature.set_writable(True)
    await humidity.set_writable(True)
    
    async with server:
        print("OPC UA server started on port 4840")
        while True:
            try:
                temp_value = random.uniform(20.0, 25.0)
                hum_value = random.uniform(30.0, 50.0)
                
                await temperature.write_value(temp_value)
                await humidity.write_value(hum_value)
                
                print(f"Updated - Temperature: {temp_value:.2f}°C, Humidity: {hum_value:.2f}%")
                await asyncio.sleep(1)
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
