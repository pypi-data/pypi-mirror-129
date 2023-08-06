# NEON AI (TM) SOFTWARE, Software Development Kit & Application Framework
# All trademark and other rights reserved by their respective owners
# Copyright 2008-2022 Neongecko.com Inc.
# Contributors: Daniel McKnight, Guy Daniels, Elon Gasper, Richard Leeds,
# Regina Bloomstine, Casimiro Ferreira, Andrii Pernatii, Kirill Hrymailo
# BSD-3 License
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from this
#    software without specific prior written permission.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
# CONTRIBUTORS  BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
# OR PROFITS;  OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE,  EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import time
import uuid
import pika
import pika.exceptions
import threading

from abc import ABC, abstractmethod
from typing import Optional
from neon_utils import LOG
from neon_utils.socket_utils import dict_to_b64

from .config import load_neon_mq_config
from .utils import RepeatingTimer, retry, wait_for_mq_startup


class ConsumerThread(threading.Thread):
    """Rabbit MQ Consumer class that aims at providing unified configurable interface for consumer threads"""
    @retry(use_self=True)  # Handle connection failures in case MQ server is still starting up
    def __init__(self, connection_params: pika.ConnectionParameters, queue: str, callback_func: callable,
                 error_func: callable, auto_ack: bool = True, *args, **kwargs):
        """
            :param connection_params: pika connection parameters
            :param queue: Desired consuming queue
            :param callback_func: logic on message receiving
            :param error_func: handler for consumer thread errors
            :param auto_ack: Boolean to enable ack of messages upon receipt
        """
        threading.Thread.__init__(self, *args, **kwargs)
        self.connection = pika.BlockingConnection(connection_params)
        self.callback_func = callback_func
        self.error_func = error_func
        self.queue = queue
        self.channel = self.connection.channel()
        self.channel.basic_qos(prefetch_count=50)
        self.channel.queue_declare(queue=self.queue, auto_delete=False)
        self.channel.basic_consume(on_message_callback=self.callback_func,
                                   queue=self.queue,
                                   auto_ack=auto_ack)

    def run(self):
        """Creating consumer channel"""
        super(ConsumerThread, self).run()
        try:
            self.channel.start_consuming()
        except pika.exceptions.ChannelClosed:
            LOG.debug(f"Channel closed by broker: {self.callback_func}")
        except Exception as e:
            LOG.error(e)
            self.error_func(self, e)

    def join(self, timeout: Optional[float] = ...) -> None:
        """Terminating consumer channel"""
        try:
            self.channel.stop_consuming()
            if self.channel.is_open:
                self.channel.close()
            if self.connection.is_open:
                self.connection.close()
        except Exception as x:
            LOG.error(x)
        finally:
            super(ConsumerThread, self).join()


class MQConnector(ABC):
    """Abstract method for attaching services to MQ cluster"""

    @abstractmethod
    def __init__(self, config: Optional[dict], service_name: str):
        """
            :param config: dictionary with current configurations.
            ``` JSON Template of configuration:

                     { "users": {"<service_name>": { "username": "<username>",
                                                     "password": "<password>" },
                       "server": "localhost",
                       "port": 5672
                     }
            ```
            :param service_name: name of current service
       """
        self.config = config or load_neon_mq_config()
        if self.config.get("MQ"):
            self.config = self.config["MQ"]
        self._service_id = self.create_unique_id()
        self.service_name = service_name
        self.consumers = dict()
        self.sync_period = 10  # in seconds
        self.vhost = '/'
        self._sync_thread = None

    @property
    def service_id(self):
        """ID of the service should be considered to be unique"""
        return self._service_id

    @property
    def mq_credentials(self):
        """Returns MQ Credentials object based on username and password in configuration"""
        if not self.config:
            raise Exception('Configuration is not set')
        return pika.PlainCredentials(self.config['users'][self.service_name].get('user', 'guest'),
                                     self.config['users'][self.service_name].get('password', 'guest'))

    def get_connection_params(self, vhost, **kwargs) -> pika.ConnectionParameters:
        """
        Gets connection parameters to be used to create an mq connection
        """
        connection_params = pika.ConnectionParameters(host=self.config.get('server', 'localhost'),
                                                      port=int(self.config.get('port', '5672')),
                                                      virtual_host=vhost,
                                                      credentials=self.mq_credentials,
                                                      **kwargs)
        return connection_params

    @staticmethod
    def create_unique_id():
        """Method for generating unique id"""
        return uuid.uuid4().hex

    @classmethod
    def emit_mq_message(cls, connection: pika.BlockingConnection, queue: str, request_data: dict,
                        exchange: Optional[str], expiration: int = 1000) -> str:
        """
            Emits request to the neon api service on the MQ bus

            :param connection: pika connection object
            :param queue: name of the queue to publish in
            :param request_data: dictionary with the request data
            :param exchange: name of the exchange (optional)
            :param expiration: mq message expiration time (in millis, defaults to 1 second)

            :raises ValueError: invalid request data provided
            :returns message_id: id of the sent message
        """
        if request_data and len(request_data) > 0 and isinstance(request_data, dict):
            message_id = cls.create_unique_id()
            request_data['message_id'] = message_id
            channel = connection.channel()
            channel.basic_publish(exchange=exchange or '',
                                  routing_key=queue,
                                  body=dict_to_b64(request_data),
                                  properties=pika.BasicProperties(expiration=str(expiration)))
            channel.close()
            return message_id
        else:
            raise ValueError(f'Invalid request data provided: {request_data}')

    def create_mq_connection(self, vhost: str = '/', **kwargs):
        """
            Creates MQ Connection on the specified virtual host
            Note: In order to customize behavior, additional parameters can be defined via kwargs.

            :param vhost: address for desired virtual host
            :raises Exception if self.config is not set
        """
        if not self.config:
            raise Exception('Configuration is not set')
        return pika.BlockingConnection(parameters=self.get_connection_params(vhost, **kwargs))

    def register_consumer(self, name: str, vhost: str, queue: str,
                          callback: callable, on_error: Optional[callable] = None,
                          auto_ack: bool = True):
        """
        Registers a consumer for the specified queue. The callback function will handle items in the queue.
        Any raised exceptions will be passed as arguments to on_error.
        :param name: Human readable name of the consumer
        :param vhost: vhost to register on
        :param queue: MQ Queue to read messages from
        :param callback: Method to passed queued messages to
        :param on_error: Optional method to handle any exceptions raised in message handling
        :param auto_ack: Boolean to enable ack of messages upon receipt
        """
        error_handler = on_error or self.default_error_handler
        self.consumers[name] = ConsumerThread(self.get_connection_params(vhost), queue=queue, callback_func=callback,
                                              error_func=error_handler, auto_ack=auto_ack, name=name)

    @staticmethod
    def default_error_handler(thread: ConsumerThread, exception: Exception):
        LOG.error(f"{exception} occurred in {thread}")

    def run_consumers(self, names: tuple = (), daemon=True):
        """
            Runs consumer threads based on the name if present (starts all of the declared consumers by default)

            :param names: names of consumers to consider
            :param daemon: to kill consumer threads once main thread is over
        """
        if not names or len(names) == 0:
            names = list(self.consumers)
        for name in names:
            if name in list(self.consumers) and not self.consumers[name].is_alive():
                self.consumers[name].daemon = daemon
                self.consumers[name].start()

    def stop_consumers(self, names: tuple = ()):
        """
            Stops consumer threads based on the name if present (stops all of the declared consumers by default)
        """
        if not names or len(names) == 0:
            names = list(self.consumers)
        for name in names:
            try:
                if name in list(self.consumers):
                    self.consumers[name].join()
            except Exception as e:
                raise ChildProcessError(e)

    def sync(self, vhost: str = None, exchange: str = None, queue: str = None, request_data: dict = None):
        """
            Periodical notification message to be sent into MQ,
            used to notify other network listeners about this service health status

            :param vhost: mq virtual host (defaults to self.vhost)
            :param exchange: mq exchange (defaults to base one)
            :param queue: message queue prefix (defaults to self.service_name)
            :param request_data: data to publish in sync
        """
        vhost = vhost or self.vhost
        queue = f'{queue or self.service_name}_sync'
        exchange = exchange or ''
        request_data = request_data or {'service_id': self.service_id, 'time': int(time.time())}

        with self.create_mq_connection(vhost=vhost) as mq_connection:
            LOG.info(f'Emitting sync message to (vhost="{vhost}", exchange="{exchange}", queue="{queue}")')
            self.emit_mq_message(mq_connection, queue=queue, exchange=exchange, request_data=request_data)

    def run(self, run_consumers: bool = True, run_sync: bool = True, **kwargs):
        """
            Generic method called on running the instance

            :param run_consumers: to run this instance consumers (defaults to True)
            :param run_sync: to run synchronization thread (defaults to True)
        """
        try:
            host = self.config.get('server', 'localhost')
            port = int(self.config.get('port', '5672'))
            wait_for_mq_startup(host, port)
            kwargs.setdefault('consumer_names', ())
            kwargs.setdefault('daemonize_consumers', False)
            self.pre_run(**kwargs)
            if run_consumers:
                self.run_consumers(names=kwargs['consumer_names'],
                                   daemon=kwargs['daemonize_consumers'])
            if run_sync:
                self.sync_thread.start()
            self.post_run(**kwargs)
        except Exception as ex:
            self.stop()
            LOG.error(f'Connection received interrupt due to exception {ex}')

    @property
    def sync_thread(self):
        """Creates new Repeating Timer if none is present"""
        if not self._sync_thread:
            self._sync_thread = RepeatingTimer(self.sync_period, self.sync)
        return self._sync_thread

    def stop_sync_thread(self):
        """Stops Repeating Timer and dereferences it"""
        if self._sync_thread:
            self._sync_thread.cancel()
            self._sync_thread = None

    def stop(self):
        """Generic method for graceful instance stopping"""
        self.stop_consumers()
        self.stop_sync_thread()

    def pre_run(self, **kwargs):
        """Additional logic invoked before method run()"""
        pass

    def post_run(self, **kwargs):
        """Additional logic invoked after method run()"""
        pass
