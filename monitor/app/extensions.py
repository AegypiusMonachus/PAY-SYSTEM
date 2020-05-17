from threading import Thread
from queue import Queue

from .common import get_current_time_seconds, sleep_until_time_seconds, Requester


requester = Requester()


class OrderWorker(Thread):
	def __init__(self, queue):
		Thread.__init__(self, daemon=True)
		self.queue = queue

	def run(self):
		self.interrupted = False
		while not self.interrupted:
			item = self.queue.get()

			sleep_until_time_seconds(item['seconds'])
			try:
				requester.post(item['callback'], json={'order_no': item['order']}, timeout=3)
			except:
				pass

	def interrupt(self):
		self.interrupted = True


class OrderManager:
	def __init__(self):
		self.queue = Queue()

		self.workers = []
		for i in range(1):
			self.workers.append(OrderWorker(self.queue))
		for worker in self.workers:
			worker.start()

	def init_app(self, app):
		self.seconds = app.config.get('AUTO_CANCEL_SECONDS', 5)
		self.callback = app.config.get('AUTO_CANCEL_CALLBACK')

	def put(self, order, callback=None):
		self.queue.put({
			'order': order,
			'seconds': get_current_time_seconds() + self.seconds,
			'callback': self.callback,
		})


order_manager = OrderManager()
