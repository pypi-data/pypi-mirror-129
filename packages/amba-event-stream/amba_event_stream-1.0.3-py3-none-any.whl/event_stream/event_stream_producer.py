import logging
from kafka import KafkaProducer
from .event_stream_base import EventStreamBase


class EventStreamProducer(EventStreamBase):
    """produce messages for kafka

    """
    producer = False
    log = "EventStreamProducer"

    def publish(self, event):
        """publish an event

        Arguments:
            event: the event which should be shared
        """
        topic_event = self.get_topic_name_event(event)

        if not self.producer:
            self.create_producer()

        value = event.get_json()
        self.producer.send(topic_event, value=value.encode('utf-8'))
        self.producer.flush()
        logging.debug(self.log + 'Message published successfully to topic %s' % topic_event)

    def create_producer(self):
        """create the producer
        """
        self.producer = KafkaProducer(bootstrap_servers=self.bootstrap_servers, api_version=self.api_version)
