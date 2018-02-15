import numpy as np
import time
import os
import pickle

N, E, S, W, FIRE = 0, 1, 2, 3, 4

class Bot(object):
    def __init__(self, player, name, x, y, movespeed):
        self.player = player
        self.type = "Bot"
        self.name = name
        self.x = x
        self.y = y
        self.movespeed = movespeed
        self.last_direction = N
        self.last_fire = 0
    def move(self, timestep, direction):
        self.last_fire += timestep
        if direction == N:
            self.y += self.movespeed * timestep
        elif direction == S:
            self.y -= self.movespeed * timestep
        elif direction == E:
            self.x += self.movespeed * timestep
        elif direction == W:
            self.x -= self.movespeed * timestep
        self.last_direction = direction
    def fire(self, timestep):
        self.last_fire += timestep
        if self.last_fire < 0:
            return None
        else:
            self.last_fire = -3
        if self.last_direction == N:
            return Projectile(self.name + " projectile", self.x, self.y + 1, 3, self.last_direction)
        elif self.last_direction == S:
            return Projectile(self.name + " projectile", self.x, self.y - 1, 3, self.last_direction)
        elif self.last_direction == E:
            return Projectile(self.name + " projectile", self.x + 1, self.y, 3, self.last_direction)
        elif self.last_direction == W:
            return Projectile(self.name + " projectile", self.x - 1, self.y, 3, self.last_direction)

class Projectile(object):
    def __init__(self, name, x, y, movespeed, direction):
        self.type = "Projectile"
        self.name = name
        self.x = x
        self.y = y
        self.movespeed = movespeed
        self.direction = direction
    def move(self, timestep):
        if self.direction == N:
            self.y += self.movespeed * timestep;
        if self.direction == S:
            self.y -= self.movespeed * timestep;
        if self.direction == E:
            self.x += self.movespeed * timestep;
        if self.direction == W:
            self.x -= self.movespeed * timestep;

class BattleWorld(object):
    def __init__(self):
        self.border = 7.9
        xA, yA, xB, yB = 0, 0, 0, 0
        while np.abs(xA - xB) < 3 or np.abs(yA - yB) < 3:
            xA, yA, xB, yB = np.random.randint(100)/100*self.border, np.random.randint(100)/100*self.border, np.random.randint(100)/100*self.border, np.random.randint(100)/100*self.border
        self.bots = {1: Bot(1, "Alpha", xA, yA, 1), 2: Bot(2, "Beta", xB, yB, 1)}
        self.objects = [self.bots[1], self.bots[2]]
        self.timestep = 0.15
        self.win = None
        self.counter = 0
    def act(self, player, move):
        if move in [N, E, S, W]:
            self.bots[player].move(self.timestep, move)
        elif move == FIRE:
            ret_obj = self.bots[player].fire(self.timestep)
            if ret_obj:
                self.objects.append(ret_obj)
    def observe(self, player):
        if player == 1:
            enemy = 2
        elif player == 2:
            enemy = 1
        assert enemy
        x = (self.bots[enemy].x, self.bots[enemy].y, self.bots[player].x, self.bots[player].y, self.bots[player].last_direction, self.bots[player].last_fire >= 0)
        r = 0
        if self.win:
            if self.win == player:
                r = 1
            elif self.win == 0:
                r = -0.5
            else:
                r = -1
        return x, r
    def passive_move(self):
        self.counter += 1
        remove = set()
        for i, obj in enumerate(self.objects):
            if obj.type == "Projectile":
                obj.move(self.timestep)
                if obj.x < 0 or obj.y < 0 or obj.x > self.border or obj.y > self.border:
                    remove.add(i)
            else:
                if obj.x < 0:
                    obj.x = 0
                if obj.y < 0:
                    obj.y = 0
                if obj.x > self.border:
                    obj.x = self.border
                if obj.y > self.border:
                    obj.y = self.border
        for i, objA in enumerate(self.objects):
            if objA.type == "Projectile":
                for j, objB in enumerate(self.objects):
                    if i != j:
                        if np.abs(objA.x - objB.x) < 0.9 and np.abs(objA.y - objB.y) < 0.9:
                            remove.add(i)
                            remove.add(j)
        for i in sorted(list(remove), reverse=True):
            if self.objects[i].type == "Projectile":
                self.objects.pop(i)
            elif self.objects[i].type == "Bot":
                if self.win == None:
                    if self.objects[i].player == 1:
                        self.win = 2
                    elif self.objects[i].player == 2:
                        self.win = 1
                    assert self.win
                else:
                    self.win = 0
        if np.abs(self.bots[1].x - self.bots[2].x) < 0.9 and np.abs(self.bots[1].y - self.bots[2].y) < 0.9:
            self.win = 0
        if self.counter > 400:
            self.win = 0
        return self.win
    def show(self, iter_name):
        os.system("clear")
        print(iter_name, self.counter)
        tiles = {}
        for obj in self.objects:
            _x = int(obj.x)
            _y = int(obj.y)
            if obj.type == "Bot":
                if obj.player == 1:
                    if self.win == 2:
                        _c = 0
                    else:
                        _c = 1
                else:
                    if self.win == 1:
                        _c = 0
                    else:
                        _c = 2
            else:
                _c = 0
            pos = str(_x) + " " + str(_y)
            tiles[pos] = _c
        for y in range(8):
            for x in range(8):
                pos = str(x) + " " + str(y)
                if pos in tiles:
                    print(tiles[pos], end="")
                else:
                    print(".", end="")
            print("", flush=True)
        time.sleep(0.050)

class ModelAbsctract(object):
    # This is the class that shows how RL algo should be mplemented.
    def __init__(self):
        # This method is called once and it should init internal parameters.
        pass
    def refresh(self):
        # This method is called between battles, so you get notified about the session end.
        pass
    def act(self, x, r, exploit=0.9):
        # This method accepts observation `x`, reward `r` and `exploit` rate.
        # x is (enemy_x, enemy_y, player_x, player_y, front_direction, is_reloaded)
        # they are (float, float, float, float, int, bool)
        # You may want to change coordinates to ints so you could easily produce states.
        # exploit rate shows the probability that you should do the right (non-exploration) turn.
        # You can ignore this parameter if you want to.
        # Be default it is 0.9 at training and 1.0 at demonstration.
        # You should return one of actions.
        # Available actions are N, E, S, W, FIRE. They are integers 0-4.
        # They are defined as constants at the header of this file.
        return 0

class ModelTD(object):
    def __init__(self):
        self.states = {}
        self.last_s = None
        self.last_a = None
        self.learn_rate = 0.1
        self.discount = 0.99
    def refresh(self):
        self.last_s = None
        self.last_a = None
    def act(self, x, r, exploit=0.9) -> int:
        if np.random.randint(100) / 100.0 > exploit:
            return np.random.randint(5)
        s = self._get_state(x)
        if s in self.states:
            q = self.states[s]
            a = np.argmax(q)
        else:
            q = np.random.random((5,))
            self.states[s] = q
            a = np.random.randint(5)
        if self.last_s is not None and self.last_a is not None:
            self.states[self.last_s][self.last_a] += \
                    self.learn_rate * ( r + self.discount * np.max(q) - self.states[self.last_s][self.last_a] )
        self.last_s = s
        self.last_a = a
        return a
    def _get_state(self, x): # This internal function produces states from observation.
        x = list(x)
        x[0] *= 1.2
        x[1] *= 1.2
        x[2] *= 1.2
        x[3] *= 1.2
        state = ' '.join(map(lambda x: str(int(x)), x))
        return state # It returns the string that can be used to distinguish this state from anothers.

class ModelMC(object):
    def __init__(self):
        self.states = {}
        self.history = []
        self.learn_rate = 0.1
        self.discount = 0.99
    def refresh(self):
        cum_r = 0
        total = len(self.history)
        i = total - 2
        while i >= 0:
            r = self.history[i+1]['r']
            s = self.history[i]['s']
            a = self.history[i]['a']
            cum_r = self.discount * cum_r + r
            self.states[s][a][0] += cum_r
            self.states[s][a][1] += 1
            i -= 1
        self.history = []
    def act(self, x, r, exploit=0.9) -> int:
        if np.random.randint(100) / 100.0 > exploit:
            return np.random.randint(5)
        s = self._get_state(x)
        if s in self.states:
            q = []
            for i in range(5):
                try:
                    q.append(self.states[s][i][0] / self.states[s][i][1])
                except:
                    q.append(0)
            a = np.argmax(q)
        else:
            state = [[0,0],[0,0],[0,0],[0,0],[0,0]]
            self.states[s] = state
            a = np.random.randint(5)
        self.history.append({'s': s, 'a': a, 'r': r})
        return a
    def _get_state(self, x):
        x = list(x)
        x[0] *= 1.2
        x[1] *= 1.2
        x[2] *= 1.2
        x[3] *= 1.2
        state = ' '.join(map(lambda x: str(int(x)), x))
        return state

class ModelStatic(object):
    def __init__(self):
        self.state = 0
    def refresh(self):
        pass
    def act(self, x, r, exploit=None) -> int:
        # x is (en.x, en.y, pl.x, pl.y, ld, lf)
        a = self._act(x)
        if np.random.randint(40) == 0:
            if self.state == 0:
                self.state = 1
            else:
                self.state = 0
        if self.state == 1: # Retreat
            if a == S:
                a = N
            elif a == N:
                a = S
            elif a == E:
                a = W
            elif a == W:
                a = E
            elif a == FIRE:
                a = np.random.randint(4)
        return a
    def _act(self, x):
        en_x = x[0]
        en_y = x[1]
        pl_x = x[2]
        pl_y = x[3]
        ld = x[4]
        lf = x[5]
        if np.abs(pl_x - en_x) < 0.7:
            if en_y > pl_y:
                if ld == N:
                    return FIRE
                else:
                    return N
            else:
                if ld == S:
                    return FIRE
                else:
                    return S
        if np.abs(pl_y - en_y) < 0.7:
            if en_x > pl_x:
                if ld == E:
                    return FIRE
                else:
                    return E
            else:
                if ld == W:
                    return FIRE
                else:
                    return W
        if np.abs(pl_x - en_x) < np.abs(pl_y - en_y): # diff in x is lesser of diff in y
            if pl_x < en_x:
                return E
            else:
                return W
        else:
            if pl_y < en_y:
                return N
            else:
                return S

def main():
    step = 5000 # The demonstration will be shown each 5000 steps.
    winrate = [0,0,0]
    modelA = ModelMC()
    modelB = ModelStatic() # You can change this to `modelB = ModelTD()`
    # To make both players controlled by RL
    counter = 0
    while True:
        modelA.refresh()
        modelB.refresh()
        world = BattleWorld()
        result = None
        while result is None:
            result = world.passive_move()
            if counter % step == 0:
                world.show(str(counter))
            xA, rA = world.observe(1)
            xB, rB = world.observe(2)
            exploit = 0.9 # Change of this value will affect only training games.
            if counter % step == 0:
                exploit = 1.0 # Change of this value will affect only demo games.
            aA = modelA.act(xA, rA, exploit=exploit)
            aB = modelB.act(xB, rB, exploit=exploit)
            world.act(1, aA)
            world.act(2, aB)
        winrate[result] += 1
        if counter != 0 and counter % step == 0:
            print("None: ", winrate[0] / step)
            print("MC One: ", winrate[1] / step)
            print("ML Two: ", winrate[2] / step, flush=True)
            winrate = [0,0,0]
        if counter >= 50000: # After the game 50000 the demonstration will be shown each 500 steps
            step = 500
        if counter % 10000 == 0: # Save the states in the pickled format so you could use them afterwards.
            with open("modelMC_vsML_{}.pickle".format(counter), "wb") as fw:
                pickle.dump(modelA.states, fw)
            # with open("modelTD_{}.pickle".format(counter), "wb") as fw:
            #     pickle.dump(modelB.states, fw)
        counter += 1

main()