import time
import settings
import test

if __name__ == "__main__":
	start_time = time.time()
	print("#########################################################\n#########################################################")
	settings.init()
	test.stuff()
	print(f"setting value is {settings.parameters.gamma}")
	print("--- %s seconds ---" % (time.time() - start_time))

