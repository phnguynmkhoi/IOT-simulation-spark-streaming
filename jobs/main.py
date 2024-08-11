import os
from confluent_kafka import SerializingProducer
import simplejson as json
import datetime
import random
import uuid
import time


LONDON_COORDINATES = { "latitude": 51.5074, "longitude": -0.1278}
BIRMINGHAM_COORDINATES = { "latitude": 52.4862, "longitude": -1.8984}

#Example movement's increments
LATITUDE_INCREMENT = (BIRMINGHAM_COORDINATES['latitude'] - LONDON_COORDINATES['latitude'])/100
LONGITUDE_INCREMENT = (BIRMINGHAM_COORDINATES['longitude'] - LONDON_COORDINATES['longitude'])/100

#
KAFKA_BOOTSTRAP_SERVER = os.getenv('KAFKA_BOOTSTRAP_SERVER', 'localhost:9092')
VEHICLE_TOPIC = os.getenv('VEHICLE_TOPIC','vehicle_data')
GPS_TOPIC = os.getenv('GPS_TOPIC','gps_data')
TRAFFIC_TOPIC = os.getenv('TRAFFIC_TOPIC','traffic_data')
WEATHER_TOPIC = os.getenv('WEATHER_TOPIC','weather_data')
EMERGENCY_TOPIC = os.getenv('EMERGENCY_TOPIC','emergency_data')

curr_time = datetime.datetime.now()
curr_location = LONDON_COORDINATES.copy()

def get_next_time():
    global curr_time
    
    curr_time+= datetime.timedelta(seconds=random.randint(30,60))

    return curr_time

def simulate_vehicle_movement():
    global curr_location
    
    #moving the truck to Birmingham
    curr_location['latitude']+=LATITUDE_INCREMENT
    curr_location['longitude']+=LONGITUDE_INCREMENT

    #add some randomness
    curr_location['latitude']==random.uniform(-0.0005,0.0005)
    curr_location['longitude']==random.uniform(-0.0005,0.0005)
    
    return curr_location

def generate_vehicle_data(device_id):
    location = simulate_vehicle_movement()
    return {
        'id': uuid.uuid4(),
        'deviceId': device_id,
        'timestamp': curr_time.isoformat(),
        'location': (location['latitude'],location['longitude']),
        'speed': random.randint(10,40),
        'direction': 'North East',
        'make': 'BMW',
        'model': 'C500',
        'year': 2024,
        'fuelType': 'Hybrid'
    }

def generate_gps_data(device_id,timestamp,vehicle_type='private'):
    return {
        'id': uuid.uuid4(),
        'deviceId': device_id,
        'timestamp': timestamp,
        'speed': random.randint(0,40),
        'direction': 'North-East',
        'vehicleType': vehicle_type
    }

def generate_traffic_camera_data(device_id, timestamp, location ,camera_id):
    return {
        'id': uuid.uuid4(),
        'deviceId': device_id,
        'timestamp': timestamp,
        'cameraId': camera_id,
        'location': location,
        'snapshot': 'Base64EncodedString'
    }

def generate_weather_data(device_id, timestamp, location):
    return {
        'id': uuid.uuid4(),
        'deviceId': device_id,
        'timestamp': timestamp,
        'location': location,
        'temperature': random.uniform(-5,25),
        'weatherCondition': random.choice(['Sunny','Cloud','Rain','Snow']),
        'precipitation': random.uniform(0,25),
        'windSpeed': random.uniform(0,100),
        'humidity': random.randint(0,100),
        'airQualityIndex': random.uniform(0,500)
    }

def generate_emergency_data(device_id, timestamp, location):
    return {
        'id': uuid.uuid4(),
        'deviceId': device_id,
        'timestamp': timestamp,
        'incidentId': uuid.uuid4(),
        'type': random.choice(['Accident','Fire','Police','Medical','None']),
        'location': location,
        'status': random.choice(['Active','Resolved']),
        'description': 'Description of the incident'
    }

def json_serializer(obj):
    if isinstance(obj, uuid.UUID):
        return str(obj)
    raise TypeError(f'Object  of type {obj.__class__.__name__} is not serializable')

def delivery_report(err, msg):
    if err is not None:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}]')
        
    
def produce_data_to_kafka(producer, TOPIC, data):
    producer.produce(
        topic=TOPIC,
        key=str(data['id']),
        value=json.dumps(data, default=json_serializer).encode('utf-8'),
        on_delivery=delivery_report
    )    
    
    producer.flush()

def simulate_journey(producer, device_id):
    while True:
        print(1)
        vehicle_data = generate_vehicle_data(device_id)
        gps_data = generate_gps_data(device_id,vehicle_data['timestamp'])
        traffic_data = generate_traffic_camera_data(device_id,vehicle_data['timestamp'],vehicle_data['location'], camera_id= 'Camera1')
        weather_data = generate_weather_data(device_id,vehicle_data['timestamp'],vehicle_data['location'])
        emergency_data = generate_emergency_data(device_id,vehicle_data['timestamp'],vehicle_data['location'])
        
        if (vehicle_data['location'][0]>=BIRMINGHAM_COORDINATES['latitude'] and vehicle_data['location'][1]<=BIRMINGHAM_COORDINATES['longitude']):
            print('Vehicle has reached Birmingham. Simulation ending...')
            break
        
        produce_data_to_kafka(producer, VEHICLE_TOPIC, vehicle_data)
        produce_data_to_kafka(producer, GPS_TOPIC, gps_data)
        produce_data_to_kafka(producer, TRAFFIC_TOPIC, traffic_data)
        produce_data_to_kafka(producer, WEATHER_TOPIC, weather_data)
        produce_data_to_kafka(producer, EMERGENCY_TOPIC, emergency_data)

        # print(vehicle_data,gps_data,traffic_data,weather_data,emergency_data)
        
        time.sleep(3)

if __name__=='__main__':
    producer_config = {
        'bootstrap.servers': KAFKA_BOOTSTRAP_SERVER,
        'error_cb': lambda err: print(f'Kafka error: {err}')
    }
    producer = SerializingProducer(producer_config)
    
    try:
        simulate_journey(producer, 'vehicle')
        
    except KeyboardInterrupt:
        print('User stop simulation') 
    # except Exception as e:
    #     print(f'Unexpected error: {e}')