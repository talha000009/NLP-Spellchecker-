import numpy as np


class Levenshtein:
    """returns the cost of edit distance"""
    def __init__(self, insertion_cost, deletion_cost, substitution_cost):
        self.insertion_cost = insertion_cost
        self.deletion_cost = deletion_cost
        self.substitution_cost = substitution_cost  # Levenshtein version of edit distance (substitution cost = 2)
        self.distance = np.zeros((0, 0))

    def _init_distance(self, source, target):
        """create graph of edit distance between source word and target word"""
        self.distance = np.zeros((source, target))
        for x in range(source):
            self.distance[x, 0] = x
        for y in range(target):
            self.distance[0, y] = y

        return self.distance

    def _insertion(self, char):
        return self.insertion_cost

    def _deletion(self, char):
        return self.deletion_cost

    def _substitution(self, source, target):
        if source == target:
            return 0
        return self.substitution_cost

    def minimum_edit_distance(self, source, target):
        n = len(target) + 1
        m = len(source) + 1
        distance = self._init_distance(m, n)
        for j in range(1, n):
            for i in range(1, m):
                distance[i, j] = min(distance[i - 1, j] + self._deletion(target[j - 1]),  # delete
                                     distance[i, j - 1] + self._insertion(target[j - 1]),  # insert
                                     distance[i - 1, j - 1] + self._substitution(source[i - 1], target[j - 1])
                                     )

        print("source:", source, "target", target, "edit distance:", distance[m-1, n-1])
        return distance[m - 1, n - 1]
