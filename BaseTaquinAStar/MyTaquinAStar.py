from taquin_viewer import TaquinViewerHTML
from state import State
from heapq import heappush, heappop
import operator


# goal: h=0 (ordered)
# select the state (path) with lower f(n)=g(h)+h(h)
# g= cost
# h= disordered numbers

def search(init, final_values):
    frontiere = [init]
    elems = dict()
    # elems = {init: fValue(init, final_values)}  # dict
    # frontier_trie = sorted(elems.items(), key=operator.itemgetter(1))  # list
    history = set()  # set > list
    while frontiere:
        etat = frontiere.pop()  # take 1st item of frontier_trie
        history.add(etat)
        if etat.final(final_values):
            # the research is done
            return etat

        ops = etat.applicable_operators()
        for op in ops:
            new = etat.apply(op)
            # here we need to select best state
            if (new not in history) and new.legal():
                frontiere.insert(0, new)
        frontiere.sort(key=lambda x: -x.h(final_values))
        # print(sorted(elems.values()))
        # print(elems.values())
        # test = sorted(elems.items(), key=operator.itemgetter(1))
        # for e in test:
        #     print(e[0])
        # for k in test:
        #     if (k[0] not in history) and k[0].legal():
        #         frontiere.append(k[0])  # dfs
        # frontiere.insert(0, k[0])  # bfs

    return None


def fValue(state, final):
    return state.g() + state.h(final)


if __name__ == '__main__':
    taquin_state1 = [[1, 2, 3],
                     [4, 6, 8],
                     [7, 0, 5]]

    final_values = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

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
