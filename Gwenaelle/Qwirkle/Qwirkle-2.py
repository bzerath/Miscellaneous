#!/usr/bin/env python
# coding: utf-8

# In[2]:


import termcolor
import pprint
import random

scores=[0,0,0]
#Need to put exception handling
#Need to do customised version with menu
#need to do trading tiles part

FORMES = {
    "croix": "X",
    "losange": "♦",
    "cercle": "●",
    "carré": "■",
    "étoile": "☼",
    "trèfle": "♣"
}

COULEURS = {
    "rouge": "red",
    "violet": "magenta",
    "bleu": "blue",
    "gris": "white",  # pas d'orange en console
    "vert": "green",
    "jaune": "yellow",
}

dico_example_2 = {(0, 0): ('losange', 'violet'),
                  (1, 0): ('croix', 'violet'),
                  (2, 0): ('cercle', 'violet'),
                  (-1, 0): ('étoile', 'violet'),
                  (2, -1): ('cercle', 'gris'),
                  (0, 1): ('losange', 'vert'),
                  (-1, 1): ('étoile', 'vert'),
                  (0, -1): ('losange', 'bleu'),
                  (0, 2): ('losange', 'jaune'),
                  (-1, 2): ('étoile', 'jaune')
       
       }

NOMBRE_DE_JOUEURS = 3
NOMBRE_DE_CARTE_PAR_MAIN = 6

NOMBRE_DE_TUILES_IDENTIQUES = 3

COULEUR = "couleur"
FORME = "forme"


def render_hand(hand, sep="\t"):
    output = []
    for carte in hand:
        try:
            forme = FORMES[carte[0]]
            couleur = COULEURS[carte[1]]
            output.append(termcolor.colored(forme, couleur))
        except TypeError:
            output.append(termcolor.colored(" ", None))
    return sep.join(output)


def extract_bigger_categories(categories):
    maximum = categories[0]
    for i in range(len(categories)):
        if categories[i][1] > maximum[1]:
            maximum = categories[i]
    return maximum


def get_bigger_set_of_cards(hand):
    color_sets = {color: set() for color in COULEURS}
    formes_sets = {forme: set() for forme in FORMES}

    for forme, couleur in hand:
        color_sets[couleur].add((forme, couleur))
        formes_sets[forme].add((forme, couleur))

    # à partir du dictionnaire color_sets -> une liste de tuples [(couleur, nombre de cartes de cette couleur), ...]
    colors_count = []
    for color in color_sets:
        tuple_temp = (color, len(color_sets[color]))
        colors_count.append(tuple_temp)
    formes_count = []
    for forme in formes_sets:
        tuple_temp = (forme, len(formes_sets[forme]))
        formes_count.append(tuple_temp)
    most_found_color = extract_bigger_categories(colors_count)
    most_found_forme = extract_bigger_categories(formes_count)

    if most_found_color[1] >= most_found_forme[1]:
        return COULEUR, most_found_color
    else:
        return FORME, most_found_forme


def get_first_player(joueurs: dict):
    # for joueur in joueurs:
    #     print(joueur, "\t", render_hand(joueurs[joueur]))
    #     print(get_bigger_set_of_cards(joueurs[joueur]))
    joueurs_sets = {}
    for joueur in joueurs:
        joueurs_sets[joueur] = get_bigger_set_of_cards(joueurs[joueur])
    #print(joueurs_sets)----> to see everybody maximum set
    print(joueurs_sets)
    maximum = (list(joueurs_sets.keys())[0], joueurs_sets[list(joueurs_sets.keys())[0]])
    for joueur in joueurs_sets:
        number = joueurs_sets[joueur][1][1]
        if number > maximum[1][1][1]:
            maximum = (joueur, joueurs_sets[joueur])

    return maximum

#To check horizontal/vertical line is not interupted
def adjacent_checks(position,dico_example_2,attribute):
    scale_x_n=(0,-1)
    scale_y_p=(-1,0)
    scale_x_p=(0,1)
    scale_y_n=(1,0)
    result_1=tuple(p+q for p, q in zip(position,scale_x_n ))
    result_2=tuple(p+q for p, q in zip(position,scale_y_p ))
    result_3=tuple(p+q for p, q in zip(position,scale_x_p ))
    result_4=tuple(p+q for p, q in zip(position,scale_y_n ))
    check_adj=False
    for key in dico_example_2:
        if (key==result_1) or (key==result_2) or (key==result_3) or (key==result_4):
            check_adj=True
            break
        else:
            check_adj=False
    
    return check_adj
  

#function to check whether each row/column has same shapes or colours, validation check
#Check forward in x direction
def is_shape_col_valid_x(x,y,attribute,max_adj_col,max_adj_line):
    valid=True
    shape=attribute[0]
    colour=attribute[1]
    while matrix_output[y][x+1]!= None:
        temp_att=matrix_output[y][x+1]
        temp_form=temp_att[0]
        temp_colour=temp_att[1] 
        if (shape==temp_form) or (colour==temp_colour):
            valid=True
        else:
            valid=False
            break

        x=x+1
        if x==max_adj_col:
            break
                
    return valid

#check backwards in x direction
def is_x_shape_colour_valid(x,y,attribute):
    valid=True
    shape=attribute[0]
    colour=attribute[1]   
    while matrix_output[y][x-1] != None:
        temp_att=matrix_output[y][x-1]
        temp_form=temp_att[0]
        temp_colour=temp_att[1] 
        if (shape==temp_form) or (colour==temp_colour):
            valid=True
        else:
            valid=False
            break
        x=x-1
        if x==0:
            break

    return valid

#check in upwards direction
def is_shape_col_valid_y(x,y,attribute):
    
    valid=True
    shape=attribute[0]
    colour=attribute[1]

    while matrix_output[y-1][x] != None:
        temp_att=matrix_output[y-1][x]
        temp_form=temp_att[0]
        temp_colour=temp_att[1] 
        if (shape==temp_form) or (colour==temp_colour):
            valid=True
        else:
            valid=False
            break
        y=y-1
        if y== 0:
            break
            
    return valid

#check in downwards direction
def y_is_shape_col_valid(x,y,attribute,max_adj_line):
    valid=True
    shape=attribute[0]
    colour=attribute[1]
    while matrix_output[y+1][x]!= None:
        temp_att=matrix_output[y+1][x]
        temp_form=temp_att[0]
        temp_colour=temp_att[1]
        if (shape==temp_form) or (colour==temp_colour):
            valid=True
        else:
            valid=False
            break
        
        y+=1
        if y==max_adj_line:
            break  
     
    print(valid)
    return valid    

#Validation whether in forward direction, there is no "doubles"
            
def for_x(x,y,attribute,max_adj_col,max_adj_line):
    check_for=True    
    while matrix_output[y][x+1]!= None:
        if matrix_output[y][x+1]==attribute:
            check_for=False
            break
        else:
            check_for=True

        x=x+1
        if x==max_adj_col:
            break
                
    return check_for

#Validation check whether there is no doubles in backwards direction
def back_x(x,y,attribute,max_adj_line):
    check_back=True       
    while matrix_output[y][x-1] != None:

        if matrix_output[y][x-1]== attribute:
            check_back= False
            break
        else:
            check_back=True
        x=x-1
        if x==0:
            break

    return check_back

#Validation check whether there is no doubles in upwards direction
def up_y(x,y,attribute, max_adj_col):
    check_up=True
    while matrix_output[y-1][x] != None:
        if matrix_output[y-1][x]== attribute:
            check_up= False
            break
        else:
            check_up=True
        y=y-1
        if y== 0:
            break
            
    return check_up


#Validation check whether there is no doubles in downwards direction
def down_y(x,y,attribute,max_adj_line,max_adj_col):
    check_down=True
    while matrix_output[y+1][x]!= None:
        if matrix_output[y+1][x]==attribute:
            check_down=False
            break
        else:
            check_down=True
        y+=1
        if y==max_adj_line:
            break  
            
    return check_down


def score_fx(x,y,attribute,max_adj_col,max_adj_line):
    
    if matrix_output[y][x+1] != None:
        score=1
    else:
        score=0
        
    qwirkle_c=0   
    while matrix_output[y][x+1]!= None:
        if matrix_output[y][x+1] != None:
            score+=1
        if score==6:
            score+=6
        x=x+1
        if x==max_adj_col:
            break
            
    score=score+(qwirkle_c*6)
    return score


def score_bx(x,y,attribute,max_adj_line):
    qwirkle_c=0
    if matrix_output[y][x-1] != None:
        score=1
    else:
        score=0
          
    while matrix_output[y][x-1] != None:

        if matrix_output[y][x-1] != None:
            score+=1
        x=x-1
        if score==6:
            qwirkle_c +=1

        if x==0:
            break  
                    
    score=score+(qwirkle_c*6)                
    return score

def score_u_y(x,y,attribute, max_adj_col):
    
    qwirkle_c=0
    if matrix_output[y-1][x] != None:
        score=1
    else:
        score=0

    while matrix_output[y-1][x] != None:
        if matrix_output[y-1][x]!= None:
            score+=1
        if score==6:
            qwirkle_c+=1
        y=y-1
        if y== 0:
            break

    score =score+ (qwirkle_c*6)
    return score


def score_d_y(x,y,attribute,max_adj_line,max_adj_col):
    qc=0
    if matrix_output[y+1][x] != None:
        score=1
    else:
        score=0

    while matrix_output[y+1][x]!= None:
        if matrix_output[y+1][x] !=None:
            score+=1
        if score==6:
            qc+=1
        y+=1
        if y==max_adj_line:
            break
                    
    score=score+(qc*6)         
    return score



def score(dico_example_2,position,attribute):
    list_of_numline = []
    list_of_numcol = []
    for key in dico_example_2:
        list_of_numline.append(key[0])
        list_of_numcol.append(key[1])

    min_line = min(list_of_numline)
    max_line = max(list_of_numline)
    min_col = min(list_of_numcol)
    max_col = max(list_of_numcol)
    y_min=abs(min_line)
    x_min=abs(min_col)
    max_adj_col=x_min+max_col
    min_adj_col=0
    max_adj_line=y_min+max_line
    min_adj_line=0
    
    position_temp=[]
    position_temp.append(y_min+position[0])
    position_temp.append(x_min+position[1])
    pos_tuple=(position_temp[0],position_temp[1])

    x=pos_tuple[1]
    y=pos_tuple[0]
    s1=0
    s2=0
    s3=0
    s4=0
     
    
    if x<0 and y==0:
        s1=score_fx(x,y,attribute,max_adj_col,max_adj_line)
    if y<0 and x==0:
        s4= score_d_y(x,y,attribute,max_adj_line,max_adj_col)

    if x>max_adj_col and y==0:
        s2=score_bx(x,y,attribute,max_adj_line)
    
   
    if y<0 and x==max_adj_col:
        s4=score_d_y(x,y,attribute,max_adj_line,max_adj_col)
        
    if x<0 and y==max_adj_line:
        s1=score_fx(x,y,attribute,max_adj_col,max_adj_line)
        
    
    if y>max_adj_line and x==0:
        s3=score_u_y(x,y,attribute, max_adj_col)
       
        
    if y>max_adj_line and x==max_adj_col:
        s3=score_u_y(x,y,attribute, max_adj_col)
        
    if x>max_adj_col and y==max_adj_line:
        s2=score_bx(x,y,attribute,max_adj_line)
        
    if x<0 and (y > 0 and y <max_adj_line) :
        s1=score_fx(x,y,attribute,max_adj_col,max_adj_line)
        
    if y<0 and (x>0 and x<max_adj_col ):
        s4=score_d_y(x,y,attribute,max_adj_line,max_adj_col)
        
    if x>max_adj_col and (y> 0 and y < max_adj_line ):
        s2=score_bx(x,y,attribute,max_adj_line)
        
    if y>max_adj_line and (x >0 and x <max_adj_col ):
        s3=score_u_y(x,y,attribute, max_adj_col)
        
        
    if x==0 and y==0:
        s1=score_fx(x,y,attribute,max_adj_col,max_adj_line)
        s4=score_d_y(x,y,attribute,max_adj_line,max_adj_col)
        
    if x==max_adj_col and y==0:
        s2=score_bx(x,y,attribute,max_adj_line)
        s4=score_d_y(x,y,attribute,max_adj_line,max_adj_col)
        
    if y==max_adj_line and x==0:
        s1=score_fx(x,y,attribute,max_adj_col,max_adj_line)
        s3=score_u_y(x,y,attribute, max_adj_col)
        
    
    if x==max_adj_col and y==max_adj_line:
        s2=score_bx(x,y,attribute,max_adj_line)
        s3=score_u_y(x,y,attribute, max_adj_col)

    if y==0 and (x > 0 and x < max_adj_col ):
        s2=score_bx(x,y,attribute,max_adj_line)
        s1=score_fx(x,y,attribute,max_adj_col,max_adj_line)
        s4=score_d_y(x,y,attribute,max_adj_line,max_adj_col)
        if s2 !=0 and s1 !=0 and s4 !=0:
            s2=s2-1
        
    if x==0 and (y >0 and y <max_adj_line):
        s1=score_fx(x,y,attribute,max_adj_col,max_adj_line)
        s3=score_u_y(x,y,attribute, max_adj_col)
        s4=score_d_y(x,y,attribute,max_adj_line,max_adj_col)
        if s3 !=0 and s1 !=0 and s4 !=0:
            s3=s3-1
    if y== max_adj_line and (x >0 and x < max_adj_col):
        s2=score_bx(x,y,attribute,max_adj_line)
        s1=score_fx(x,y,attribute,max_adj_col,max_adj_line)
        s3=score_u_y(x,y,attribute, max_adj_col)
        if s3 !=0 and s1 !=0 and s2 !=0:
            s3=s3-1
        
       
        
    if x== max_adj_col and (y >0 and y < max_adj_line):
        s2=score_bx(x,y,attribute,max_adj_line)
        s3=score_u_y(x,y,attribute, max_adj_col)
        s4=score_d_y(x,y,attribute,max_adj_line,max_adj_col)
        if s3 !=0 and s2 !=0 and s4 !=0:
            s3=s3-1
       
    if (x>=1 and x<= max_adj_col-1) and (y>=1 and y<=max_adj_line-1)  :
        s2=score_bx(x,y,attribute,max_adj_line)
        s1=score_fx(x,y,attribute,max_adj_col,max_adj_line)
        s3=score_u_y(x,y,attribute, max_adj_col)
        s4=score_d_y(x,y,attribute,max_adj_line,max_adj_col)
   
    scores=s1+s2+s3+s4
    return scores



#Check whether there is no doubles in col/row
def is_row_col_valid(dico_example_2,position,attribute):
    list_of_numline = []
    list_of_numcol = []
    for key in dico_example_2:
        list_of_numline.append(key[0])
        list_of_numcol.append(key[1])

    min_line = min(list_of_numline)
    max_line = max(list_of_numline)
    min_col = min(list_of_numcol)
    max_col = max(list_of_numcol)
    y_min=abs(min_line)
    x_min=abs(min_col)
    max_adj_col=x_min+max_col
    min_adj_col=0
    max_adj_line=y_min+max_line
    min_adj_line=0
    
    position_temp=[]
    position_temp.append(y_min+position[0])
    position_temp.append(x_min+position[1])
    pos_tuple=(position_temp[0],position_temp[1])

    x=pos_tuple[1]
    y=pos_tuple[0]
    
    c1=True
    c2=True
    c3=True
    c4=True
    sc1=True
    sc2=True
    sc3=True
    sc4=True
    
    
    
    if x<0 and y==0:
        c1=for_x(x,y,attribute,max_adj_col,max_adj_line)
        sc1=is_shape_col_valid_x(x,y,attribute,max_adj_col,max_adj_line)

    if y<0 and x==0:
        c4=down_y(x,y,attribute,max_adj_line,max_adj_col)
        sc4=y_is_shape_col_valid(x,y,attribute,max_adj_line)

    if x>max_adj_col and y==0:
        c2=back_x(x,y,attribute,max_adj_line)
        sc2=is_x_shape_colour_valid(x,y,attribute)
   
    if y<0 and x==max_adj_col:
        c4=down_y(x,y,attribute,max_adj_line,max_adj_col)
        sc4=y_is_shape_col_valid(x,y,attribute,max_adj_line)

        
    if x<0 and y==max_adj_line:
        c1=for_x(x,y,attribute,max_adj_col,max_adj_line)
        sc1=is_shape_col_valid_x(x,y,attribute,max_adj_col,max_adj_line)
    
    if y>max_adj_line and x==0:
        c3=up_y(x,y,attribute, max_adj_col)
        sc3=is_shape_col_valid_y(x,y,attribute)
        
    if y>max_adj_line and x==max_adj_col:
        c3=up_y(x,y,attribute, max_adj_col)
        sc3=is_shape_col_valid_y(x,y,attribute)
    
    if x>max_adj_col and y==max_adj_line:
        c2=back_x(x,y,attribute,max_adj_line)
        sc2=is_x_shape_colour_valid(x,y,attribute)
        
    if x<0 and (y > 0 and y <max_adj_line) :
        c1=for_x(x,y,attribute,max_adj_col,max_adj_line)
        sc1=is_shape_col_valid_x(x,y,attribute,max_adj_col,max_adj_line)
        
    if y<0 and (x>0 and x<max_adj_col ):
        c4=down_y(x,y,attribute,max_adj_line,max_adj_col)
        sc4=y_is_shape_col_valid(x,y,attribute,max_adj_line)

        
    if x>max_adj_col and (y> 0 and y < max_adj_line ):
        c2=back_x(x,y,attribute,max_adj_line)
        sc2=is_x_shape_colour_valid(x,y,attribute)
    
    if y>max_adj_line and (x >0 and x <max_adj_col ):
        c3=up_y(x,y,attribute, max_adj_col)
        sc3=is_shape_col_valid_y(x,y,attribute)
        
    if x==0 and y==0:
        c1=for_x(x,y,attribute,max_adj_col,max_adj_line)
        c4=down_y(x,y,attribute,max_adj_line,max_adj_col)
        sc4=y_is_shape_col_valid(x,y,attribute,max_adj_line)
        sc1=is_shape_col_valid_x(x,y,attribute,max_adj_col,max_adj_line)

        
    if x==max_adj_col and y==0:
        c4=down_y(x,y,attribute,max_adj_line,max_adj_col)
        c2=back_x(x,y,attribute,max_adj_line)
        sc4=y_is_shape_col_valid(x,y,attribute,max_adj_line)
        sc2=is_x_shape_colour_valid(x,y,attribute)
  
    if y==max_adj_line and x==0:
        c1=for_x(x,y,attribute,max_adj_col,max_adj_line)
        c3=up_y(x,y,attribute, max_adj_col)
        sc3=is_shape_col_valid_y(x,y,attribute)
        sc1=is_shape_col_valid_x(x,y,attribute,max_adj_col,max_adj_line)
    
    if x==max_adj_col and y==max_adj_line:
        c2=back_x(x,y,attribute,max_adj_line)
        c3=up_y(x,y,attribute, max_adj_col)
        sc3=is_shape_col_valid_y(x,y,attribute)
        sc2=is_x_shape_colour_valid(x,y,attribute)
        
    if y==0 and (x > 0 and x < max_adj_col ):
        c1=for_x(x,y,attribute,max_adj_col,max_adj_line)
        c2=back_x(x,y,attribute,max_adj_line)
        c4=down_y(x,y,attribute,max_adj_line,max_adj_col)
        sc4=y_is_shape_col_valid(x,y,attribute,max_adj_line)
        sc2=is_x_shape_colour_valid(x,y,attribute)
        sc1=is_shape_col_valid_x(x,y,attribute,max_adj_col,max_adj_line)

        
    if x==0 and (y >0 and y <max_adj_line):
        c1=for_x(x,y,attribute,max_adj_col,max_adj_line)
        c3=up_y(x,y,attribute, max_adj_col)
        c4=down_y(x,y,attribute,max_adj_line,max_adj_col)
        sc4=y_is_shape_col_valid(x,y,attribute,max_adj_line)
        sc3=is_shape_col_valid_y(x,y,attribute)
        sc1=is_shape_col_valid_x(x,y,attribute,max_adj_col,max_adj_line)
        
    if y== max_adj_line and (x >0 and x < max_adj_col):
        c1=for_x(x,y,attribute,max_adj_col,max_adj_line)
        c2=back_x(x,y,attribute,max_adj_line)
        c3=up_y(x,y,attribute, max_adj_col)
        sc3=is_shape_col_valid_y(x,y,attribute)
        sc2=is_x_shape_colour_valid(x,y,attribute)
        sc1=is_shape_col_valid_x(x,y,attribute,max_adj_col,max_adj_line)
    if x== max_adj_col and (y >0 and y < max_adj_line):
        c2=back_x(x,y,attribute,max_adj_line)
        c3=up_y(x,y,attribute, max_adj_col)
        c4=down_y(x,y,attribute,max_adj_line,max_adj_col)
        sc4=y_is_shape_col_valid(x,y,attribute,max_adj_line)
        sc3=is_shape_col_valid_y(x,y,attribute)
        sc2=is_x_shape_colour_valid(x,y,attribute)

       
    if (x>=1 and x<= max_adj_col-1) and (y>=1 and y<=max_adj_line-1)  :
        c1=for_x(x,y,attribute,max_adj_col,max_adj_line)
        c2=back_x(x,y,attribute,max_adj_line)
        c3=up_y(x,y,attribute, max_adj_col)
        c4=down_y(x,y,attribute,max_adj_line,max_adj_col)
        sc4=y_is_shape_col_valid(x,y,attribute,max_adj_line)
        sc3=is_shape_col_valid_y(x,y,attribute)
        sc2=is_x_shape_colour_valid(x,y,attribute)
        sc1=is_shape_col_valid_x(x,y,attribute,max_adj_col,max_adj_line)
    
    if c1==False or c2==False or c3==False or c4==False or sc1 == False or sc2 == False or sc3 == False or sc4==False :
        return False
    else:
        return True
        
    
    
#def shape_row_valid():
    
            
def pos_taken(position,dico_example_2):
    if position in dico_example_2:
        return True
    else:
        return False
        
    
def refill(joueurs,player_num):
    while len(paquet)>0 and len(joueurs[player_num])<6:
        joueurs[player_num].append(paquet.pop(0))
        

#def swapping(jouers,player_num): ---> trading of tiles yet to be done
    
        
        
        

        
def main():
    # Une tuile = un tuple <(forme, couleur)>
    # Préparer le jeu (108 cartes = 6 formes * 6 couleurs * 3)
    global paquet
    paquet = []
    for i in range(NOMBRE_DE_TUILES_IDENTIQUES):
        for forme in FORMES:
            for couleur in COULEURS:
                tuile = (forme, couleur)
                paquet.append(tuile)
    random.shuffle(paquet)
    random.shuffle(paquet)
    random.shuffle(paquet)

    # Piocher 6 cartes par personne
    joueurs = {}
    for i in range(NOMBRE_DE_JOUEURS):
        joueurs[i] = []
        for j in range(NOMBRE_DE_CARTE_PAR_MAIN):
            joueurs[i].append(paquet.pop(0))

    for joueur in joueurs:
        print(joueur, "\t", render_hand(joueurs[joueur]))
    
    
    first_player = get_first_player(joueurs)
    print("The player n°{player_num} will play first, because he has the biggest set ({category}), "
          "with {number} {type_}.".format(player_num=first_player[0],
                                          category=first_player[1][0],
                                          number=first_player[1][1][1],
                                          type_=first_player[1][1][0]))
    

    player_num=first_player[0]
    print(render_hand(joueurs[player_num]))
    dico_example_2={}
    position=(0,0)
    num_to_pop=int(input("Input number of the tile you want to play"))-1
    attribute=joueurs[player_num].pop(num_to_pop)
    dico_example_2[position]=attribute
    render_board(dico_example_2)
    scores[player_num]+=1
    print("The score for player n° :",player_num)
    print(scores[player_num])
    #print(joueurs[player_num]) the player number set of cards in terms of tuples
    #print(render_hand(joueurs[player_num])) display of the term coloured tuples
    choice_play_again=input("Do you want to play again(Y/N) ?")
    end_turn="N"
    fail=0
    if choice_play_again=="Y":
        while len(paquet)>0:
            end_turn="N"
            print("Player",player_num,"'s turn")
            print(render_hand(joueurs[player_num]))
            num_to_pop=int(input("Input number of the tile you want to play"))-1
            #test_list=render_hand(joueurs[player_num]).strip().split('\t')
            attribute=joueurs[player_num].pop(num_to_pop)
            position=eval(input("Input position where you want the tile to be place"))

            while pos_taken(position, dico_example_2) is True \
                    or adjacent_checks(position, dico_example_2, attribute) is False \
                    or is_row_col_valid(dico_example_2, position, attribute) is False:
                fail += 1
                joueurs[player_num].insert(num_to_pop,attribute)
                print(render_hand(joueurs[player_num]))
                if fail >= 1:
                    end_turn=input("Invalid position,Do you want to end turn (Y/N)?")
                    if end_turn =="Y":
                        fail=0
                        refill(joueurs,player_num)
                        if player_num==NOMBRE_DE_JOUEURS-1:
                            player_num=0

                        else:
                            player_num+=1

                        break

                    else:
                        print(" Enter tile and position again")
                        print("Player",player_num,"'s turn")
                        print(render_hand(joueurs[player_num]))
                        num_to_pop=int(input("Input number of the tile you want to play"))-1
                        attribute=joueurs[player_num].pop(num_to_pop)
                        position=eval(input("Input position where you want the tile to be place"))


            if end_turn != "Y":
                if len(paquet)==1:
                    scores[player_num]+=6
                scores[player_num]+=score(dico_example_2,position,attribute)
                dico_example_2[position]=attribute
                print(render_hand(joueurs[player_num]))
                render_board(dico_example_2)
                print("The score for player n° :",player_num)
                print(scores[player_num])
                end_turn=input("Do you want to end turn (Y/N)?")
                if end_turn == "Y":
                    refill(joueurs,player_num)
                    if player_num==NOMBRE_DE_JOUEURS-1:
                        player_num=0
                    else:
                        player_num+=1

                

                
def render_board(board: dict):
    # Analyser les coordonnées pour avoir la dimension de la future matrice
    list_of_numline = []
    list_of_numcol = []
    for key in board:
        list_of_numline.append(key[0])
        list_of_numcol.append(key[1])
   
    # Avoir les bornes de chaque dimension pour faire un range(min, max)
    # TODO: faire ça avec la méthode de recherche min/max vue en cours
    min_line = min(list_of_numline)
    max_line = max(list_of_numline)
    min_col = min(list_of_numcol)
    max_col = max(list_of_numcol)

    valeur_case_vide = None

    global matrix_output
    matrix_output=[]
    for numline in range(min_line, max_line+1):
        line_temp = []
        for numcol in range(min_col, max_col+1):
            line_temp.append(board.get((numline, numcol),
                                       valeur_case_vide))
        matrix_output.append(line_temp)

    line_of_numcols = ""
    for i in range(min_col, max_col+1):
        line_of_numcols += str(i) + "\t"
    print("\t", termcolor.colored(line_of_numcols, "grey"))
    list_of_numlines = list(range(min_line, max_line+1))
    for i, ligne in enumerate(matrix_output):
        print(termcolor.colored(list_of_numlines[i], "grey"),
              "\t", render_hand(ligne))


  
if __name__ == "__main__":
    main() 
    #               (y, x):     ( forme,     couleur)
    dico_example = {(0, 0):     ('losange', 'violet'),
                    (1, 0):     ('croix',   'violet'),
                    (2, 0):     ('cercle',  'violet'),
                    (-1, 0):    ('étoile',  'violet'),
                    (2, -1):    ('cercle',  'gris'),
                    (0, 1):     ('losange', 'vert'),
                    (-1, 1):    ('étoile',  'vert')}

    dico_example_3 = {(0, 0): ('losange', 'violet'),
                      (1, 0): ('croix', 'violet'),
                      (2, 0): ('cercle', 'violet'),
                      (-1, 0): ('étoile', 'violet'),
                      (2, -1): ('cercle', 'gris'),
                      (0, 1): ('losange', 'vert'),
                      (-1, 1): ('étoile', 'vert'),
                      (0, -1): ('losange', 'bleu'),
                      (0, 2): ('losange', 'jaune'),
                      (-1, 2): ('étoile', 'jaune'),
                      (-2, -2): ('croix', 'bleu')}
  
    #print(render_hand(joueurs[joueur[0]])) 
    # Poser les cartes du premier joueur sur le plateau, à la verticale, en partant de (0, 0)

    # Le premier joueur pioche les cartes qui lui manquent
    # -> On compte les points

    # Là on commence la boucle
    # Faire un while jusqu'à ce que la pioche soit vide, qui itère sur la liste des joueurs, en partant du joueur *suivant*
    # -> joueur choisit ses tuiles
    # -> vérifier que la sélection est correcte selon les règles du jeu
    # -> Si OK, passer au choix des coordonnées, sinon rester sur le choix des tuiles
    # -> joueur choisit les positions
    # -> vérifier que les positions sont correctes selon les règles du jeu
    #    --> autant de coordonnées que de cartes choisies
    #    --> coordonnées sont libres
    #    --> pas de doublon (ligne ou colonne ?)
    #    --> colonne ou ligne ininterrompue
    # -> si OK, ajouter les choix au dico board
    # -> On compte les points
    # -> joueur pioche
    # -> render_board
    # Passer au jouer *suivant*
    
    # etc...




    


# In[ ]:


a=(-1,0)
b=(1,0)
tuple(p+q for p, q in zip(a, b))


# In[2]:


a=('cercle','jaune')
b=('cercle','jaune')
if a==b:
    print(True)
    


# In[4]:


dico_example_2 = {(0, 0): ('losange', 'violet'),
                  (1, 0): ('croix', 'violet'),
                  (2, 0): ('cercle', 'violet'),
                  (-1, 0): ('étoile', 'violet'),
                  (2, -1): ('cercle', 'gris'),
                  (0, 1): ('losange', 'vert'),
                  (-1, 1): ('étoile', 'vert'),
                  (0, -1): ('losange', 'bleu'),
                  (0, 2): ('losange', 'jaune'),
                  (-1, 2): ('étoile', 'jaune')
                 }


x1=dico_example_2[(0,0)]
print(x1[0])


# In[ ]:




