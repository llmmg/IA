from taquin_viewer import TaquinViewerHTML
from state import State


def search(init, final_values):
    frontiere = [init]
    history = set()
    while frontiere:
        etat = frontiere.pop()
        history.add(etat)
        if etat.final(final_values):
            return etat
        ops = etat.applicable_operators()
        for op in ops:
            new = etat.apply(op)
            if (new not in history) and new.legal():
                #  frontiere.append(new)  # dfs
                frontiere.insert(0, new)  # bfs
    return None

if __name__ == '__main__':
    taquin_state1 = [[1, 2, 3, 4],
                     [5, 0, 7, 8],
                     [9, 6, 10, 12],
                     [13, 14, 11, 15]]

    final_values = [[1, 2, 3, 4],
                     [5, 6, 7, 8],
                     [9, 10, 11, 12],
                     [13, 14, 15, 0]]

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
