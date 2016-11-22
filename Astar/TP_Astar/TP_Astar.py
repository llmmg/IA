import math
import sys


class City(object):
    def __init__(self, name, posx, posy):
        self.name = name
        self.x = posx
        self.y = posy
        self.g = 0  # may false algo?


# return dict
def getNeighbour(cityName, connections):
    return connections[cityName]


def heur0(src, dest):
    return 0


def heur1_x(src, dest, positions):
    dist = int(positions[src][0]) - int(positions[dest][0])
    return math.fabs(dist)


def heur2_y(src, dest, positions):
    dist = int(positions[src][1]) - int(positions[dest][1])
    return dist


def heur3_bird(src, dest, positions):
    distx = int(positions[src][0]) - int(positions[dest][0])
    disty = int(positions[src][1]) - int(positions[dest][1])
    return math.sqrt(math.pow(distx, 2) + math.pow(disty, 2))


def heur4_manhattan(src, dest, positions):
    distx = int(positions[src][0]) - int(positions[dest][0])
    disty = int(positions[src][1]) - int(positions[dest][1])
    return disty + distx


def search(connections, positions, startCity, destination):
    frontiere = [startCity]  # string city name + g
    history = set()  # set > list
    totDist = 0
    old = startCity
    i = 1
    path = []  # list of visited cities
    while frontiere:
        print('{} iteration'.format(i))
        i += 1
        city = frontiere.pop()  # /!\ return last item
        path.append(city.name)
        history.add(city)

        if city.name != old.name:
            try:
                totDist += int(connections[old.name][city.name])
                print(old.name, " ", city.name, "=", totDist)
            except:
                print("back to:", city.name)

        city.g = totDist
        old = city
        if city.name == destination.name:
            print(path)
            # for obj in history:
            #     print(obj.name)
            # print(bestPath(path))
            return city
        neighbours = getNeighbour(city.name, connections)
        for cit, dist in neighbours.items():
            # if cit not in history:
            # if any((cit != x.name) for x in history):
            if not isInList(cit, history):
                tmpCit = createObjcity(positions)[cit]
                # g is updated even if there's a "back to" so
                # => g may be crushed
                # tmpCit.g = totDist + int(dist)
                tmpCit.g += int(dist)
                if isInList(tmpCit.name, frontiere):
                    # update in list if new is < than older
                    updateInList(frontiere, tmpCit)
                else:
                    frontiere.insert(0, tmpCit)

                    # print(tmpCit.name, " ", tmpCit.g + heur1_x(tmpCit.name, destination.name, positions))
        frontiere.sort(key=lambda x: (x.g + heur1_x(x.name, destination.name, positions)), reverse=True)

        print("\nfront: ", end=" ")
        for obj in frontiere:
            print(obj.name, " ", obj.g + heur1_x(obj.name, destination.name, positions), " /", end=" ")

        print("\nhist: ", end=" ")
        for obj in history:
            print(obj.name, " /", end=" ")

            # frontiere.sort(key=lambda x: x.name in neighbours)
            # for asdf in frontiere:
            #     print("eh",asdf.name)
    return None


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
    # print(positions)
    return positions


def read_connections():
    connections = {}
    with open('connections.txt', 'r') as f:
        for line in f:
            data = line.split()

            try:
                connections[data[0]].update({data[1]: data[2]})
            except:
                connections[data[0]] = {data[1]: data[2]}

            try:
                connections[data[1]].update({data[0]: data[2]})
            except:
                connections[data[1]] = {data[0]: data[2]}

        f.close()
    return connections


def createObjcity(cities):
    myDict = {}

    for city, dist in cities.items():
        # print(city, dist)
        myDict[city] = City(city, dist[0], dist[1])

    return myDict


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


# get path - DOES NOT WORK /!\
def bestPath(wholePath):
    realPath = []
    tmp = wholePath.pop()
    while wholePath:
        neigbOftmp = getNeighbour(tmp, read_connections())
        if wholePath[-1] in neigbOftmp:
            tmp = wholePath.pop()
            realPath.append(tmp)
        else:
            wholePath.pop()

    realPath.reverse()
    return realPath


def tests():
    read_position()
    derp = read_connections()
    # print(derp['Berlin']['Warsaw'])
    # print(derp['Warsaw']['Budapest'])
    # print(derp['Budapest']['Belgrade'])


    # for key, val in derp.items():
    #     print("--------City:", key)
    #     for key2, val2 in val.items():
    #         print(key2, val2)

    # show all neighbourd of "berlin"
    # for key, val in derp.items():
    #     if key == 'Berlin':
    #         print(key, val)

    # print("---neighbours----")
    # for neig,t in derp['Berlin'].items():
    #     print(neig,t)

    # for key, val in getNeighbour('Berlin', derp).items():
    #     print(key, val)

    # print("----position------")
    # print(read_position()['Berlin'][0])  # [0] 626
    # print(read_position()['Prague'][0])
    # print(heur1_x(myObj['Berlin'].name, myObj['Prague'].name, read_position()))

    # for obj,val in createObjcity(read_position()).items():
    #     print(obj,val.name)

    # print(createObjcity(read_position())['Berlin'].name)

    # Calc dist between berlin and Prague
    # print("----Dist Berlin prague---")
    # print(derp['Berlin']['Prague'])


def main(argv):
    srcCity = argv[0]
    destCity = argv[1]
    # TODO: argv[2] for heuristic

    myObj = createObjcity(read_position())
    search(read_connections(), read_position(), myObj[srcCity], myObj[destCity])


if __name__ == '__main__':
    main(sys.argv[1:])
