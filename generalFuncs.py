def currentDemand(parameters, S, z):
	total_value = 0
	for zeta in range(parameters.Noz):
		value = 0
		for j in range(parameters.Nof):
			value = value + parameters.H[j][zeta] * S.y[j]
		total_value = total_value + parameters.A[z][zeta] * value
	return total_value

def currentOnstreetCPs(parameters, S, z):
	value = 0
	for j in range(parameters.Nof):
		value = value + parameters.alpha[j] * parameters.H[j][z] *S.y[j]
	return value

