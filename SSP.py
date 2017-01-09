from random import randint, sample, shuffle
from itertools import chain, combinations
from time import time
from timeit import timeit
from pprint import pprint

class SSP:
    """
    object representing an instance of a subset sum problem
    """
    def __init__(self, S=[], t=0):
        """
        takes two arguments, S being the language and t being the target
        """
        self.S = S
        self.t = t
        self.n = len(S)
        #
        self.decision = False
        self.total    = 0
        self.selected = []

    def __repr__(self):
        return "SSP instance: S="+str(self.S)+"\tt="+str(self.t)
    
    def random_instance(self, n, bitlength=10):
        """
        generate a random instance where the max integer size is 2**bitlength-1 and length of n
        """
        if n < max_n_bit_number:
            #self.S = sorted( [ randint(0,max_n_bit_number) for i in range(n) ] , reverse=True)
            new = randint(0, max_n_bit_number)
            S = []
            while len(S) < n:
                if new not in S:
                    S.append(new)
                new = randint(0, max_n_bit_number)
            self.S = sorted(S, reverse=True)
            self.t = randint(0,n*max_n_bit_number)
            self.n = len( self.S )
        else:
            raise ValueError("bitlength too short for {} size set".format(n))

    def random_yes_instance(self, n, bitlength=10):
        """
        generate SSP instance where we know t equals a subset
        """
        self.random_instance(n, bitlength)
        self.t = sum( sample(self.S, randint(0,n)) )

    def random_no_instance(self, n, bitlength=10):
        """
        generate SSP instance that we know will be the worst case
        """
        self.random_instance(n, bitlength)
        self.t = sum(self.S) + 1

    def try_at_random(self):
        """
        randomly attempt to match t to a sub set
        """
        candidate = []
        total = 0
        while total != self.t:
            candidate = sample(self.S, randint(0,self.n))
            total     = sum(candidate)
            print( "Trying: ", candidate, ", sum:", total )

    def power_set(self):
        """
        return list of all possible combinations of elements in S
        """
        p_set = []
        s_len = 2**self.n - 1
        max_bits = len(bin(s_len)) - 2

        for i in range(0, s_len + 1):
            padded_bits = format(i, '0%sb' % max_bits)
            p_set.append([i for i, s in zip(self.S, padded_bits) if int(s)])

        return p_set

    def exhaustive(self):
        """
        exhaustively search the super set of S for t
        """
        S = self.power_set()
        for e in S:
            if sum(e) == self.t:
                print("t found in {}".format(e))
                return True
        return False

    def greedy(self, rand=False):
        total = []
        copy = self.S.copy()

        if rand:
            shuffle(copy)

        for x in copy:
            if x > self.t:
                copy.remove(x)

        while copy and sum(total) < self.t:
            for i in copy:
                if i + sum(total) <= self.t:
                    total.append(i)
                    copy.remove(i)
                    break
                else:
                    copy.remove(i)
        return (self.t - sum(total), total)

    def local_search(self, subset):
        diff = self.t - sum(subset)
        copy = subset.copy()
        for x in self.S:
            for i in subset:
                if x - i < 0:
                    pass
                elif x - i < diff:
                    copy.remove(i)
                    copy.append(x)
                    return copy
        return copy

    def distance(self, subset):
        s = sum(subset)
        return self.t - s

    def grasp(self):
        best = []
        for iteration in range(1000):
            greedy = self.greedy(True)
            grasp = self.local_search(greedy[1])
            if self.distance(grasp) < self.distance(best):
                print("GRASP: found better solution: {}".format(grasp))
                best = grasp
            if sum(best) == self.t:
                print("GRASP: completed in {} iterations".format(iteration + 1))
                return best
        print("GRASP: found insufficient subset, {} off target".format(self.distance(best)))
        return best

    def dynamic(self):
        """
        return True or False to whether a subset sums to the target via dynamic programming
        """
        it = 0
        L = {0}
        for x in self.S:
            it += len(L)
            L = L.union({i + x for i in L if (i + x) <= self.t})
            if self.t in L:
                print("dynamic: completed in {} iterations".format(it))
                return self.t in L
        print("dynamic: failed in {} iterations".format(it))
        return False

if __name__ == "__main__":
    instance = SSP()
    times = {}
    for i in range(50, 1001, 50):
        n = 1
        print("--- random {} elements yes instance ---".format(i))
        instance.random_yes_instance(i, 15)
        print(instance)
        dyn_time = timeit(instance.dynamic, number=n)
        grasp_time = timeit(instance.grasp, number=n)
        times[i] = (round(dyn_time, 5), round(grasp_time, 5))
        print("Dynamic: {} seconds".format(dyn_time))
        print("GRASP: {} seconds".format(grasp_time))

    print("\tDynamic   GRASP")
    pprint(times)



# print( instance )
# print(instance.greedy())
# print(instance.dynamic())

# print("exhaustive search completed in {} seconds".format(timeit(instance.exhaustive_search, number=1)))
#instance.try_at_random()
# for i in range(2, 23):
#     instance.random_yes_instance(i)
#     print(i)
#     print("exhaustive search completed in {} seconds".format(timeit(instance.exhaustive, number=1)))
