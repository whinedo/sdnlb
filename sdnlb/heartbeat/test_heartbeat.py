from heartbeat import HeartBeat
from parser import Parser
import time

def main():

	parser = Parser('/home/mininet/sdnlb/sdnlb/servers.conf')
	services = parser.parse()
	hb = HeartBeat(services)
	hb.start()

	while True:
		time.sleep(20)


if __name__ == "__main__":
	main()
