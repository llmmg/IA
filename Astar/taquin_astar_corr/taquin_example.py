from taquin_viewer import TaquinViewerHTML
from state import State


def search(init, final_values):
    frontiere = [init]
    history = set()  # set > list
    i=1
    while frontiere:
        print('{} iteration'.format(i))
        i+=1
        etat = frontiere.pop() # /!\ return this last item
        history.add(etat)
        if etat.final(final_values):
            return etat
        ops = etat.applicable_operators()
        for op in ops:
            new = etat.apply(op)
            if (new not in history) and new.legal():
                #frontiere.append(new)  # dfs
                frontiere.insert(0, new)  # bfs
        frontiere.sort(key=lambda x: -x.lazy_distance(final_values))
        #frontiere = sorted(frontiere, key=lambda x: -x.lazy_distance(final_values))
    return None

if __name__ == '__main__':
    #taquin_state1 = [[1, 2, 3], [4, 8, 5], [0, 7, 6]]
    taquin_state1 = [[2, 3, 4, 5, 0], 
                    [1, 6, 8, 9, 10],
                    [12, 7, 13, 14, 15],
                    [11, 17, 18, 24, 19],
                    [16, 21, 22, 23, 20]]

    #final_values = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
    final_values = [[1, 2, 3, 4, 5], 
                    [6, 7, 8, 9, 10],
                    [11, 12, 13, 14, 15],
                    [16, 17, 18, 19, 20],
                    [21, 22, 23, 24, 0]]

    result = search(State(taquin_state1), final_values)
    if result is not None:
        winning_path = []
        while result.parent is not None:
            winning_path.insert(0, result)
            result = result.parent
        winning_path.insert(0, result)
        with TaquinViewerHTML('example.html') as viewer:
            for i, state in enumerate(winning_path):
                viewer.add_taquin_state(state.values, title=i)
    else:
        print('solution not found')
