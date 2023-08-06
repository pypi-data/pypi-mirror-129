from multiprocessing import Process
from typing import Tuple, Union

from breath_api_interface import ProcessQueue, ServiceProxy
from breath_api_interface.service_interface import Service

from breath_data import BDAcessPoint, DataWorflow
from breath_main.console_application import ConsoleApplication

import multiprocessing

SERVICES = {"BDAcessPoint": BDAcessPoint, "DataWorkflow" : DataWorflow, "ConsoleApplication": ConsoleApplication}

def create_and_run_service(service_class, proxy, request_queue, global_response_queue):
    service : Service = service_class(proxy, request_queue, global_response_queue)
    service.run_forever()

class ProcessServiceConstructor:
    def __init__(self):
        self._available_services : dict[str, type] = SERVICES

    def register_available_service(self, service_name:str, service_class:type):
        self._available_services[service_name] = service_class

    def create_service(self, service_name: str, manager_queue: ProcessQueue, global_response_queue:ProcessQueue): #-> Union[Tuple(ProcessQueue, ProcessQueue), None]:
        if service_name not in self._available_services:
            return None

        request_queue = ProcessQueue()
        response_queue = ProcessQueue()
        
        proxy = ServiceProxy(manager_queue, response_queue)
        service_class = self._available_services[service_name]

        print("LOG: INICIANDO", service_name)

        

        p = Process(target = create_and_run_service, args=(service_class, proxy, request_queue, global_response_queue))
        p.start()

        return request_queue, response_queue

