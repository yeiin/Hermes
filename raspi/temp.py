import network
import videostream
import threading

t1 = threading.Thread(target=network.main)
t1.start()
t2 = threading.Thread(target=videostream.entry)
t2.start()
while True:
	time.sleep(0.1)
	
t1.join()
t2.join()
