import random


class hexFlower:
    def __init__(self, states: dict[int, str], currentState=1):
        if not isinstance(states, dict):
            raise TypeError("states must be a dictionary")
        expectedKeys = set(range(1, 20))
        if set(states.keys()) != expectedKeys:
            raise ValueError("states keys must be integers from 1 to 19 inclusive")
        self.states = states
        self.currentState = currentState
        self.defaultState = currentState
        self.transitionDict = {
            1: {1: 3, 2: 4, 3: 1, 4: 6, 5: 2, 6: 5},
            2: {1: 5, 2: 1, 3: 17, 4: 11, 5: 4, 6: 7},
            3: {1: 6, 2: 9, 3: 18, 4: 1, 5: 5, 6: 8},
            4: {1: 7, 2: 2, 3: 14, 4: 16, 5: 1, 6: 9},
            5: {1: 8, 2: 3, 3: 1, 4: 2, 5: 7, 6: 10},
            6: {
                1: 1,
                2: 14,
                3: 16,
                4: 3,
                5: 8,
                6: 11,
            },
            7: {1: 10, 2: 5, 3: 2, 4: 4, 5: 9, 6: 12},
            8: {1: 11, 2: 6, 3: 3, 4: 5, 5: 10, 6: 13},
            9: {1: 12, 2: 7, 3: 4, 4: 18, 5: 3, 6: 14},
            10: {1: 13, 2: 8, 3: 5, 4: 7, 5: 12, 6: 15},
            11: {1: 2, 2: 17, 3: 6, 4: 8, 5: 13, 6: 16},
            12: {1: 15, 2: 10, 3: 7, 4: 9, 5: 14, 6: 17},
            13: {1: 16, 2: 11, 3: 8, 4: 10, 5: 15, 6: 18},
            14: {1: 17, 2: 12, 3: 9, 4: 19, 5: 6, 6: 4},
            15: {1: 18, 2: 13, 3: 10, 4: 12, 5: 17, 6: 19},
            16: {1: 4, 2: 19, 3: 11, 4: 13, 5: 18, 6: 11},
            17: {1: 19, 2: 15, 3: 12, 4: 14, 5: 11, 6: 2},
            18: {1: 9, 2: 16, 3: 13, 4: 15, 5: 19, 6: 3},
            19: {1: 19, 2: 18, 3: 15, 4: 17, 5: 19, 6: 19},
        }

    def transition(self, direction: int):
        ## Check whether direction is valid
        if direction not in range(0, 7):
            raise ValueError("direction must be an integer from 0 to 6 inclusive")
        ## Change current state
        if direction == 0:
            return
        else:
            self.currentState = self.transitionDict[self.currentState][direction]
            return

    def random_transition(self):
        ## Generate two random integers between 1 and 6 inclusive
        d6 = random.randint(1, 6)
        d8 = random.randint(1, 8)
        sum = d6 + d8
        if sum <= 3:
            direction = 1
        elif sum <= 5:
            direction = 2
        elif sum <= 7:
            direction = 3
        elif sum <= 8:
            direction = 0
        elif sum <= 10:
            direction = 4
        elif sum <= 12:
            direction = 5
        elif sum <= 14:
            direction = 6
        else:
            raise ValueError("Invalid sum")

        self.transition(direction)
        return direction

    def get_current_state(self):
        return self.states[self.currentState]

    def get_current_cell(self):
        return self.currentState

    def reset(self):
        self.currentState = self.defaultState

    def set_states(self, newStates, defaultState=1):
        """
        Update the hex flower with a new set of states

        Args:
            newStates (dict): Dictionary mapping cell IDs (1-19) to state names
        """
        if not isinstance(newStates, dict):
            raise TypeError("states must be a dictionary")

        expectedKeys = set(range(1, 20))
        if set(newStates.keys()) != expectedKeys:
            raise ValueError("states keys must be integers from 1 to 19 inclusive")

        self.states = newStates
        self.defaultState = defaultState
        self.reset()

    def set_current_cell(self, cellId):
        """
        Set the current cell to a specific cell ID

        Args:
            cellId (int): The cell ID to set as current (1-19)
        """
        if not isinstance(cellId, int):
            try:
                cellId = int(cellId)
            except (TypeError, ValueError):
                raise TypeError("cell_id must be an integer")

        if cellId < 1 or cellId > 19:
            raise ValueError("cell_id must be between 1 and 19 inclusive")

        self.currentState = cellId
        return self.get_current_state()
