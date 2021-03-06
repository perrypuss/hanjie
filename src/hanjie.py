# parse board
# calculate definites and possibilities
# loop, eliminating possibilities, until consistent
import itertools
import sys
from copy import copy, deepcopy

def partitions(n, k):
    for c in itertools.combinations(range(n+k-1), k-1):
        yield [b-a-1 for a, b in zip((-1,)+c, c+(n+k-1,))]

def read_clues(infile):
    across = []
    down = []
    
    for line in open(infile):
        if line.strip()=="across":
            active = across
        elif line.strip()=="down":
            active = down
        else:
            line = line.strip().split()
            active.append(map(int, line))
    
    return Hanjie_board(across,down)

class Hanjie_board(object):
    def __init__(self, across, down):
    
        self.across = tuple(across)
        self.down = tuple(down)

        self.height = len(across)
        self.width = len(down)

        self.board = [['-']*self.width for i in range(self.height)]
        self.board_old = deepcopy(self.board)
    
        print self.height, self.width
        
    def clues_to_poss_interleaved(self):
        long_side = max(self.height, self.width)
        
        self.across_possibilities = []
        self.down_possibilities = []
        
        for i in range(0,long_side):
            print i,'|',
            if i<self.height:
                item = tuple(self.across[i])
                possibles = self.calc_possibles(item, self.width)
                self.across_possibilities.append(possibles)
                self.update_across(i)
                print len(possibles), sum(self.across[i]), '|',
                
            if i<self.width:
                item = tuple(self.down[i])
                possibles = self.calc_possibles(item, self.height)
                self.down_possibilities.append(possibles)
                self.update_down(i)    
                print len(possibles), sum(self.down[i]),'|'
                       

    def update_grid_across(self, line, i):
        for j in range(self.width):
            if self.board[i][j] == "-" and line[j] != "-":
                self.board[i][j] = line[j]
        
    def update_grid_down(self, line, i):
        for j in range(self.height):
            if self.board[j][i] == "-" and line[j] != "-":
                self.board[j][i] = line[j]
    
    
    def calc_possibles(self, clue, length):
        possibles = []
        
        min_squares = len(clue) - 1
        extra_squares = length - min_squares - sum(clue)
        
        squares_dist = partitions(extra_squares, min_squares+2)
        
        for p in squares_dist:
            expanded_clue = [0] * (len(clue) * 2 + 1)
            expanded_clue[1::2] = clue
            expanded_clue[0::2] = p
            for i in range(2,len(expanded_clue)-1,2):
                expanded_clue[i] += 1
            new_possible = self.convert_clue_to_line(expanded_clue)
            possibles.append(new_possible)
        
        #print clue, len(possibles)
        return possibles
    
    def calc_definites(self, current, possibles):
        for item in possibles:
            current = self.compare_lines(current, item)
            
        return current
    
    def convert_clue_to_line(self,expanded_clue):
        hanjie_line = [] 
        for i in range(0, len(expanded_clue)):
            if i%2 == 0:
                hanjie_line.extend(u'\u2588'*expanded_clue[i])
            else:
                hanjie_line.extend(" "*expanded_clue[i])
        
        return hanjie_line
        
    def compare_lines(self, line1, line2):
        newline = []
        for i in range(len(line1)):
            if line1[i] == line2[i]:
                newline.append(line1[i])
            else:
                newline.append('-')
        return newline
        
    def update_across(self, i):
        for item in self.across_possibilities[i]:
            for j in range(self.width):
                if self.board[i][j] != '-' and self.board[i][j] != item[j]:
                    self.across_possibilities[i].remove(item)
                    break
        if len(self.across_possibilities[i]) == 1:
            newline = self.across_possibilities[i][0]
        else:
            newline = self.calc_definites(self.across_possibilities[i][0],self.across_possibilities[i][1:])
        self.update_grid_across(newline, i)

    def update_down(self, i):
        for item in self.down_possibilities[i]:
            for j in range(self.height):
                if self.board[j][i] != '-' and self.board[j][i] != item[j]:
                    self.down_possibilities[i].remove(item)
                    break
        if len(self.down_possibilities[i]) == 1:
            newline = self.down_possibilities[i][0]
        else:
            newline = self.calc_definites(self.down_possibilities[i][0],self.down_possibilities[i][1:])
        
        self.update_grid_down(newline, i)

            
    def solve(self):
        #if self.height == self.width:
        #   self.clues_to_possibilities()
        #else:
        #   self.clues_to_possibilities("across")
        #   self.clues_to_possibilities("down")
        self.clues_to_poss_interleaved()
        self.draw_board()
        
        done = False
        while not done:
            done = True
            for item in self.board:
                if '-' in item:
                    done = False
                    break
            
            board_current = deepcopy(self.board)
            
            long_side = max(self.height, self.width)
            
            for i in range(long_side):
                if i < self.height:
                    if len(self.across_possibilities[i]) > 1 and self.board_old[i]!=self.board[i]:
                        self.update_across(i)
                    print i, len(self.across_possibilities[i])

                if i< self.width:
                    board_changed = False
                    for j in range(self.height):
                        if self.board_old[j][i] != board_current[j][i]:
                            board_changed = True
                            break
                    if len(self.down_possibilities[i]) > 1:# and board_changed:
                        self.update_down(i)
                    print i, len(self.down_possibilities[i])
                    
            self.draw_board()
            
            self.board_old = deepcopy(board_current)
            
        self.draw_board()
    
    def draw_board(self):
        
        print "-"+''.join('-'*self.width)+"-"
        for item in self.board:
            print "|"+''.join(item)+"|"
        print "-"+''.join('-'*self.width)+"-"           

def main():
    #infile = "hanjie1.txt"
    infile = sys.argv[1]
    
    hanjie = read_clues(infile)
    hanjie.solve()
    
if __name__ == "__main__":
    main()