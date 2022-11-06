import threading 
import time
import baby
import camera
import network


 
def main():
	try:
		t1 = threading.Thread(target=baby.main)
		t1.start()
		t2 = threading.Thread(target=camera.main)
		t2.start()
		t3 = threading.Thread(target=network.main)
		t3.start()
  
		while True:
			time.sleep(0.1)
	
	except KeyboardInterrupt:
		print("Ctrl+C Pressed.")
		global flag_exit
		flag_exit = True

		if(baby.state == True):
			baby.joinGpioThread(baby.ledt, baby.mobilet,baby.audiot)
		network.close()
		join(t1, t2, t3)

def join(t1, t2, t3):
    print(">>>>main join")
    t1.join()
    t2.join()	
    t3.join()
 
if __name__ == "__main__":
	main()