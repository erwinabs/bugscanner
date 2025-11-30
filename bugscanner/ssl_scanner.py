import socket
import ssl

from .bug_scanner import BugScanner


class SSLScanner(BugScanner):
	host_list = []
	# New configurable attributes
	connect_host: str = '77.88.8.8'
	connect_port: str = '443'

	def get_task_list(self):
		for host in self.filter_list(self.host_list):
			yield {
				'host': host,
			}

	def log_info(self, color, status, server_name_indication):
		super().log(f'{color}{status:<6}  {server_name_indication}')

	def log_info_result(self, **kwargs):
		G1 = self.logger.special_chars['G1']
		W2 = self.logger.special_chars['W2']

		status = kwargs.get('status', '')
		status = 'True' if status else ''
		server_name_indication = kwargs.get('server_name_indication', '')

		color = G1 if status else W2

		self.log_info(color, status, server_name_indication)

	def init(self):
		super().init()

		self.log_info('', 'Status', 'Server Name Indication')
		self.log_info('', '------', '----------------------')

	def task(self, payload):
		server_name_indication = payload['host']

		self.log_replace(server_name_indication)

		response = {
			'server_name_indication': server_name_indication,
		}

		try:
			socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			socket_client.settimeout(5)
			
			# Use configurable host and port
			socket_client.connect((self.connect_host, int(self.connect_port)))
			
			socket_client = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2).wrap_socket(
				socket_client, server_hostname=server_name_indication, do_handshake_on_connect=True
			)
			response['status'] = True

			self.task_success(server_name_indication)

		except (socket.timeout, socket.error, ssl.SSLError):
			# More specific error handling
			response['status'] = False

		except Exception:
			# Catch any other unexpected errors
			response['status'] = False
			
		finally:
			if 'socket_client' in locals() and isinstance(socket_client, socket.socket):
				socket_client.close()

		self.log_info_result(**response)
