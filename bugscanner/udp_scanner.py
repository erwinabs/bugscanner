import socket

from .bug_scanner import BugScanner


class UdpScanner(BugScanner):
	# Add default values for clarity/safety
	udp_server_host: str = 'bugscanner.tppreborn.my.id'
	udp_server_port: str = '8853'

	host_list: list

	def get_task_list(self):
		for host in self.host_list:
			yield {
				'host': host,
			}

	def log_info(self, color, status, hostname):
		super().log(f'{color}{status:<6}  {hostname}')

	def init(self):
		super().init()

		self.log_info('', 'Status', 'Host')
		self.log_info('', '------', '----')

	def task(self, payload):
		host = payload['host']

		self.log_replace(host)

		bug = f'{host}.{self.udp_server_host}'
		server_address = (bug, int(self.udp_server_port)) # Use combined address

		G1 = self.logger.special_chars['G1']
		W2 = self.logger.special_chars['W2']

		client = None # Initialize client outside try block

		try:
			client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

			# Sending to (bug, port) is intended for a specific bug,
			# so we use server_address consistently.
			
			client.settimeout(3)
			client.sendto(bug.encode(), server_address)
			client.recv(4)

			client.settimeout(5)
			client.sendto(bug.encode(), server_address)
			client.recv(4)

			client.settimeout(5)
			client.sendto(bug.encode(), server_address)
			client.recv(4)

			self.log_info(G1, 'True', host)

			self.task_success(host)

		except (OSError, socket.timeout):
			self.log_info(W2, '', host)

		finally:
			if client:
				client.close()
