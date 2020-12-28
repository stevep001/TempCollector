from datetime import datetime
from azure.eventgrid import EventGridClient
from msrest.authentication import TopicCredentials
import uuid
import bme280
import configparser

def publish_event(humidity, pressure, temperature):
	config = configparser.ConfigParser()
	config.read('config.ini')
	credentials = TopicCredentials(config['DEFAULT']['TopicCredentials'])
	endpoint = config['DEFAULT']['Endpoint']
	print "Endpoint: ", endpoint

	client = EventGridClient(credentials)
	payload = [{
			'id' : str(uuid.uuid4()),
			'subject' : "/environmentSensor/1",
			'data': {
				'temperature' : temperature,
				'humidity' : humidity,
				'pressure' : pressure
			},
			'event_type' : 'Sample',
			'event_time' : datetime.now(),
			'data_version' : 1
		}]
	
	client.publish_events(
		endpoint,
		events = payload
	)

def main():
	print("Starting")
	temperature, pressure, humidity = bme280.readBME280All()
	print "Temperature: ", temperature
	print "Humidity: ", humidity
	print "Pressure: ", pressure
	publish_event(humidity, pressure, temperature)
	print("All done.")

if __name__ == "__main__":
	main()
