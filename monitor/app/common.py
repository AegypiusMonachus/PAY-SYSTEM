import time, requests


DEFAULT_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'


def get_current_time_seconds():
	return int(time.time())


def get_current_time_string(format=DEFAULT_TIME_FORMAT):
	return time.strftime(format)


def convert_time_string_to_time_seconds(s, format=DEFAULT_TIME_FORMAT):
	t = time.strptime(s, format)
	return int(time.mktime(t))


def convert_time_seconds_to_time_string(seconds, format=DEFAULT_TIME_FORMAT):
	t = time.localtime(seconds)
	return time.strftime(format, t)


def sleep_until_time_seconds(time_seconds):
	time_seconds = int(time_seconds)
	current_time_seconds = get_current_time_seconds()
	seconds = time_seconds - current_time_seconds
	if seconds > 0:
		time.sleep(seconds)


class Coordinator:
	def __init__(self, seconds):
		self.seconds = seconds
		self.start_time_seconds = get_current_time_seconds()

	def do(self, callback, *args, **kwargs):
		sleep_until_time_seconds(self.start_time_seconds)
		try:
			return callback(*args, **kwargs)
		except:
			raise
		finally:
			self.start_time_seconds = get_current_time_seconds() + self.seconds


class Requester:
	def __init__(self, seconds=2):
		self.coordinator = Coordinator(seconds)

	def request(self, method, url, **kwargs):
		return self.coordinator.do(requests.request, method, url, **kwargs)

	def get(self, url, **kwargs):
		return self.request('GET', url, **kwargs)

	def post(self, url, **kwargs):
		return self.request('POST', url, **kwargs)


if __name__ == '__main__':
	current_time_seconds = get_current_time_seconds()
	print('CURRENT TIME SECONDS:', current_time_seconds)
	current_time_string = get_current_time_string()
	print('CURRENT TIME STRING:', current_time_string)

	time_seconds = convert_time_string_to_time_seconds(current_time_string)
	print('TIME SECONDS:', time_seconds)
	time_string = convert_time_seconds_to_time_string(current_time_seconds)
	print('TIME STRING:', time_string)

	current_time_seconds = get_current_time_seconds()
	current_time_seconds = current_time_seconds + 9
	print('SLEEP UNTIL TIME SECONDS:', current_time_seconds)
	sleep_until_time_seconds(current_time_seconds)

	current_time_seconds = get_current_time_seconds()
	current_time_seconds = current_time_seconds - 9
	print('SLEEP UNTIL TIME SECONDS:', current_time_seconds)
	sleep_until_time_seconds(current_time_seconds)
