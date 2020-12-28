from datetime import datetime
from azure.eventgrid import EventGridClient
from msrest.authentication import TopicCredentials
import uuid
import bme280

def publish_event(self, temperature, humidity, pressure):
	credentials = TopicCredentials(self.settings.EVENT_GRID_KEY)
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
		"endpoint",
		events = payload
	)
