class State:
    matrice = [[]]
    posZero = []

    def __init__(self, mat):
        self.matrice = mat

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
        # for index, row in enumerate(self.matrice):
        #     if 0 in row:
        #         x = row.index(0)  # la position dans la sous list
        #         y = index  # la colone
        #         self.posZero = [x, y]  # Contain position(indexes) of the 0
        self.posZero = self.findHole()
        x = self.posZero[0]
        y = self.posZero[1]
        ops = []
        if y is not None and x is not None:
            # possibilités selon la position du 0 (deplacements possibles du 0)
            if x == 0 or x == 1:
                ops.append('RIGHT')
            if x == 1 or x == 2:
                ops.append('LEFT')
            if y == 0 or y == 1:
                ops.append('DOWN')
            if y == 1 or y == 2:
                ops.append('UP')
        return ops

    def swap(self, src, dest):
        src, dest = dest, src

    def apply(self, op):
        x = ''
        y = ''
        x = self.posZero[0]
        y = self.posZero[1]mn
        print(x,y)
        print(self.matrice)
        # print(self.matrice[x][y])
        # print(self.matrice[1][2])
        # print(self.matrice[2][2])
        # print(self.matrice[2][0])


        if op == 'RIGHT':
            print("Right")
            # =>echanger la pos du zero avec l'index à droite

            self.matrice[x][y], self.matrice[x + 1][y] = self.matrice[x + 1][y], self.matrice[x][y]
            # print(self.matrice)
        if op == 'LEFT':
            print("left")
            self.matrice[x][y], self.matrice[x - 1][y] = self.matrice[x - 1][y], self.matrice[x][y]
        if op == 'UP':
            print("up")
            # dest = self.matrice[x][y - 1]
            # self.swap(zero, dest)
            self.matrice[x][y], self.matrice[x][y - 1] = self.matrice[x][y - 1], self.matrice[x][y]
        if op == 'DOWN':
            print("down")
            # dest = self.matrice[x][y + 1]
            # self.swap(zero, dest)
            self.matrice[x][y], self.matrice[x][y - 1] = self.matrice[x][y - 1], self.matrice[x][y]

        # print('end of apply:')
        # print(self.matrice)
        self.posZero = self.findHole()
        newState = State(self.matrice)
        newState.posZero = newState.findHole()
        # TODO mettre à jour la position du zéro après chaque déplacements
        newState.parent = self
        newState.op = op
        # print(newState.matrice)
        return newState


def search(init):
    frontiere = [State(init)]
    history = []
    while frontiere:
        etat = frontiere.pop()
        history.append(etat)
        # print(etat.matrice)
        if etat.matrice == etat.final():
            return etat.matrice
        ops = etat.applicableOperators()
        for op in ops:
            # print("apply opp")
            new = etat.apply(op)
            print(new.matrice)
            if (new not in frontiere) and (new not in history) and new.legal():
                # insert(frontiere, new)
                frontiere.append(new)
    return
