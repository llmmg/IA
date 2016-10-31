from taquin_viewer import TaquinViewerHTML
import Taquin

if __name__ == '__main__':
    taquin_state1 = [[0, 4, 2],
                     [3, 1, 5],
                     [6, 7, 8]]

    taquin_state10 = [[1, 0, 2],
                      [3, 4, 5],
                      [6, 7, 8]]

    first_move = [[4, 0, 2],
                  [3, 1, 5],
                  [6, 7, 8]]

    sec_move = [[4, 1, 2],
                [3, 0, 5],
                [6, 7, 8]]
    # final_state = Taquin.search(taquin_state10)
    final_state = Taquin.search2FIFO(first_move)
    print(final_state)

with TaquinViewerHTML('example.html') as viewer:
    viewer.add_taquin_state(taquin_state1, "origin")
    # viewer.add_taquin_state(first_move, "first move")
    # viewer.add_taquin_state(sec_move, "second move")
    viewer.add_taquin_state(final_state, "Found state")
