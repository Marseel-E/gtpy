from flask import Flask, Response, request
from requests import post


class App(Flask):
	def __init__(self) -> None:
		super().__init__(__name__)

		self.target_host = None
		self.target_port = None

		self.add_url_rule("/fetch_targets", "return_hostnport", self.return_hostnport, methods=['GET'])
		self.add_url_rule("/growtopia/server_data.php", "server_data", self.server_data, methods=['POST', 'GET'])
		
	
	def return_hostnport(self):
		return {
			"server": self.target_host,
			"port": self.target_port
		}
	

	def server_data(self):
		response: Response = post(
			url="https://www.growtopia2.com/growtopia/server_data.php",
			data=request.get_data(),
			headers=request.headers
		)

		content: str = response.content.decode().replace("\r", "")

		print(content)

		meta: str = ""
		for pair in content.split("\n"):
			if len(pair.split("|")) == 2:
				key, value = pair.split("|")
				
				if key == "server":
					self.target_host = value
				if key == "port":
					self.target_port = value
				if key == "meta":
					meta = value

		print(self.target_host, self.target_port)

		return Response(
			f"server|127.0.0.1\nport|10000\ntype|1\n#maint\nbeta_server|127.0.0.1\nbeta_port|17095\nbeta_type|1\nmeta|{meta}\nRTENDMARKERBS1001",
		mimetype="plain/text",
		)


if __name__ == '__main__':
	App().run(
		host="127.0.0.1",
		port=443,
		ssl_context=("cert.pem", "key.pem")
	)