print 'Brick Game emu.'
game = 0
while not game in [1, 2]: game = input('Chose the game (1-Racing1, 2-Racing2): ')

if game == 1:
    mode = 0
    while not mode in [1, 2]: mode = input('Choce 1 for pve or 2 for simulation: ')
    from Racing1_first_atempt.Racing1 import startGame as startGame1
    startGame1(mode)
elif game == 2:
    mode = 0
    while not mode in [1, 2, 3]: mode = input('Choce 1 for pve, 2 for demonstrationor or 3 for training: ')
    from Racing2_XOX_method_used.Racing2 import startGame as startGame2
    startGame2(mode)
