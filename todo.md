****************** TODO ********************

3. write down the local search algorithm for every zone first and then globally
4. sample the locations of the vehicles using randomisation, using a preprocessing to create the file with vehicles' locations
5. osmnx network visualisation
6. Nof, Nov, Nos to be removed from the parameters file
7. values for beta to be read from a separate file



8. write the demand constraint differently in the pseudocode i.e.
if facility j belongs in zone z then 
\sum_{zeta \in N(z)} where N(z) the neighboring zones of z

9. prove (in words) that the initial solution is feasible


10. In the end of the algorithm
if the demand on each zone is not met then there is no feasible solution


11. randomness in localsearch?

12. CAs of fixed bundle size, specifically size 3

13. demand prediction

14. Preprocessing file to check the tables (read_data checkSizes(parameters)) and a method to convert the input data to AMPL format for pyomo

16. add dictionaries to speed up

17. add a number of facilities in one zone for debugging

18. replace the list of facilities with a dictionary where the key wil be the facility id and value the object of that facility
Each zone will have a list of ids of its facilities
Similarly replace the list of zones with a dictionary
Each facility will keep a value of the key of the zone it belongs to



20. In getDistMatrix() the 'weights' arguments can be omitted

21. visualize the nodes and edges


####################### EXPERIMENTS ##############################
- [ ] Show experimentally by how much the budget constraint is violated using lagrangian relaxation
- [ ] different demand scenarios
- [ ] what happens if the number of EVs changes significantly
- [ ] compare values of lagrangian and opt


################################ LOCAL SEARCH #####################################
Instead of swapping do the following:
- open/close new facilities for the current solution S
- compute the new cost
- if better 
    return the solution
  else
    revert to previous solution by close/open new facilities

################################ MULTIPROCESSING #####################################

- [x] Create local solution class that will have only the variables of a specific zone
- [ ] After initialisation create a dictionary of local solutions (taken from the global one) *localSolutionsDict* for all
the zones
- [ ] Run the for loop (of zones) in local search by splitting the zone Ids into batches and update each local solution in
*localSolutionsDict*
- [ ] (optionally) balance the zones in the batches according to the total number of facilities/combinations that need to be
checked  
- split the lagrangian file into budgeted and unbudgeted


- a dictionary of dictionaries of Values for the x dictionary of dictionaries and an array of arrays of locks


################################ MULTIPROCESSING OF FILES #####################################
- [ ] when reading a file pass as parameters to each process the pointer positions where it should start and end 
reading **[30 mins]**
- [ ] when writing a file, in order to uses multiprocessing, write to different files, one for each process, and in
 the end merge the files **[30 mins]**


################################ TESTING #####################################
- [ ] Before getting an initial solution check if for each vehicle there is at least one facility with NON infinite 
time cost https://docs.python.org/3/library/unittest.html

################################ VISUALISATION #####################################
- [ ] Visualise network nodes
- [ ] Visualise network edges
- [ ] Visualise facilities (different colour than nodes)
- [ ] Visualise vehicles (different colour than nodes and facilities)
- [ ] Show the id of an element when the mouse hovers over it

################################ TIME IMPROVEMENT #####################################
- [ ] Consider only node to open facilities for which every vehicle has not infinite time


- [ ] change import time to from time import time