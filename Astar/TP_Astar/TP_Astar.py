import math


class City(object):
    def __init__(self, name, posx, posy):
        self.name = name
        self.x = posx
        self.y = posy
        self.g = 0  # may false algo?


# return dict
def getNeighbour(cityName, connections):
    return connections[cityName]


# TODO: heuristique
def heur0(src, dest):
    return 0


def heur1_x(src, dest, positions):
    dist = int(positions[src][0]) - int(positions[dest][0])
    return dist


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


def search(connections, positions, destination, startCity):
    frontiere = [startCity]  # string city name + g
    history = set()  # set > list
    totDist = 0
    old = startCity
    i = 1
    path=[] #list of visited cities
    while frontiere:
        print('{} iteration'.format(i))
        i += 1
        city = frontiere.pop()  # /!\ return last item
        path.append(city.name)
        history.add(city)
        if city.name != old.name:
            totDist += int(connections[old.name][city.name])
            print(old.name, " ", city.name, "=", totDist)
        city.g = totDist
        old = city
        if city.name == destination.name:
            print(path)
            return city
        neighbours = getNeighbour(city.name, connections)
        for cit, dist in neighbours.items():
           # if cit not in history:
            if any(x.name != cit for x in history):
               frontiere.insert(0, createObjcity(positions)[cit])

        frontiere.sort(key=lambda x: (x.g + heur3_bird(x.name, destination.name, positions)), reverse=True)
        #     if (new not in history) and new.legal():
        #         frontiere.insert(0, new)  # bfs
        # frontiere.sort(key=lambda x: -x.lazy_distance(final_values))
        # frontiere = sorted(frontiere, key=lambda x: -x.lazy_distance(final_values))
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


if __name__ == '__main__':
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

    myObj = createObjcity(read_position())

    # print(heur1_x(myObj['Berlin'].name, myObj['Prague'].name, read_position()))

    search(read_connections(), read_position(), myObj['Budapest'], myObj['Madrid'])

    # for obj,val in createObjcity(read_position()).items():
    #     print(obj,val.name)

    # print(createObjcity(read_position())['Berlin'].name)

    # Calc dist between berlin and Prague
    # print("----Dist Berlin prague---")
    # print(derp['Berlin']['Prague'])
