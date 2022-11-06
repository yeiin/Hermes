import threading 
import time
import baby
import camera
 
def main():
	try:
		t1 = threading.Thread(target=baby.main)
		t1.start()
		t2 = threading.Thread(target=camera)
		t2.start()
  
		while True:
			time.sleep(0.1)
	
	except KeyboardInterrupt:
		print("Ctrl+C Pressed.")
		global flag_exit
		flag_exit = True

		if(baby.state == True):
			print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>state True")
			baby.joinGpioThread(baby.ledt, baby.mobilet,baby.audiot)
		
		join(t1, t2)

def join(t1, t2):
    print(">>>>>>>>>>>>>>join")
    t1.join()
    t2.join()		
 
if __name__ == "__main__":
	main()