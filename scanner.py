import socket
import time
import threading

from queue import Queue


class Scanner:
    def __init__(self, host, max_threads, max_workers):
        self.host = host
        self.host_IP = socket.gethostbyname(self.host)
        self.lock = threading.Lock()
        self.worker_queue = Queue()
        self.start_time = time.time()
        self.working_ports = []
        self.time_passed = 0

        self.max_threads = max_threads

        self.max_workers = max_workers
    
    def scan_port(self, port):
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            connection = soc.connect((self.host_IP, port))
            with self.lock:
                self.working_ports.append(str(port) + ": OPEN")
            connection.close()
        except:
            pass
    
    def thread_handler(self):
        while True:
            worker = self.worker_queue.get()
            self.scan_port(worker)
            self.worker_queue.task_done()
    
    def start_scanning(self):
        for x in range(self.max_threads):
            thread_stuff = threading.Thread(target=self.thread_handler)
            thread_stuff.daemon = False
            thread_stuff.start()
        
        for worker in range(1, self.max_workers):
            self.worker_queue.put(worker)
        
        self.worker_queue.join()

        self.time_passed = time.time() - self.start_time