#takes values from kuksa databroker and publishes them to a zenoh router
import zenoh
from kuksa_client.grpc.aio import VSSClient
import asyncio
import time

async def main():
    with zenoh.open(zenoh.Config()) as session:
        async with VSSClient('127.0.0.1' , 55555) as client:
            while True:
                values = await client.get_current_values([
                    'Vehicle.OBD.Battery', 'Vehicle.OBD.Thermometer' ,
                    'Vehicle.OBD.Speedometer'
                ])

                battery = values['Vehicle.OBD.Battery'].value
                temperature = values['Vehicle.OBD.Thermometer'].value
                speed = values['Vehicle.OBD.Speedometer'].value

                battery_key = 'myvehicle/stats/battery_level'
                thermometer_key = 'myvehicle/stats/thermometer'
                speedometer_key = 'myvehicle/stats/speedometer'

                battery_pub = session.declare_publisher(battery_key)
                thermometer_pub = session.declare_publisher(thermometer_key)
                speed_pub = session.declare_publisher(speedometer_key)

                battery_pub.put(str(battery))
                thermometer_pub.put(str(temperature))
                speed_pub.put(str(speed))

                print('Battery = ', battery)
                print('Thermometer = ', temperature)
                print('Speedometer = ', speed)

                time.sleep(10)

asyncio.run(main())