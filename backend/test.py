# A program to illustrate Zobrist Hashing Algorithm
# python code implementation
import random

# mt19937 mt(01234567);

# Generates a Random number from 0 to 2^64-1
def randomInt():
	min = 0
	max = pow(2, 64)
	return random.randint(min, max)

# This function associates each piece with
# a number
def indexOf(piece):
	if (piece=='P'):
		return 0
	elif (piece=='N'):
		return 1
	elif (piece=='B'):
		return 2
	elif (piece=='R'):
		return 3
	elif (piece=='Q'):
		return 4
	elif (piece=='K'):
		return 5
	elif (piece=='p'):
		return 6
	elif (piece=='n'):
		return 7
	elif (piece=='b'):
		return 8
	elif (piece=='r'):
		return 9
	elif (piece=='q'):
		return 10
	elif (piece=='k'):
		return 11
	else:
		return -1

# Initializes the table
def initTable():
	# 8x8x12 array
	ZobristTable = [[[randomInt() for k in range(12)] for j in range(8)] for i in range(8)]
	return ZobristTable

# Computes the hash value of a given board
def computeHash(board, ZobristTable):
	h = 0
	for i in range(8):
		for j in range(8):
			if (board[i][j] != '-'):
				piece = indexOf(board[i][j])
				h ^= ZobristTable[i][j][piece]
	return h

# Main Function
# Uppercase letters are white pieces
# Lowercase letters are black pieces
board = [
	"---K----",
	"-R----Q-",
	"--------",
	"-P----p-",
	"-----p--",
	"--------",
	"p---b--q",
	"----n--k"
]

ZobristTable = initTable()

hashValue = computeHash(board, ZobristTable)
print("The hash value is	 : " + str(hashValue))

#Move the white king to the left
piece = board[0][3]

board[0] = list(board[0])
board[0][3] = '-'
board[0] = ''.join(board[0])

hashValue ^= ZobristTable[0][3][indexOf(piece)]

board[0] = list(board[0])
board[0][2] = piece
board[0] = ''.join(board[0])
hashValue ^= ZobristTable[0][2][indexOf(piece)]


print("The new hash value is : " + str(hashValue))

# Undo the white king move
piece = board[0][2]

board[0] = list(board[0])
board[0][2] = '-'
board[0] = ''.join(board[0])

hashValue ^= ZobristTable[0][2][indexOf(piece)]

board[0] = list(board[0])
board[0][3] = piece
board[0] = ''.join(board[0])
hashValue ^= ZobristTable[0][3][indexOf(piece)]

print("The old hash value is : " + str(hashValue))
