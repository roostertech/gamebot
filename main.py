import numpy as np
import time
import random
from com.dtmilano.android.viewclient import ViewClient
from recognizer import Recognizer
from PIL import Image

# Translate from screenshot coor 1080x1920 to device coor 1440, 2560
def translate_coor(x, y):
    return int(float(x) / 1080 * 1440), int(float(y) / 1920 * 2560)

def get_cell_center(board_box, cell_size, x, y):
    return board_box[0] + x * cell_size + cell_size / 2, board_box[1] + y * cell_size + cell_size / 2

def get_map_cell_center(x, y):
    return get_cell_center(map_box, map_cell_size, x, y)


def get_battle_cell_center(x, y):
    return get_cell_center(board_box, cell_size, x, y)


board_dict = {0: 'Empty', 1: 'Mob ', 2: 'Player'}

board_box = (21, 340, 1059, 1724)
board_size = (6, 8)
cell_size = 173

map_size = (9, 12)
map_box = (0, 180, 1080, 1626)
map_cell_size = 120
map_action_button = (334, 415)



def print_board(board):
    print "-----------\n"
    index = 0
    for line in board:
        print '%2d: ' % index,
        index += 1
        for elem in line:
            print board_dict[elem] + '\t',
        print ' '
    print "-----------\n"

def find_bottom_player(board):
    x = y = indexx = indexy = 0

    for line in board:
        for elem in line:
            if elem == 2:
                x = indexx
                y = indexy
            indexx += 1
        indexx = 0
        indexy += 1
    print 'Player at %d %d' % (x, y)

    return (x, y)


def find_players_column(board):
    column = 0
    max_count = 0
    bottom_column = 0

    curr_column = 0
    for line in board.transpose():
        player = 0
        rowindex = 0
        lastFoundPlayerAt = 0
        for elem in line:
            if elem == 2:
                player += 1
                lastFoundPlayerAt = rowindex
            rowindex += 1

        if player > max_count:
            column = curr_column
            max_count = player
            bottom_column = lastFoundPlayerAt
        curr_column += 1

    print "Found column at ", column, bottom_column
    return (column, bottom_column)

device, serialno = ViewClient.connectToDeviceOrExit(verbose=True, serialno='34eda071')
print(serialno)
print device.getDisplayInfo()
# exit(0)

def send_drag(cell_A, cell_B, randomFactor=5):
    x1 = cell_A[0] + random.randrange(-randomFactor, randomFactor)
    y1 = cell_A[1] + random.randrange(-randomFactor, randomFactor)
    x2 = cell_B[0] + random.randrange(-randomFactor, randomFactor)
    y2 = cell_B[1] + random.randrange(-randomFactor, randomFactor)

    print "Dragging from cells : (%d, %d) to (%d, %d)" % (x1, y1, x2, y2)
    device.drag((x1, y1), (x2, y2), 500, 10)

def battle_drag(x1, y1, x2, y2):
    start = get_battle_cell_center(x1, y1)
    end = get_battle_cell_center(x2, y2)
    send_drag(start, end)

def battle_drag_left(x, y):
    battle_drag(x, y, x - 1, y)
def battle_drag_right(x, y):
    battle_drag(x, y, x + 1, y)
def battle_drag_down(x, y):
    battle_drag(x, y, x, y + 1)
def battle_drag_up(x, y):
    battle_drag(x, y, x, y - 1)

def map_drag_left(x, y):
    start = get_map_cell_center(x, y)
    end = get_map_cell_center(x - 1, y)
    send_drag(start, end)
def map_drag_right(x, y):
    start = get_map_cell_center(x, y)
    end = get_map_cell_center(x + 1, y)
    send_drag(start, end)
def send_tap(x, y, randomFactor=10):
    x = x + random.randrange(-randomFactor, randomFactor)
    y = y + random.randrange(-randomFactor, randomFactor)
    print "Touch %d, %d" % (x, y)
    device.touch(x, y)

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

scene_dict = {0: 'Map', 1: 'Battle', 2: 'Load', 3: 'Loot', 4: 'Score', 5: 'Map-Action'}

scene_recognizer = Recognizer("scene")
scene_recognizer.load('training/scenes/map', 0)
scene_recognizer.load('training/scenes/battle', 1)
scene_recognizer.load('training/scenes/load', 2)
scene_recognizer.load('training/scenes/loot', 3)
scene_recognizer.load('training/scenes/score', 4)
scene_recognizer.load('training/scenes/map-action', 5)
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
            # cell_image.save('tmp/cell_%d_%d.png' % (x, y))

    return return_board.transpose()


def parseBattleBoard(rawImage):
    return parseBoard(rawImage, board_box, board_size, cell_size, battle_recognizer)

def parseMapBoard(rawImage):
    return parseBoard(rawImage, map_box, map_size, map_cell_size, map_recognizer)


# print_board(parseBattleBoard(Image.open('training/scenes/battle/snap1.png')))
# print_board(parseMapBoard(Image.open('training/scenes/map/map.png')))

# send_drag(get_cell_center(1,1), get_cell_center(2,2))
# send_drag(get_cell_center(1,0), get_cell_center(2,0))
# for x in range(0,10):
#     send_battle_drag(get_cell_center(1,1), get_cell_center(3,3))

# device.

#
# device.takeSnapshot(reconnect=True).save('training/scenes/map/battle5.png', 'PNG')
while (1):
    # snapshot = Image.open('training/scenes/battle/battle1.png')
    snapshot = device.takeSnapshot(reconnect=True)
    scene = scene_recognizer.predict(snapshot)
    print 'Scene ', scene
    if scene == 5:
        print 'Map Action'
        send_tap(map_action_button[0], map_action_button[1])
        time.sleep(5)
    elif scene == 0:
        map_board = parseMapBoard(snapshot)
        (player_x, player_y) = find_bottom_player(map_board)
        if player_x == 5:
            map_drag_left(player_x, player_y)
            time.sleep(3)
        elif player_x == 4:
            map_drag_right(player_x, player_y)
            time.sleep(3)
        else:
            print "?????"

    elif scene == 1:
        print 'Battle'
        battle_board = parseBattleBoard(snapshot)
        (player_x, player_y) = find_bottom_player(battle_board)
        (column, bottom_column) = find_players_column(battle_board)

        if player_x != column:
            battle_drag(player_x, player_y, column, bottom_column+1)
            time.sleep(10)
        elif player_x == column:
            above_player = battle_board[player_y - 1][player_x]
            if above_player == 2:
                battle_drag_down(player_x, player_y)
                time.sleep(10)
            else:
                battle_drag_up(player_x, player_y)
                time.sleep(10)
        else:
            print "?????"
    elif scene == 4 or scene == 3:
        # tap anywhere
        send_tap(random.randrange(100, 500), random.randrange(200, 600), 2)
        time.sleep(5)
    else:
        print "Not yet implemented"
    time.sleep(1)

# snapshot = device.takeSnapshot().save('tmp/snap.png', 'PNG')
# snapshot = device.takeSnapshot()
# snapshot.save('training/scenes/map-action1.png', 'PNG')
# snapshot.save('tmp/snap.png', 'PNG')

# snapshot = Image.open('tmp/snap.png')
# map_board = parseMapBoard(snapshot)
# print_board(map_board)
# (playerx, playery) = find_bottom_player(map_board)
#
# send_drag(get_map_cell_center(playerx, playery), get_map_cell_center(playerx+1, playery))

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
