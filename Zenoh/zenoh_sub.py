import zenoh
from dataclasses import dataclass
import time

@dataclass
class Stats():
    battery: int
    thermometer: float
    speedometer: float

def getStats():
    with zenoh.open(zenoh.Config()) as session:
        battery = 0
        thermometer = 0
        speedometer = 0

        replies = session.get('myvehicle/stats/*')
        for reply in replies:
            if reply.ok.key_expr == "myvehicle/stats/battery_level":
                battery = reply.ok.payload.to_string()
            elif reply.ok.key_expr == "myvehicle/stats/thermometer":
                thermometer = reply.ok.payload.to_string()
            elif reply.ok.key_expr == "myvehicle/stats/speedometer":
                speedometer = reply.ok.payload.to_string()
                
        vehicle = Stats(battery, thermometer, speedometer)
        return vehicle

if __name__ == "__main__":
    while True:
        vehicle = getStats()
        print(f"battery: {vehicle.battery}, temperature: {vehicle.thermometer}, speed: {vehicle.speedometer}")
        time.sleep(10)