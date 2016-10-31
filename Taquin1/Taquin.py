import copy


class State:
    matrice = [[]]
    posZero = []

    def __init__(self, mat):
        self.matrice = mat
        # self.field = [[j for j in i] for i in field]
        #   self.zero=self.findzero()
        self.parent = self

    # def applicableoperators(self):
    #     return [op for op in [[0, 1], [0, -1], [1, 0], [-1, 0]] if self.legal(op)]

    def __eq__(self, other):
        if self.matrice == other.matrice:
            return True
        return False

    # def hasIn(self, list):
    #     for x in list:
    #         if x.matrice == self.matrice:
    #             return True
    #     return False

    def attrib(self, newMatrice):
        self.matrice = newMatrice

    def legal(self):
        return True

    def final(self):
        return [[0, 1, 2],
                [3, 4, 5],
                [6, 7, 8]]

    def findHole(self):
        for index, row in enumerate(self.matrice):
            if 0 in row:
                x = row.index(0)  # la position du 0 dans la sous list
                y = index  # la colone
                # self.posZero=[x,y]
        return [x, y]

    def applicableOperators(self):
        # # on ne peut que échanger les cases voisin du 0 avec le '0'
        self.posZero = self.findHole()
        x = self.posZero[0]
        y = self.posZero[1]
        ops = []
        if y is not None and x is not None:
            # possibilités selon la position du 0 (deplacements possibles du 0)
            if x == 1 or x == 2:
                ops.append('LEFT')
            if x == 0 or x == 1:
                ops.append('RIGHT')
            if y == 0 or y == 1:
                ops.append('DOWN')
            if y == 1 or y == 2:
                ops.append('UP')
        return ops

    def swap(self, src, dest):
        src, dest = dest, src

    def apply(self, op):
        newMatrice = copy.deepcopy(self.matrice)
        # newMatrice=self.matrice[:]

        x = ''
        y = ''
        x = self.posZero[0]  # SWAPED
        y = self.posZero[1]  # |

        ###///!!!!\\\\ ==>l'accès aux élements dans la matrice ne se fait pas avec matrice[x][y] mais avec matrice[y][x]
        ###                 car la 1ere colonne de la matrice correspond aux sous liste et donc aux lignes (y)
        if op == 'RIGHT':
            # print("Right")
            # =>echanger la pos du zero avec l'index à droite
            # self.matrice[y][x], self.matrice[y][x + 1] = self.matrice[y][x + 1], self.matrice[y][x]
            newMatrice[y][x], newMatrice[y][x + 1] = newMatrice[y][x + 1], newMatrice[y][x]
        if op == 'LEFT':
            # print("left")
            # self.matrice[y][x], self.matrice[y][x - 1] = self.matrice[y][x - 1], self.matrice[y][x]
            newMatrice[y][x], newMatrice[y][x - 1] = newMatrice[y][x - 1], newMatrice[y][x]
        if op == 'UP':
            # print("up")
            # self.matrice[y][x], self.matrice[y - 1][x] = self.matrice[y - 1][x], self.matrice[y][x]
            newMatrice[y][x], newMatrice[y - 1][x] = newMatrice[y - 1][x], newMatrice[y][x]
        if op == 'DOWN':
            # print("down")
            # self.matrice[y][x], self.matrice[y + 1][x] = self.matrice[y + 1][x], self.matrice[y][x]
            newMatrice[y][x], newMatrice[y + 1][x] = newMatrice[y + 1][x], newMatrice[y][x]

        # self.posZero = self.findHole()
        newState = State(newMatrice)
        newState.posZero = newState.findHole()
        newState.parent = self

        # print(newState.matrice)
        # print(newState.posZero)
        newState.op = op
        return newState


def search(init):
    frontiere = []
    history = [] #set rather than list
    # frontiere.append(State(init))
    frontiere = [State(init)]
    while frontiere:
        etat = frontiere.pop()
        # oldState=copy.deepcopy(etat)
        # history.append(oldState)
        history.append(etat)
        # print("etat initiale dans history:" + str(history[0].matrice))
        # print("history:"+str(etat.matrice))
        if etat.matrice == etat.final():
            return etat.matrice
        ops = etat.applicableOperators()
        # print(ops)
        # print("hist: " + str(len(history)))
        print("front: " + str(len(frontiere)))
        for op in ops:
            # print(op)
            new = etat.apply(op)
            #recherche dans list est couteux => utiliser un set pour l'history
            if (new not in frontiere) and (new not in history) and new.legal():
                # insert(frontiere, new)
                frontiere.append(new)
                print(new.matrice)



    return [[]]


import queue


#
# class CheckableQueue(queue.Queue):  # or OrderedSetQueue
#     def __contains__(self, item):
#         with self.mutex:
#             return item in self.queue

def search2FIFO(init):
    frontiere = queue.deque()
    history = []
    frontiere.append(State(init))
    # frontiere.put(State(init))
    while len(frontiere) > 0:
        etat = frontiere.popleft()
        # oldState=copy.deepcopy(etat)
        # history.append(oldState)
        history.append(etat)
        # print("etat initiale dans history:" + str(history[0].matrice))
        # print("history:"+str(etat.matrice))
        if etat.matrice == etat.final():
            return etat.matrice
        ops = etat.applicableOperators()
        # print(ops)
        print(etat.matrice)
        # print("hist: " + str(len(history)))
        # print("front: " + str(frontiere.maxsize))
        for op in ops:
            new = etat.apply(op)
            # print("new matrice: " + str(new.matrice))
            # print("in frontier " + str(new in frontiere))
            # print("in history " + str(new in history))

            if (new not in frontiere) and (new not in history) and new.legal():
                # insert(frontiere, new)
                frontiere.append(new)
                # print(new.matrice)
                # print("stored!")
                # print("front: " + str(len(frontiere)))
                # else:
                # print("alredy in lists!")
                # print("history matrice: " + str(history[0].matrice))
                # print("hist: " + str(len(history)))
                # print("front: " + str(len(frontiere)))

    return [[]]
