def search(init, final_values):
    frontiere = [init]
    history = set()  # set > list
    i = 1
    while frontiere:
        print('{} iteration'.format(i))
        i += 1
        etat = frontiere.pop()  # /!\ return this last item
        history.add(etat)
        if etat.final(final_values):
            return etat
        ops = etat.applicable_operators()
        for op in ops:
            new = etat.apply(op)
            if (new not in history) and new.legal():
                # frontiere.append(new)  # dfs
                frontiere.insert(0, new)  # bfs
        frontiere.sort(key=lambda x: -x.lazy_distance(final_values))
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
    print(positions)
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


if __name__ == '__main__':
    read_position()
    derp = read_connections()
    print(derp['Hamburg'])

    for key, val in derp.items():
        print("--------City:", key)
        for key2, val2 in val.items():
            print(key2, val2)
