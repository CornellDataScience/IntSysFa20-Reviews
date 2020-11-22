from gerrypy.data.load import load_opt_data
import networkx as nx
import matplotlib.pyplot as plt
import copy
import numpy as np
from scipy.spatial import distance
import time

'''
state_df columns:
Index(['GEOID', 'x', 'y', 'area', 'population',
       'p_public_transportation_commute', 'p_walk_commute',
       'mean_commute_time', 'p_bachelors_degree_or_higher',
       'unemployment_rate', 'p_GRAPI<15%', 'p_GRAPI>35%',
       'p_without_health_insurance', 'p_nonfamily_household',
       'p_vacant_housing_units', 'p_renter_occupied',
       'median_household_income', 'p_SNAP_benefits', 'p_below_poverty_line',
       'p_white', 'p_age_students', 'median_age', 'p_mobile_homes',
       'p_without_person_vehicle', 'p_veterans', '2000', '2004', '2008',
       '2012', '2016'],
      dtype='object') 

Initial solutions: 
A list of plans(dict of districts(key is district id, value is the node)) 
'''

class LocalSearch:

    def __init__(self, state_df, G, initial_solutions, obj_func):
        self.state_df = state_df
        self.G = G
        self.initial_solutions = initial_solutions
        self.times = np.empty(1)
        self.obj_func = obj_func


    def hill_climbing(self, iterations):
        ''' Hill climbing given one initial solution '''
        current = self.initial_solutions[0]
        for i in range(iterations):
            print(i)
            start_time = time.time()
            new_solution = self.get_best_solutions(current)
            if new_solution == current:
                break
            current = new_solution
            print(time.time() - start_time)
            np.append(self.times, time.time() - start_time)
        return current
    
    def get_best_solutions(self, initial_solution):
        ''' Returns a list of all feasible neighboring solutions given an initial solution'''
        # Construct dictionary: nodes as keys, their corresponding district as value
        district_of_node = {n: d for d, nodes in initial_solution.items() for n in nodes}

        # Store obj of each district in a dictionary so that it only needs to be calculated once
        obj = {}
        for d, tracts in initial_solution.items():
            obj[d] = self.obj_func(tracts)
        print(obj)

        # Check all the edges to identify adj nodes in two district, switch them to get a new solution
        solution = copy.deepcopy(initial_solution)
        for u, v in self.G.edges():
            if district_of_node[u] != district_of_node[v]: 
                old_d1 = district_of_node[u]
                new_tracts1 = copy.deepcopy(solution[old_d1])
                new_tracts1.remove(u)
                new_tracts1.append(v)
                old_d2 = district_of_node[v]
                new_tracts2 = copy.deepcopy(solution[old_d2])
                new_tracts2.remove(v)
                new_tracts2.append(u)
                # Test whether it improves the objective
                new_obj1, new_obj2 = self.obj_func(new_tracts1), self.obj_func(new_tracts2)
                if (new_obj1 + new_obj2) < (obj[old_d1] + obj[old_d2]):
                    solution[old_d1], solution[old_d2] = new_tracts1, new_tracts2
                    obj[old_d1], obj[old_d2] = new_obj1, new_obj2 # update with values of new solution so as to find the optimum
                    district_of_node[u], district_of_node[v] = old_d2, old_d1 # update district of the node
                    
        return solution

    def is_feasible(self, solution):
        ''' Returns True if the solution preserves population tolerance and spatial contiguity '''
        # population tolerance
        e = 0.01
        ideal_population = self.state_df.population.sum() / len(solution)
        for tracts in solution.values():
            population = self.state_df.iloc[tracts].population.sum()
            dev = (ideal_population - population) / ideal_population
            if abs(dev) > e:
                return False

        # contiguity
        # TODO: use a faster algorithm
        for tracts in solution.values():
            if not nx.is_connected(G.subgraph(tracts)):
                return False

        return True

def dispersion(tracts):
    ''' Given a district (list of tracts), returns the dispersion '''
    population = state_df.loc[tracts]['population'].values
    dlocs = state_df.loc[tracts][['x', 'y']].values
    centroid = np.average(dlocs, weights=population, axis=0)
    geo_dispersion = (np.subtract(dlocs, centroid) ** 2).sum(axis=1) ** .5 / 1000
    dispersion = np.average(geo_dispersion, weights=population)
    return dispersion

if __name__ == "__main__": 
    state = 'WI'
    state_df, G, lengths, edge_dists = load_opt_data(state)
    initial_solutions = nx.read_gpickle("gerrypy/optimize/WI_sample_plans.p")
    local_search = LocalSearch(state_df, G, initial_solutions, dispersion)
    local_search.hill_climbing(10)