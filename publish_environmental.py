from datetime import datetime
from azure.eventgrid import EventGridPublisherClient, EventGridEvent, CloudEvent
from azure.core.credentials import AzureKeyCredential
import uuid
import bme280
import configparser
import os

def publish_event(humidity, pressure, temperature):
	configPath = os.path.split(os.path.abspath(__file__))[0] + "/config.ini"
	config = configparser.ConfigParser()
	config.read(configPath)
	credentialString = config['DEFAULT']['TopicCredentials']
	topicHostname = config['DEFAULT']['TopicHostname']

	credentials = AzureKeyCredential(credentialString)
	client = EventGridPublisherClient(topicHostname, credentials)

	payload = EventGridEvent(
		id = str(uuid.uuid4()),
		subject = "/environmentSensor/1",
		data = {
			'temperature' : temperature,
			'humidity' : humidity,
			'pressure' : pressure
		},
		event_type = 'Sample',
		event_time = datetime.now(),
		data_version = 1
	)
	client.send(payload)

def main():
	temperature, pressure, humidity = bme280.readBME280All()
	print "Temperature: ", temperature
	print "Humidity: ", humidity
	print "Pressure: ", pressure
	publish_event(humidity, pressure, temperature)

if __name__ == "__main__":
	main()
