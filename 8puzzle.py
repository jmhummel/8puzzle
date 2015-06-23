#!/usr/bin/env python

# Jeremy Hummel
# 02/11/14
# CMPSCI 383

import sys
import re
import copy

class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class InputError(Error):
    """Exception raised for errors in the input.

    Attributes:
        expr -- input expression in which the error occurred
        msg  -- explanation of the error
    """

    def __init__(self, msg):
        self.msg = msg
        
class EightPuzzle():
    def __init__(self, str):
        pttn = re.compile("(\d)\s(\d)\s(\d)\s(\d)\s(\d)\s(\d)\s(\d)\s(\d)\s(\d)")
        result = pttn.match(str)
        if result is not None:
            s = result.groups()
            self.state = [[int(s[0]), int(s[1]), int(s[2])],
                          [int(s[3]), int(s[4]), int(s[5])],
                          [int(s[6]), int(s[7]), int(s[8])]]
        else:
            raise InputError("Improperly formatted 8-puzzle")

    def __str__(self):
        s = ''
        for i in range (0,3):
            for j in range(0,3):
                s += str(self.state[i][j]) + ' '
        return s

#def __str__(self):
#    s = ''
#    for i in range (0,3):
#        for j in range (0,3):
#            s += str(self.state[i][j]) + ' '
#        s += '\n'
#    return s

    def __eq__(self, other):
        if type(other) is type(self):
            return self.__dict__ == other.__dict__
        return False
        
    def __ne__(self, other):
        return not self.__eq__(other)
        
    def __hash__(self):
        uid = 0
        mult = 1
        for i in range(0,3):
            for j in range(0,3):
                uid += self.state[i][j] * mult
                mult *= 9
        return uid
                
    def tile_switches_remaining(self, goal):
        sum = 0
        for i in range(0, 3):
            for j in range(0, 3):
                if (self.state[i][j] != goal.state[i][j]):
                    sum += 1
        return sum
        
    def manhatten_distance(self, goal):
        sum = 0
        for i in range(0, 3):
            for j in range(0, 3):
                tile = self.state[i][j]
                for m in range(0, 3):
                    for n in range(0, 3):
                        if tile == goal.state[m][n]:
                            sum += abs(i-m) + abs(j+n)
        return sum
        
    def neighbors(self):
        list = []
        idx = self.get_blank_index()
        x = idx[0]
        y = idx[1]
        if x > 0:
            r = copy.deepcopy(self)
            r.state[y][x] = r.state[y][x-1]
            r.state[y][x-1] = 0
            list.append((r,'r'))
        if x < 2:
            l = copy.deepcopy(self)
            l.state[y][x] = l.state[y][x+1]
            l.state[y][x+1] = 0
            list.append((l,'l'))
        if y > 0:
            d = copy.deepcopy(self)
            d.state[y][x] = d.state[y-1][x]
            d.state[y-1][x] = 0
            list.append((d,'d'))
        if y < 2:
            u = copy.deepcopy(self)
            u.state[y][x] = u.state[y+1][x]
            u.state[y+1][x] = 0
            list.append((u,'u'))
        return list
        
    def get_blank_index(self):
        for i in range(0, 3):
            for j in range(0, 3):
                if self.state[i][j] == 0:
                    x = j
                    y = i
        return (x,y)
    
    def a_star(self, goal, heuristic, output):
        closed_set = set()      
        open_set = set([self])
        came_from = {}
        
        g_score = {self : 0}
        f_score = {self : g_score[self] + heuristic(self,goal)}
        
        while (len(open_set) != 0):
#            print len(open_set),len(closed_set)
            current = None
            for node in open_set:
                if current is None or f_score[node] < f_score[current]:
                    current = node
            if current == goal:
                return output(self, came_from, current)
                
            open_set.remove(current)
            closed_set.add(current)
#             print "Closed set:"
#             for p in closed_set:
#                 print p
            for n in current.neighbors():
                neighbor = n[0]
#                 print "Neighbor:\n",neighbor
                if neighbor in closed_set:
#                     print "Current:\n",current
#                     print "Neighbor:\n",neighbor
                    continue
                tentative_g_score = g_score[current] + 1
                
                if neighbor not in open_set or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = (current, n[1])
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = g_score[neighbor] + heuristic(neighbor,goal)
                    if neighbor not in open_set:
                        open_set.add(neighbor)

        return "nil"
    
    def action_sequence(self, came_from, current_node):
        goal = current_node
        return self.action_sequence_helper(came_from, current_node, goal)
    
    def action_sequence_helper(self, came_from, current_node, goal):
        delineator = ","
        if current_node == goal:
            delineator = ""
        if current_node in came_from:
            p = self.action_sequence_helper(came_from, came_from[current_node][0], goal)
            p += came_from[current_node][1] + delineator
            return p
        else:
            return "" 
    
    def state_transition(self, came_from, current_node):
        goal = current_node
        return self.state_transition_helper(came_from, current_node, goal)
             
    def state_transition_helper(self, came_from, current_node, goal):
        delineator = "\n"
        if current_node == goal:
            delineator = ""
        if current_node in came_from:
            p = self.state_transition_helper(came_from, came_from[current_node][0], goal)
            p += str(current_node) + delineator
            return p
        else:
            return str(current_node) + delineator


# function reconstruct_path(came_from, current_node)
#     if current_node in came_from
#         p := reconstruct_path(came_from, came_from[current_node])
#         return (p + current_node)
#     else
#         return current_node

def main():
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        raise InputError("Not enough arguments")
    h = int(sys.argv[1])
    if h == 1:
        heuristic = EightPuzzle.manhatten_distance
    elif h == 2:
        heuristic = EightPuzzle.tile_switches_remaining
    else:
        raise InputError("Heuristic argument must be 1 or 2")
    if len(sys.argv) == 3:
        o = int(sys.argv[2])
        if o == 0:
            output = EightPuzzle.action_sequence
        elif o == 1:
            output = EightPuzzle.state_transition
        else:
            raise InputError("Output argument must be 0 or 1")
    else:
        output = EightPuzzle.action_sequence
    
    input_i = sys.stdin.readline()
    input_f = sys.stdin.readline()
    
    initial = EightPuzzle(input_i)
    goal = EightPuzzle(input_f)
    
    print initial.a_star(goal, heuristic, output)
#     for keys,values in result.items():
#         print "key:\n",(keys)
#         print "value:\n",(values)
#     return 0
    

    
#     print "\n"
#     if isinstance(result, list):
#         for s in result:
#             print s
#         print len(result)-1,"moves"
#     else:
#         print result

    

    
if __name__ == '__main__':
    main()
