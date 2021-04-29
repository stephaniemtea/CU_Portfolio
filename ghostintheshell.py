import sys
import math

factory_count = int(input())  # the number of factories
link_count = int(input())  # the number of links between factories
all_fd_list = []
for i in range(link_count):
    # save a list of 3 integers, where the first two are factories, and the third is the distance between them 
    factory_distance = [int(j) for j in input().split()] 
    all_fd_list.append(factory_distance) #add all factory distances to big list
all_fd_list = sorted(all_fd_list, key = lambda x:x[2])

#DEBUGGING
#print("Factory Distances: ", file=sys.stderr)
#print(all_fd_list, file=sys.stderr)
onFirstTurn = True

#GAME LOOP
while True: # loop runs until game stops
    #SAVE GAME STATE USING A DICTIONARY
    game_state = {}
    
    #GATHERING DATA TO USE LATER 
    entity_count = int(input())  # the number of entities for one round (e.g. factories and troops)
    for i in range(entity_count):   # loops for however many game objects there are
        entity_id, entity_type, arg_1, arg_2, arg_3, arg_4, arg_5 = input().split()
        entity_id = int(entity_id)
        arg_1 = int(arg_1)
        arg_2 = int(arg_2)
        arg_3 = int(arg_3)
        arg_4 = int(arg_4)
        arg_5 = int(arg_5)
        
        #STORE INFORMATION FOR EACH TURN
        game_state[entity_id] = [entity_type, arg_1, arg_2, arg_3, arg_4, arg_5] #the key = entity id, values = entity type + arguments 
    
    def determine_num_cyborgs(gs, hf, df):
        cyborg_num = 2
        start_temp_info = gs[hf] #['FACTORY', 1, 5, 2, 0, 0]    
        dest_temp_info = gs[df]  #['FACTORY', 0, 3, 2, 0, 0]
        if start_temp_info[2] > dest_temp_info[2]: #if the starting factory has more cyborgs than the destination factory
            cyborg_num = dest_temp_info[2] + 1  #then send the number of cyborgs at the destination factory plus one (so you can capture it)
            gs[hf][2] -= cyborg_num #remove the number of cyborgs you sent from the starting factory entity in the game state dictionary
            return cyborg_num
        elif start_temp_info[2] >= 6:   #else if the starting factory has 6 or more cyborgs, send 2 cyborgs
            gs[hf][2] -= cyborg_num     #remove the cyborgs from the starting factory entity in the gs dictionary
            return cyborg_num
        elif dest_temp_info[1] == -1:   #if the destination factory is an enemy factory
            if start_temp_info[2] > dest_temp_info[2] + 5:  #if the starting factory has more cyborgs than the destination
                cyborg_num = dest_temp_info[2]+5    #send the number of cyborgs at the enemy factory plus 5 so you can stay strong and can defend yourself
                gs[hf][2] -= cyborg_num #remove the number of cyborgs from the starting factory entityin the game state dictionary
            return cyborg_num
        return 0
        
    def determine_send_bomb(gs, hf, df):    #send bomb based on the home factory and destination
        start_temp_info = gs[hf]    ##['FACTORY', 1, 5, 1, 0, 0] 
        dest_temp_info = gs[df] #['FACTORY', 0, 5, 0, 0, 0] 
        if start_temp_info[3] > 0 or start_temp_info[3] < 1:    #if the home factory produces 0 or 1 cyborgs
            if dest_temp_info[2] > 5: #if the destination factory has 5 or more cyborgs
                return True #then send a bomb
        return False
  
    #DEBUGGING
    #print("Game State Dictionary", file=sys.stderr)
    #print(game_state, file=sys.stderr)
    
    #MAKING A SMART MOVE
    #LOOP THROUGH GATHERED DATA
    fact_start = [] 
    fact_dest = []
    enemy_factories = []
    high_prod = []
    bomb_starting_dest = -1
    #FIND NEUTRAL FACTORY
    for eid, e_info in game_state.items():
        if e_info[0] == "FACTORY" and e_info[1] == 1 and e_info[2]>30 or e_info[2]>20 or e_info[2]>10: 
            #FACTORIES THAT ARE MINE + HAVE A LOT OF CYBORGS BEING PRODUCED
            high_prod.append(eid)
      #SENDING TROOPS TO NEUTRAL FACTORIES
        if e_info[0] == "FACTORY" and e_info[1]==0: 
            #find all neutral factories
            fact_dest.append(eid)
    #FIND STARTING FACTORY 
        if e_info[0] == "FACTORY" and e_info[1] == 1 and e_info[2]>0: 
            #only find factories that have a cyborg count greater than 0
            fact_start.append(eid)
    #FIND THE ENEMY FACTORY WITH THE FEWEST CYBORGS
        if e_info[0] == 'FACTORY' and e_info[1] == -1 and e_info[2]> 0: #find all enemy factories that produce cyborgs
            enemy_factories.append([eid, e_info[2]])   #add the factory id and cyborg production to list
        enemy_factories = sorted(enemy_factories, key = lambda x: x[1])  #sort list by smallest number of cyborgs
    
        if e_info[0] == "BOMB" and e_info[1] == -1:
            bomb_starting_dest = e_info[2]
            
    #BUILD TURN ACTION
    action_list = []
    # move from my factory to neutral factory 
    if onFirstTurn == True:
        action_list.append(f"BOMB {fact_start[0]} {enemy_factories[0][0]}")
        onFirstTurn = False
    if len(fact_dest) > 0 and len(fact_start) > 0:  #if there are neutral factories to go to and you own at least one factory
        for home_factory in fact_start: #for every factory you own
            for neutral_factory in fact_dest:   #for every factory that is neutral
                cyborg_to_send = determine_num_cyborgs(game_state, home_factory, neutral_factory)   #send cyborgs based on the destination
                action_list.append(f"MOVE {home_factory} {neutral_factory} {cyborg_to_send}")  
    elif len(high_prod)>0 and len(fact_dest) > 0 and len(fact_start)>0: #keep going to neutral factories if you have high producing factories
        for hp in high_prod:
            for nf in fact_dest:
                cyborg_to_send = determine_num_cyborgs(game_state, hp, nf)   #send cyborgs based on the destination
                action_list.append(f"MOVE {hp} {nf} {cyborg_to_send}") 
    # move from my factory to enemy factory with the lowest amount of cyborgs    
    elif bomb_starting_dest !=-1 and len(fact_start)>0:
        for hf in fact_start:
            for ef in enemy_factories:
                send_bomb = determine_send_bomb(game_state, hf, ef[0])
                if send_bomb == True:
                    action_list.append(f"BOMB {fact_start[0]} {bomb_starting_dest}")
    elif len(fact_start)>0 and len(enemy_factories)>0:   #start attacking enemy factories
        for hf in fact_start:
            for ef in enemy_factories:
                cyborg_to_send = determine_num_cyborgs(game_state, hf, ef[0])
                action_list.append(f"MOVE {hf} {ef[0]} {cyborg_to_send}")  
    else: 
        if len(action_list) == 0:   #if there are no actions, wait for troops to replenish and for maximum rounds to be reached
            action_list.append("WAIT")

    #WRITE AN ACTION USING PRINT
    # To debug: print("Debug messages...", file=sys.stderr)


    # Any valid action, such as "WAIT" or "MOVE source destination cyborgs"
    print(";".join(action_list))
    
    
