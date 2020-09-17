


def test_method():
	K = [1,4,5,[6,54,7],8,7,4,5,89]

	for index, m in enumerate(K[1:]):
		# if index != 0:
		print(f"m is {m} and index is {index}")
		print(f'K[index] is {K[index + 1]} and K[m-1] is {K[index]}')
		print(f"m")