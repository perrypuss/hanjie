# parse board
# calculate definites and possibilities
# loop, eliminating possibilities, until consistent
import itertools
import sys

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
	
	def clues_to_possibilities(self, direction="both"):
		clues_to_lines = {}
		definites = {}
		
		if direction == "across":
			clues = self.across
			length = self.width
		elif direction == "down":
			clues = self.down
			length = self.height
		else: #gain some efficiency if hanjie is square
			clues = self.across + self.down
			length = self.height
		
		for item in clues:
			item = tuple(item)
			if item not in clues_to_lines:
				possibles = self.calc_possibles(item, length)
				clues_to_lines[item] = possibles
				if len(possibles) == 1:
					definites[item] = possibles[0]
				else:
					definites[item] = self.calc_definites(possibles[0],possibles[1:])
		
		if direction == "down" or direction == "both":
			self.down_possibilities = []
			for i in range(self.width):
				item = tuple(self.down[i])
				new_poss = list(clues_to_lines[item])
				self.down_possibilities.append(new_poss)
				self.update_grid_down(definites[item], i)
		
		if direction == "across" or direction == "both":
			self.across_possibilities = []
			for i in range(self.height):
				item = tuple(self.across[i])
				new_poss = list(clues_to_lines[item])
				self.across_possibilities.append(new_poss)
				self.update_grid_across(definites[item], i)
			

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
		
		print clue, len(possibles)
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
		if self.height == self.width:
			self.clues_to_possibilities()
		else:
			self.clues_to_possibilities("across")
			self.clues_to_possibilities("down")
		self.draw_board()
		
		done = False
		while not done:
			done = True
			for item in self.board:
				if '-' in item:
					done = False
					break
			for i in range(self.height):
				if len(self.across_possibilities[i]) > 1:
					self.update_across(i)
			
			for i in range(self.width):
				if len(self.down_possibilities[i]) > 1:
					self.update_down(i)
						
			self.draw_board()
			
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