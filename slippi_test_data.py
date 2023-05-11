import numpy as np
from slippi import Game
def snapshot_gen(filename):
    curr_game = Game(filename)
    ports_in_use = []
    for port in range(len(curr_game.metadata.players)):
        if curr_game.metadata.players[port] != None:
            ports_in_use.append(port)
    #players_info = curr_game.start.players
    #player_0_data = [players_info[ports_in_use[0]].character, players_info[ports_in_use[0]].stocks]
    #player_1_data = [players_info[ports_in_use[1]].character, players_info[ports_in_use[1]].stocks] <- dont actually want to do it this way


    num_frames = len(curr_game.frames)
    #print(curr_game.frames[0]) <- doesn't work, frame objects don't have __str__ methods

    for i in range(0, num_frames, 180): # steps in 180 frames = 3 seconds
        curr_frame = curr_game.frames[i]
        player0_port = ports_in_use[0]
        player1_port = ports_in_use[1]
        player0data = curr_frame.ports[player0_port].leader.post
        player1data = curr_frame.ports[player1_port].leader.post
        '''
        ^--- this data will look like
                -character (enumeration)
                -state (actionstate, also an enumeration) (is this worth including????)
                -position (Position object)
                -direction (enumeration) either -1 or 1 (which i think is fine to leave as is ?) 
                -damage (float)
                -shield (size of shield) (do we need this??? <- yes, in case state is shielding)
                -stocks
                -state_age
                -flags (state flags (stuff like shield, hit_lag, hit_stun, etc.))
                -hit_stun
                -airborne
                -jumps



        '''


snapshot_gen('sample_data/Game_20200814T200309.slp')

#stats of a player will always come in an np_array that takes form:
#    [stage, character, damage, stocks, direction, jumps, grounded, position, shield, .etc.]

def state_to_onehot(action):
    vec = np.zeros(383)
    vec[action] = 1
    return vec

#NOTE : make sure to use InGameCharacter enumeration to obtain the character (found under frame.leader.post.character) - it has a different enumeration than CSSCharacter (found in game.start.port)
def char_to_onehot(char):
    vec = np.zeros(26)
    #nana is given character 11 - but is unplayable, so useful to represent that in our vector
    #technically, there are also enums > 26, but they are non-pickable characters (i.e. giga-bowser, wireframe-man, etc.)
    if char >= 11:
        char -= 1
    vec[char] = 1
    return vec

#stage is stored as enum - but only stages that matter to us are 2, 3, 8, 28, 31, 32)
def stage_to_onehot(stage):
    vec = np.zeros(6)
    conv = {2: 0, 3: 1, 8:2, 28:3, 31:4, 32: 5}
    vec[conv[stage]] = 1
    return vec
def stateflag_to_onehot(state):
    conv = {16: 0, 1024: 1, 2048: 2, 8192: 3, 8388608: 4, 33554432: 5, 67108864: 6, 536870912: 7, 34359738368: 8,68719476736: 9,  274877906944: 10, 549755813888: 11}
    vec = np.zeros(12)
    vec[conv[state]] = 1
    return vec

def calculate_advantage(player0_prestats, player0_poststats, player1_prestats, player1_poststats): #returns 0 for a player 0 advantage, 1 for player 1 advantage
    pass