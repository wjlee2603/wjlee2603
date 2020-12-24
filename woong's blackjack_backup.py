#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 11:46:18 2020

@author: taylorlee
"""

import numpy as np
import random



#define functions
def decks (number_decks,card_decks):
    new_deck = []
    for i in range(number_decks):
        for j in range(4):
            new_deck.extend(card_decks)
    random.shuffle(new_deck)
    return new_deck

def get_ace_values(temp_list):
    sum_array = np.zeros((2**len(temp_list), len(temp_list)))
    # This loop gets the permutations
    for i in range(len(temp_list)):
        n = len(temp_list) - i
        half_len = int(2**n * 0.5)
        for rep in range(int(sum_array.shape[0]/half_len/2)):
            sum_array[rep*2**n : rep*2**n+half_len, i] = 1
            sum_array[rep*2**n+half_len : rep*2**n+half_len*2, i] = 11
    # Only return values that are valid (<=21)
    return list(set([int(s) for s in np.sum(sum_array, axis=1) if s<=21]))
    
def ace_values (num_aces):
    temp_list=[]
    for i in range (num_aces):
        temp_list.append([1,11])
    return get_ace_values(temp_list)

def soft_sum(hand):
    aces=0
    total=0
    for card in hand:
        if card != 'A':
            total+=card
        else:
            aces+= 1
    ace_value_list=ace_values(aces)
    return min(ace_value_list)+total


def sum_hand(hand):
    aces=0
    total=0
    for card in hand:
        if card != 'A':
            total+=card
        else:
            aces+= 1
    ace_value_list=ace_values(aces)
    final_totals=[i+total for i in ace_value_list if i+total<=21]
    if final_totals == []:
        return min(ace_value_list) + total
    else:
        return max(final_totals)


  

#main program
stacks=10000
players=1
number_decks=8
card_decks=['A',2,3,4,5,6,7,8,9,10,10,10,10]
dealer_card_track=[]
player_hands_track=[]
player_score_track=[]
dealer_hands_track=[]
doubledown_track=[]
surrender_track=[]




# simulation starts, dealer starts dealing cards
for stack in range(stacks):
    dealer_cards = decks (number_decks, card_decks)
    blackjack = set(['A',10])
    while len(dealer_cards) > 20:
        
        player_score = np.zeros((1,players))
        dealer_hand = []
        player_hands = [[] for player in range(players)]
        doubledown=[0 for player in range(players)]
        surrender=[0 for player in range(players)]
        # Deal FIRST card
        for player, hand in enumerate(player_hands):
            player_hands[player].append(dealer_cards.pop(0))
        dealer_hand.append(dealer_cards.pop(0))
        # Dealer's Card
        # Deal SECOND card
        for player, hand in enumerate(player_hands):
            player_hands[player].append(dealer_cards.pop(0))
        # Dealer's Card
        dealer_hand.append(dealer_cards.pop(0))

 # Dealer checks for 21
        if set(dealer_hand) == blackjack:
            for player in range(players):
                if set(player_hands[player]) != blackjack:
                    player_score[0,player] = -1
                else:
                    player_score[0,player] = 0
        else:
                for player in range(players):
                    if set(player_hands[player]) == blackjack:
                        player_score[0,player] = 1
                    #Surrender chance!
                    elif sum_hand(player_hands[player])==16 and (dealer_hand[0]==9 or dealer_hand[0]==10 or dealer_hand[0]=='A'):
                        surrender=1
                        player_score[0,player]=-0.5
                        break      
                    elif sum_hand(player_hands[player])==15 and dealer_hand[0]==10:
                        surrender=1
                        player_score[0,player]=-0.5
                        break
                    #Double down chance!
                    elif sum_hand(player_hands[player])==11:
                        player_hands[player].append(dealer_cards.pop(0))
                        doubledown[player]=1
                    elif sum_hand(player_hands[player])==10 and (dealer_hand[0]!=10 or dealer_hand[0]!='A'):
                        player_hands[player].append(dealer_cards.pop(0))
                        doubledown[player]=1
                    elif sum_hand(player_hands[player])==9 and (dealer_hand[0]==6 or dealer_hand[0]==5 or dealer_hand[0]==4 or dealer_hand[0]==3):
                        player_hands[player].append(dealer_cards.pop(0))
                        doubledown[player]=1
                    
                    else:
                        while sum_hand(player_hands[player])<=16:
                            if dealer_hand[0]=='A':
                                player_hands[player].append(dealer_cards.pop(0))
                            elif dealer_hand[0]>=7:
                                player_hands[player].append(dealer_cards.pop(0))
                            elif (dealer_hand[0]<=3 and sum_hand(player_hands[player])==12):
                                    player_hands[player].append(dealer_cards.pop(0))
                            elif sum_hand(player_hands[player])<=11:
                                player_hands[player].append(dealer_cards.pop(0))
                            else:
                                break 
                            if sum_hand(player_hands[player]) > 21:
                                    player_score[0,player] = -1
                                    break   
# Soft Total        
                        while sum_hand(player_hands[player])<=19:
                            if player_hands[player].count('A')>=1:
                                if soft_sum(player_hands[player])==9 and dealer_hand[0]==6:
                                    player_hands[player].append(dealer_cards.pop(0))
                                elif soft_sum(player_hands[player])==8 and dealer_hand[0]=='A':
                                    player_hands[player].append(dealer_cards.pop(0))
                                elif soft_sum(player_hands[player])==8 and (dealer_hand[0]<=6 or dealer_hand[0]>=9):
                                    player_hands[player].append(dealer_cards.pop(0))
                                elif soft_sum(player_hands[player])<=7:
                                    player_hands[player].append(dealer_cards.pop(0))
                                else:
                                    break
                            else:
                                break
                                
# Dealer's turn - hits based on the rules
                while sum_hand(dealer_hand) <17:
                    dealer_hand.append(dealer_cards.pop(0))
                    if player_score[0,player]==-0.5:
                        break
# Determine who won, if no one busted
                    elif sum_hand(dealer_hand)>21:
                        for player in range(players):
                            if doubledown[player]==1:
                                player_score[0,player]=2
                            elif player_score[0,player]!=-1:
                                player_score[0,player]=1
                    else:
                        for player in range(players):
                            if doubledown[player]==1 and sum_hand(dealer_hand)>sum_hand(player_hands[player]):
                                player_score[0,player]=-2
                            elif doubledown[player]==1 and sum_hand(dealer_hand)<sum_hand(player_hands[player]):
                                if sum_hand(player_hands[player])<=21:
                                    player_score[0,player]=2
                                else:
                                    player_score[0,player]=0
                            elif sum_hand(dealer_hand)>sum_hand(player_hands[player]):
                                player_score[0,player]=-1
                            elif sum_hand(dealer_hand)<sum_hand(player_hands[player]):
                                if sum_hand(player_hands[player])<=21:
                                    player_score[0,player]=1
                            else:
                                player_score[0,player]=0
                                
        doubledown_track.append(doubledown)
        surrender_track.append(surrender)
        dealer_card_track.append(dealer_hand[0])
        dealer_hands_track.append(dealer_hand)
        player_hands_track.append(player_hands)
        player_score_track.append(list(player_score[0]))

dealer_card_track
dealer_hands_track
player_hands_track                   
player_score_track
doubledown_track.count([1])
surrender_track
surrender_track.count(1)
score=[i[0] for i in player_score_track]

loss=0
win=0
tie=0
for i in score:
    if i== -1.0:
        loss += 1
    elif i== 0.0:
        tie += 1
    elif i==-0.5:
        loss +=0.5
    elif i== 2.0:
        win +=2
    else:
        win+=1

win_rate = win/(loss+win)
win_rate                            
                        
                        
                    
            

            
