### MAIN FUNCTION


In the main function the following imports take place first:

- The network nodes
- The network edges
- The dictionary belongingDict keeps as keys the node ids and each has as value the zone in which it belongs to.
The node ids whose value in belongingDict is empty are returned in the list nonBelongingNodeIds and are then removed from the network.
- A dictionary that keeps the ids of the zones which are adjacent to each zone.


vehiclesDict is a dictionary of the vehicles with keys the vehicle ids and values the objects of the vehicles.

facilitiesDict is a 

The distancesDict is a dictionary whose values are also dictionaries. 

beta is a list of 24\*60 entries 
time of a day counted in minutes starting from 0:00 and ending in 23:59



### DATA FILES
Belonging file contains node ids with an empty boundary id. However the inverse Belonging file contains only the nodes
which are within some boundary (ignoring the empty boundary ids from the belonging file).


*ZoneData.csv*
```
ZoneId	Demand	OnStreetBound
2488	190		150
4088	185		122
```