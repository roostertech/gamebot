import numpy as np
import time
from com.dtmilano.android.viewclient import ViewClient
from recognizer import GridRecognizer
from PIL import Image



def get_cell_center(x, y):
    return (board_box[0] + x * cell_size + cell_size / 2, board_box[1] + y * cell_size + cell_size / 2)

board_box = (21,340,1059,1724)
board_size = (6,8)
game_board = np.zeros((board_size[0], board_size[1]), dtype=np.int32)
board_dict = {0: 'Empty ', 1: 'Mob ', 2: 'Player '}
cell_size = 173

cell_locations = []
for column in range(0,board_size[0]):
    for row in range(0,board_size[1]):
        cell_locations.append(get_cell_center(column, row))

for index in range(0, 48):
    print str(index) + ' ' + str(cell_locations[index])

# device, serialno = ViewClient.connectToDeviceOrExit(verbose=True, serialno='34eda071')
# print(serialno)
# device.takeSnapshot().save('training/map.png', 'PNG')


def takeSnapShot():
    device.takeSnapshot().save('training/snap1.png', 'PNG')


def print_board(board):
    for line in board.transpose():
        for elem in line:
            print board_dict[elem] + ' ',
        print


def send_drag(cell_A,cell_B):
    print "Dragging from cells : " + str(cell_A) + " to " + str(cell_B)
    device.drag((cell_A[0], cell_A[1]), (cell_B[0], cell_B[1]), 100, 10)
    time.sleep(1)

recognizer = GridRecognizer()
recognizer.train()

    # {'width': 1440, 'density': 3.0, 'orientation': 0, 'height': 2560}
# print(device.getDisplayInfo())

# device.drag()

# 1050x1400
# 1080x1920c
# 1.333333333333333
# 337 down = 449

# 340
# 21 - 173 * 6 - 21
#  340 1,384 - 184
# img = Image.open('training/start.png')
img = Image.open('training/start.png')

board_image = img.crop(board_box)
board_image.save('out.png')

for x in range(0, board_size[0]):
    for y in range(0, board_size[1]):
        cell_box = (x * cell_size, y * cell_size, (x + 1) * cell_size, (y + 1) * cell_size)
        cell_image = board_image.crop(cell_box)
        game_board[x, y] = recognizer.predict(cell_image)
        # cell_image.save('cell_' + str(x) + '_' + str(y) + '.png')
        # print 'cell_' + str(x) + '_' + str(y) + ' : ' + str()

print_board(game_board)

# Find player to move
# if (game_board[2,4] == 2) :
