from datetime import datetime
from azure.eventgrid import EventGridClient
from msrest.authentication import TopicCredentials
import uuid
import bme280
import configparser

def publish_event(temperature, humidity, pressure):
	config = configparser.ConfigParser()
	config.read('config.ini')
	credentials = TopicCredentials(config['DEFAULT']['TopicCredentials'])
	endpoint = config['DEFAULT']['Endpoint']

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
			'event_time' : datetime.datetime.now(),
			'data_version' : 1
		}]
	
	client.publish_events(
		endpoint,
		events = payload
	)

def main():
	print("Starting")

if __name__ == "__main__":
	main()
