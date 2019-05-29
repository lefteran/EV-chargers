def isFacilityFull(S, facility):
	return S.y[facility.id] == facility.capacity
	
def hasFacilityStandardCPs(S, facId):
	return S.st[facId] != 0

def hasFacilityRapidCPs(S, facId):
	return S.r[facId] != 0

def getNextNotFullFacility(S, sortedByCapacity, index):
	for i in range(index, len(sortedByCapacity)):
		facility = sortedByCapacity[i]
		if not isFacilityFull(S, facility):
			return sortedByCapacity[i]

# *** THE FOLLOWING METHOD TO BE MOVED INSIDE SOLUTION CLASS ***
def redistributeCPs(S, zoneFacilities):
	sortedByCapacity = sorted(zoneFacilities, key=lambda x: x.capacity, reverse=True)
	index = 0
	facilityToFill = getNextNotFullFacility(S, sortedByCapacity, index)
	for facilityToEmpty in sortedByCapacity[::-1]:
		standardFacsToMove = S.st[facilityToEmpty.id]
		rapidFacsToMove = S.r[facilityToEmpty.id]
		for i in range(standardFacsToMove):
			S.increaseStandardCP(facilityToFill.id)
			S.removeStandardCP(facilityToEmpty.id)
			if (not hasFacilityStandardCPs(S, facilityToEmpty.id)) and (not hasFacilityRapidCPs(S, facilityToEmpty.id)):
				S.close_facility(facilityToEmpty.id)
			if isFacilityFull(S, facilityToFill):
				facilityToFill = getNextNotFullFacility(S, sortedByCapacity, index)
			if facilityToEmpty.id == facilityToFill.id:
				break
		for i in range(rapidFacsToMove):
			S.increaseRapidCP(facilityToFill.id)
			S.removeRapidCP(facilityToEmpty.id)
			if (not hasFacilityStandardCPs(S, facilityToEmpty.id)) and (not hasFacilityRapidCPs(S, facilityToEmpty.id)):
				S.close_facility(facilityToEmpty)
			if isFacilityFull(S, facilityToFill):
				facilityToFill = getNextNonFullFac(S, sortedByCapacity, index)
			if facilityToEmpty.id == facilityToFill.id:
				break
	
	# **** CHECK AFTER CLOSING EMPTY FACILITIES, IF THE VEHICLES ARE ASSIGNED TO NEW ONES ******