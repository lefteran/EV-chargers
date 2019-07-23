import time
import settings
import preprocessing as pre

if __name__ == "__main__":
	start_time = time.time()
	print("#########################################################\n#########################################################")
	settings.init()
	print(f"setting value is {settings.parameters.gamma}")
	pre.preprocessing(settings.flags.doPreprocessing)
	print("--- %s seconds ---" % (time.time() - start_time))

