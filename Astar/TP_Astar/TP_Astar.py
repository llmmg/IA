"""
    Created by Lancelot Magnin
    Last edit: 25.11.2016
"""

import math
import sys


class City(object):
    def __init__(self, name, posx, posy):
        self.name = name
        self.x = posx
        self.y = posy
        self.g = 0
        self.parent = None


# return dict
def getNeighbour(cityName, connections):
    return connections[cityName]


# 3 parameters to keep the same signature as others heuristics functions
def heur0(src, dest, pos):
    return 0


# return x distance between src and dest
def heur1_x(src, dest, positions):
    dist = int(positions[src][0]) - int(positions[dest][0])
    return math.fabs(dist)


# return y distance between src and dest
def heur2_y(src, dest, positions):
    dist = int(positions[src][1]) - int(positions[dest][1])
    return math.fabs(dist)


# return distance between src and dest
def heur3_bird(src, dest, positions):
    distx = int(positions[src][0]) - int(positions[dest][0])
    disty = int(positions[src][1]) - int(positions[dest][1])
    return math.sqrt(math.pow(distx, 2) + math.pow(disty, 2))


# return manhattan distance between src and dest
def heur4_manhattan(src, dest, positions):
    distx = math.fabs(int(positions[src][0]) - int(positions[dest][0]))
    disty = math.fabs(int(positions[src][1]) - int(positions[dest][1]))
    return disty + distx


# search and return the optimal path (a list of cities name is returned)
def search(startCity, destination, numHeuristic):
    # parsing
    positions = read_position()
    connections = read_connections()

    heuristics = [heur0, heur1_x, heur2_y, heur3_bird, heur4_manhattan]
    frontiere = [startCity]  # store City objects
    history = set()  # set > list
    old = startCity  # useful for debug
    i = 0
    path = []  # list of visited cities
    while frontiere:
        i += 1
        # print('\n{} iteration'.format(i))

        city = frontiere.pop()  # /!\ return last item
        path.append(city.name)  # same as history but 'sorted'
        history.add(city)

        # if city.name != old.name:
        #     print(old.name, " ", city.name, "=", city.g)
        # old = city
        if city.name == destination.name:
            print(path)
            print("Optimal distance=", city.g)
            print("Number of cities visited:", len(path))
            print("total iterations:{}".format(i))

            print("\n--Path-- ")
            # show path
            bestPath(city)

            return storeBestPath(city)
        neighbours = getNeighbour(city.name, connections)
        for cit, dist in neighbours.items():
            if not isInList(cit, history):
                tmpCit = createObjcity(positions)[cit]

                # g= parent city.g + dest dist
                tmpCit.g = city.g + int(dist)

                # If g is number of node instead of distance
                # tmpCit.g=city.g+1

                tmpCit.parent = city
                if isInList(tmpCit.name, frontiere):
                    # update in list if new is < than older
                    updateInList(frontiere, tmpCit)
                else:
                    frontiere.insert(0, tmpCit)

        frontiere.sort(key=lambda x: (x.g + heuristics[numHeuristic](x.name, destination.name, positions)),
                       reverse=True)

        # print frontiere and history
        # showFrontierHistory(frontiere,history,heuristics,numHeuristic,positions,destination)

    return None


def showFrontierHistory(front, hist, storedHeuristics, choosenHeur, pos, dest):
    # print frontiere and history
    print("\nfront: ", end=" ")
    for obj in front:
        print(obj.name, " ", obj.g + storedHeuristics[choosenHeur](obj.name, dest.name, pos), " /", end=" ")

    print("\nhist: ", end=" ")
    for obj in hist:
        print(obj.name, " /", end=" ")


# return dict of list that contain 'CityName':[posX,posY]
def read_position():
    positions = {}
    with open('positions.txt', 'r') as f:
        for line in f:
            data = line.split()
            # each lines of files positions is split by space
            # first is name others are x and y
            positions[data[0]] = [data[1], data[2]]
        f.close()
    return positions


# return dict of dicts as 'CityName':
def read_connections():
    connections = {}
    with open('connections.txt', 'r') as f:
        for line in f:
            data = line.split()

            # store a dict{city: dist} in a dictionary.
            # each city has a dictionary of neighbour with the distance.
            # -- as the container dictionary could already have an entry, it need to be updated
            # -- but if it doesnt have any data yet, it need to get a new dictionary
            try:
                connections[data[0]].update({data[1]: data[2]})
            except:
                connections[data[0]] = {data[1]: data[2]}

            # -- add the inverse relation (n1->n2 => n2->n1)
            try:
                connections[data[1]].update({data[0]: data[2]})
            except:
                connections[data[1]] = {data[0]: data[2]}

        f.close()
    return connections


# return dict that contain City objects
def createObjcity(cities):
    myDict = {}

    for city, dist in cities.items():
        myDict[city] = City(city, dist[0], dist[1])

    return myDict


# return true if list contain object with cityName attribute
def isInList(cityName, list):
    for city in list:
        if cityName == city.name:
            return True
    return False


# update city in list if city.g in list is bigger than cityobj.g (new city)
def updateInList(list, cityObj):
    for city in list:
        if city.name == cityObj.name and city.g > cityObj.g:
            city.g = cityObj.g
            city.parent = cityObj.parent


# recursive function that show parents and g of lastCity
def bestPath(lastCity):
    if lastCity.parent is not None:
        bestPath(lastCity.parent)
    print(lastCity.name, " ", lastCity.g)


# recursive function that return a list of the lastCity's name parents
def storeBestPath(lastCity, path=[]):
    if lastCity.parent is not None:
        storeBestPath(lastCity.parent)
    path.append(lastCity.name)
    return path


def main(argv):
    # 1st arg: src city
    # 2nd arg: dest city
    # 3rd arg: heuristic id [0-4]
    srcCity = argv[0]
    destCity = argv[1]
    heuristic = int(argv[2])

    myObj = createObjcity(read_position())
    search(myObj[srcCity], myObj[destCity], heuristic)


if __name__ == '__main__':
    main(sys.argv[1:])
