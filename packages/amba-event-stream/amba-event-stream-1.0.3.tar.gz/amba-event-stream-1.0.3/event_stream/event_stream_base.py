import logging
import os
import time


class EventStreamBase(object):
    """
    a base class for connecting to kafka
    """

    id = time.time()
    event_string = "events"
    state_separator = "_"
    relation_type_separator = "-"

    bootstrap_servers = ['kafka:9092']
    group_id = 'worker'
    consumer_timeout_ms = 5000
    api_version = (0, 10)

    running = False

    config_states = {
        'unlinked': {
            'own_topic': ['discusses', 'crossref']
        },
        'linked': {
            'own_topic': ['discusses']
        },
        'unknown': {
        },
        'processed': {
            'own_topic': ['discusses']
        },
        'aggregated': {
        }}

    topics = []

    log = "EventStreamBase " + str(id) + " "

    def __init__(self, id_in, counter_in=None):
        self.id = id_in
        self.counter = counter_in
        self.log = self.log + str(self.id) + ": "
        self.bootstrap_servers = [os.environ.get('KAFKA_BOOTRSTRAP_SERVER', 'kafka:9092')]
        self.setup_logging()

    def build_topic_list(self):
        """build a list of topics from the configs
        """
        result = []

        for c_state in self.config_states:
            result.append(self.build_topic_name(c_state))
            if 'own_topic' in self.config_states[c_state]:
                for c_o_topic in self.config_states[c_state]['own_topic']:
                    result.append(self.build_topic_name(c_state, c_o_topic))

        self.topics = result
        logging.debug("%s current topics for events: %s" % (self.log, self.topics))
        return result

    def build_topic_name(self, state, relation_type=''):
        """build the name of the topic for a given state

        Arguments:
            state: the state to get the topic for
            relation_type: optional, in case it has it's own topic
        """
        result = self.event_string + self.state_separator + state

        if relation_type != '':
            result = result + self.relation_type_separator + relation_type
        return result

    def get_topic_name_event(self, event):
        """this will resolve an event to it's respected kafka topic

        Arguments:
            key: the event to be resolved
        """
        state = event.get('state')
        relation_type = event.get('relation_type')
        return self.get_topic_name(state, relation_type)

    def get_topic_name(self, state, relation_type=''):
        """get the name of the topic for a given state

        Arguments:
            state: the state to get the topic for
            relation_type: optional, in case it has it's own topic
        """
        result = self.event_string + self.state_separator + state

        # if a relation type is set and has is own topic
        if relation_type != '' and 'own_topic' in self.config_states[state] and relation_type in \
                self.config_states[state]['own_topic']:
            result = result + self.relation_type_separator + relation_type
        return result

    def resolve_event(self, event):
        """this will resolve an event to it's respected kafka topic

        Arguments:
            key: the event to be resolved
        """
        topic_name = self.build_topic_name(event['state'], event['relation_type'])
        if topic_name in self.topics:
            return topic_name

        logging.warning(self.log + "Unable to resolve event, topic_name %s not found" % topic_name)
        return False

    @staticmethod
    def setup_logging():
        """logging config to be used"""
        logging.basicConfig(format="%(asctime)s: %(message)s", level=logging.WARNING, datefmt="%H:%M:%S")

