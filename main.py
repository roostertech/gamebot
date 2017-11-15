import numpy as np
import time
import random
from com.dtmilano.android.viewclient import ViewClient
from recognizer import Recognizer
from PIL import Image


def get_cell_center(board_box, cell_size, x, y):
    return (board_box[0] + x * cell_size + cell_size / 2, board_box[1] + y * cell_size + cell_size / 2)


def get_map_cell_center(x, y):
    return get_cell_center(map_box, map_cell_size, x, y)


def get_battle_cell_center(x, y):
    return get_cell_center(board_box, cell_size, x, y)


board_dict = {0: 'Empty ', 1: 'Mob ', 2: 'Player '}

board_box = (21, 340, 1059, 1724)
board_size = (6, 8)
cell_size = 173

map_size = (9, 12)
map_box = (0, 180, 1080, 1626)
map_cell_size = 120
#
# device, serialno = ViewClient.connectToDeviceOrExit(verbose=True, serialno='34eda071')
# print(serialno)


# device.takeSnapshot().save('training/map.png', 'PNG')


def print_board(board):
    print "-----------"
    for line in board.transpose():
        for elem in line:
            print board_dict[elem] + ' ',
        print
    print "-----------"

def send_battle_drag(cell_A, cell_B, randomFactor=10):
    x1 = cell_A[0] + random.randrange(-randomFactor, randomFactor)
    y1 = cell_A[1] + random.randrange(-randomFactor, randomFactor)
    x2 = cell_B[0] + random.randrange(-randomFactor, randomFactor)
    y2 = cell_B[1] + random.randrange(-randomFactor, randomFactor)

    print "Dragging from cells : (%d, %d) to (%d, %d)" % (x1, y1, x2, y2)
    device.drag((x1, y1), (x2, y2), 100, 10)


battle_recognizer = Recognizer("battle")
battle_recognizer.load('training/battle/player', 2)
battle_recognizer.load('training/battle/enemy', 1)
battle_recognizer.load('training/battle/boss', 1)
battle_recognizer.load('training/battle/empty', 0)
battle_recognizer.train()

map_recognizer = Recognizer("map")
map_recognizer.load('training/map/player', 2)
map_recognizer.load('training/map/boss', 1)
map_recognizer.load('training/map/empty', 0)
map_recognizer.train()

scene_dict = {0: 'Map', 1: 'Battle', 2: 'Load', 3: 'Loot', 4: 'Score'}

scene_recognizer = Recognizer("scene")
scene_recognizer.load('training/scenes/map', 0)
scene_recognizer.load('training/scenes/battle', 1)
scene_recognizer.load('training/scenes/load', 2)
scene_recognizer.load('training/scenes/loot', 3)
scene_recognizer.load('training/scenes/score', 4)
scene_recognizer.train()


# {'width': 1440, 'density': 3.0, 'orientation': 0, 'height': 2560}
# print(device.getDisplayInfo())


def parseBoard(rawImage, board_box, board_size, cell_size, recognizer):
    board_image = rawImage.crop(board_box)
    board_image.save('out.png')

    return_board = np.zeros((board_size[0], board_size[1]), dtype=np.int32)

    for x in range(0, board_size[0]):
        for y in range(0, board_size[1]):
            cell_box = (x * cell_size, y * cell_size, (x + 1) * cell_size, (y + 1) * cell_size)
            cell_image = board_image.crop(cell_box)
            return_board[x, y] = recognizer.predict(cell_image)
            # cell_image.save('cell_%d_%d.png' % (x, y))

    return return_board


def parseBattleBoard(rawImage):
    return parseBoard(rawImage, board_box, board_size, cell_size, battle_recognizer)

def parseMapBoard(rawImage):
    return parseBoard(rawImage, map_box, map_size, map_cell_size, map_recognizer)


# print_board(parseBattleBoard(Image.open('training/scenes/battle/snap1.png')))
print_board(parseMapBoard(Image.open('training/scenes/map/map.png')))

# send_drag(get_cell_center(1,1), get_cell_center(2,2))
# send_drag(get_cell_center(1,0), get_cell_center(2,0))
# for x in range(0,10):
#     send_battle_drag(get_cell_center(1,1), get_cell_center(3,3))

# device.

# device.drag()

# 1050x1400
# 1080x1920c
# 1.333333333333333
# 337 down = 449

# 340
# 21 - 173 * 6 - 21
#  340 1,384 - 184
# img = Image.open('training/start.png')
# img = Image.open('training/scenes/map/map3.png')
# parseMap(img)

# cell_image.save('cell_' + str(x) + '_' + str(y) + '.png')
# print 'cell_' + str(x) + '_' + str(y) + ' : ' + str()
