import json
import os
from tkinter import *
from PIL import ImageTk,Image
import secrets
#import time
#import Main_menu

#gui init

root = Tk()
root.title("Casino Games V_0.2")
root.iconbitmap("data/card-games.ico")
root.geometry("780x780")
root["bg"]="#C4C4C4"



# general info

default_player = {
    "gold" : 1000,
    "skill" : 0,
    "won"   : 0
        }

list_of_labels = list()
set = list("234567890JQKA")
# card_suit = "Tiles", "Clovers", "Pikes", "Hearts"
card_suit = "♦", "♣", "♠", "♥"
# todo: potentially add name generator function
dealer_names = "Maxime Hand", "Dr. Zack Homenick", "Chloe Cruickshank Sr.", "Kelvin Miller"


# deck
class deck():
    def __init__(self):
        self.deck = dict()

    # generating deck out combining general info
    def create_new_deck(self):
        for i in range(len(set)):
            for x in range(len(card_suit)):
                if set[i] == "J" or set[i] == "Q" or set[i] == "K":
                    self.deck.update({f"{set[i]} of {card_suit[x]}": 10})
                elif set[i] == "A":
                    self.deck.update({f"{set[i]} of {card_suit[x]}": 11})
                #elif set[i] == "0":
                #    self.deck.update({f"10 of {card_suit[x]}": 10})
                else:
                    self.deck.update({f"{set[i]} of {card_suit[x]}": i + 2})
        return True

    def card_deal(self, who, deck_n):
        who.unpack_deck(deck_n)
        a = secrets.choice(list(self.deck))
        if isinstance(who, dealer):
            if who.card_dealt():
                print(f"card dealt {a}")
            else:
                print("card dealt to dealer")
        else:
            print(f"card dealt {a}")
        who.deck.update({f"{a}": self.deck[a]})
        self.deck.pop(a)


class player:
    def __init__(self, name):
    #  self.deck = dict()
        self.deck = {}
        self.name = name
        #list with all decks that player have
        self.packed_deck = [{},]
        self.num_of_decks = 1
        self.labels = []
        self.labels_score = []
        self.labels_status = []
        self.p_data = self.load_data()
#method that set a self.deck reference to on of list objects.
    def unpack_deck(self, i):
        self.deck = self.packed_deck[i]


#method that shows current cards in deck with number deck_n text redundant
    '''
    def show_deck_1(self, deck_n):
        self.unpack_deck(deck_n)
        a = list(self.deck.keys())
        b = ""
        for i in range(len(a)):
            b = b + " " + str(a[i])
        text = str(f"{self.name} hand is: {b}")
        if len(self.labels)-1 < deck_n:
            self.labels.append(Label(player_hand, text=text))
        else:
            c = self.labels[deck_n]
            c.config(text=text)
        v = self.labels[deck_n]
        v.place(relx=0.313, rely=0.3)
        #v.grid(row=deck_n, column=0)
    '''

#method that shows card score in deck with number deck_n
    def card_score(self, deck_n):
        self.unpack_deck(deck_n)
        summ = 0
        for i in self.deck:
            summ = summ + self.deck[i]
        text =f"{self.name.upper()} SCORE IS {summ}"
        plr_score_lbl.configure(text=text)
        return summ

#method that checks if ace should be counted as 1 or 11 in deck with number dekc_n
    def ace_check(self, deck_n):
        self.unpack_deck(deck_n)
        check = True
        while check:
            for x in range(len(card_suit)):
                if f"A of {card_suit[x]}" in self.deck and self.card_score(deck_n) > 21:
                    self.deck[f"A of {card_suit[x]}"] = 1
                check = False
        rt_value = self.card_score(deck_n)
        return rt_value

#method that checks if you can split deck with number deck_n
    def split_check(self, deck_n):
        self.unpack_deck(deck_n)
        if len(self.deck.keys()) == 2:
            x = list(self.deck.keys())
            if x[0][0] in x[1][0]:
                print("you can split")
                return True
            else:
                return False

#method that splits deck with number deck_n and adds new deck to the list of packed decks
    def split_deck(self, deck_n, where_to):
        self.unpack_deck(deck_n)
        a = list(self.deck.keys())
        b = {f"{a[0]}": self.deck[f"{a[0]}"]}
        self.deck.pop(a[0])
        self.packed_deck.append({})
        self.unpack_deck(where_to)
        self.deck.update(b)
        self.num_of_decks += 1

    def show_deck(self, deck_n):
        self.unpack_deck(deck_n)
        x = list(self.deck.keys())
        coord_l = list()
        # creating coordinates to crop picture by
        for i in x:
            b = i[0]
            if b == "A":
                b = 1
            elif b == "J":
                b = 11
            elif b == "Q":
                b = 12
            elif b == "K":
                b = 13
            elif b == "0":
                b = 10
            else:
                b = int(i[0])
            c = i[5]
            if c == "♠":
                c = 3
            elif c == "♣":
                c = 0
            elif c == "♦":
                c = 1
            elif c == "♥":
                c = 2
            coord_l.append((b, c))

        with Image.open("data/cards1.png").convert("RGBA") as img:
            self.list_of_labels = list()

            # getting opened image size to properly crop it
            w, h = img.size
            self.pil_image_list = list()

            # croping image in for i loop with coordinates processed from dictionary keys earlier
            count2 = 1
            for i in coord_l:
                # unpacking tuple
                c_value, c_suit = i
                # creating the right card position
                left = (c_value - 1) * (w / 13)
                right = c_value * (w / 13)
                upper = c_suit * (h / 5)
                lower = (c_suit + 1) * (h / 5)
                # actualy cropping image
                img_croped = img.crop([left, upper, right, lower])
                #resizing the image
                root.update()
                k = player_hand.winfo_height()
                v = player_hand.winfo_width()
                img2w, img2h = img_croped.size
                cooef = k / img2h
                img2k = cooef * img2w
                k = int(0.67 * k)
                img2k = int(0.67 * img2k)
                img3 = img_croped.resize((img2k, k), Image.ANTIALIAS)
                # converting it into tkinter image and adding it to the list
                self.pil_image_list.append(ImageTk.PhotoImage(img3))
                # making a label with the cropped image, and adding it to the list of labels with cropped images
            for x in self.pil_image_list:
                self.list_of_labels.append(Label(player_hand, image=x, bg="#C4C4C4"))
                count2 +=1
            # trying to display labels
        count = 0.3
        for i in self.list_of_labels:

            #i.grid(row=0, column=count)
            #count += 0.44/(0.057*(count2))

            i.place(relx=count, rely=0.1)
            count += 0.44/count2


    def check_save_folder(self):
        #checking save_folder
        if os.path.exists("savesJSON"):
            return True
        else:
            os.mkdir("savesJSON")
            print("creating save folder")
            return True

    def save_vibe(self):
        #checking is save exists, creating new file if nothing found
        if os.path.isfile(f"savesJSON/{self.name}.json"):
            print (f"hello, {self.name}! Loading file now.")
            save_data = open(f"savesJSON/{self.name}.json", "r")
            return True
        else:
            print("New player, welcome, creating save file")
            save_data = open(f"savesJSON/{self.name}.json", "x")
            save_data.write(json.dumps(default_player, indent=2))
            return False

    def load_data(self):
        self.check_save_folder()
        self.save_vibe()
        p_data = json.load(open(f"savesJSON/{self.name}.json", "r"))
        print("data loaded")
        return p_data

    def save_data(self):
        save_data = open(f"savesJSON/{self.name}.json", "w")
        save_data.write(json.dumps(self.p_data, indent=2))

class dealer(player):
   def show_top_deck (self):
        self.unpack_deck(0)
        x = list(self.deck.keys())
        coord_l = list()
        # creating coordinates to crop picture by
        counter = 0
        for i in x:
            b = i[0]
            if b == "A" and not counter:
                b = 1
            elif b == "J"and not counter:
                b = 11
            elif b == "Q"and not counter:
                b = 12
            elif b == "K"and not counter:
                b = 13
            elif b == "0"and not counter:
                b = 10
            elif counter != 0:
                b = 3
            else:
                b = int(i[0])
            c = i[5]
            if c == "♠"and not counter:
                c = 3
            elif c == "♣"and not counter:
                c = 0
            elif c == "♦"and not counter:
                c = 1
            elif c == "♥"and not counter:
                c = 2
            elif counter !=0:
                c = 4
            coord_l.append((b, c))
            counter +=1



        with Image.open("data/cards1.png").convert("RGBA") as img:
            self.list_of_labels = list()

            # getting opened image size to properly crop it
            w, h = img.size
            self.pil_image_list = list()

            # croping image in for i loop with coordinates processed from dictionary keys earlier
            count2 = 1
            for i in coord_l:
                # unpacking tuple
                c_value, c_suit = i
                # creating the right card position
                left = (c_value - 1) * (w / 13)
                right = c_value * (w / 13)
                upper = c_suit * (h / 5)
                lower = (c_suit + 1) * (h / 5)
                # actualy cropping imagea
                img_croped = img.crop([left, upper, right, lower])
                # resizing the image
                root.update()
                k = dealer_hand.winfo_height()
                v = dealer_hand.winfo_width()
                img2w, img2h = img_croped.size
                cooef = k / img2h
                img2k = cooef * img2w
                k = int(0.67 * k)
                img2k = int(0.67 * img2k)
                print(img2k)
                img3 = img_croped.resize((img2k, k), Image.ANTIALIAS)
                # converting it into tkinter image and adding it to the list
                self.pil_image_list.append(ImageTk.PhotoImage(img3))
                # making a label with the cropped image, and adding it to the list of labels with cropped images
            for x in self.pil_image_list:
                self.list_of_labels.append(Label(dealer_hand, image=x, bg="#C4C4C4"))
                count2 += 1
            # trying to display labels
        count = 0.3
        for i in self.list_of_labels:
            # i.grid(row=0, column=count)
            # count += 0.44/(0.057*(count2))

            i.place(relx=count, rely=0.1)
            count += 0.44 / count2


   def check_save_folder(self):
       pass

   def save_vibe(self):
       pass

   def load_data(self):
       pass

   def save_data(self):
       pass

   def show_top_deck_text(self, ):
        self.unpack_deck(0)
        a = list(self.deck.keys())
        b = f"Dealer's hand {str(a[0])} + {len(a)-1} cards"
        lbl = Label(dealer_hand, text=b)
        lbl.grid(row=0, column=0)


   def ai(self, deck_name):
        self.unpack_deck(0)
        while self.ace_check(0) < 17:
            deck_name.card_deal(self, 0)
        self.show_deck(0)
        self.card_score(0)

   def card_dealt(self):
        self.unpack_deck(0)
        if self.deck != {}:
            return False
        else:
            return True

   def show_deck_text(self, deck_n):
        self.unpack_deck(deck_n)
        a = list(self.deck.keys())
        b = ""
        for i in range(len(a)):
            b = b + " " + str(a[i])
        text = str(f"{self.name} hand is: {b}")
        if len(self.labels)-1 < deck_n:
            self.labels.append(Label(dealer_hand, text=text))
        else:
            c = self.labels[deck_n]
            c.config(text=text)
        v = self.labels[deck_n]
        v.grid(row=deck_n, column=0)

   def show_deck(self, deck_n):
        self.unpack_deck(0)
        x = list(self.deck.keys())
        coord_l = list()
        # creating coordinates to crop picture by
        #todo: use any methode to check
        for i in x:
            b = i[0]
            if b == "A":
                b = 1
            elif b == "J":
                b = 11
            elif b == "Q":
                b = 12
            elif b == "K":
                b = 13
            elif b == "0":
                b = 10
            else:
                b = int(i[0])
            c = i[5]
            if c == "♠":
                c = 3
            elif c == "♣":
                c = 0
            elif c == "♦":
                c = 1
            elif c == "♥":
                c = 2
            coord_l.append((b, c))

        with Image.open("data/cards1.png").convert("RGBA") as img:
            self.list_of_labels = list()

            # getting opened image size to properly crop it
            w, h = img.size
            self.pil_image_list = list()

            # croping image in for i loop with coordinates processed from dictionary keys earlier
            count2 = 1
            for i in coord_l:
                # unpacking tuple
                c_value, c_suit = i
                # creating the right card position
                left = (c_value - 1) * (w / 13)
                right = c_value * (w / 13)
                upper = c_suit * (h / 5)
                lower = (c_suit + 1) * (h / 5)
                # actualy cropping image
                img_croped = img.crop([left, upper, right, lower])
                #resizing the image
                root.update()
                k = dealer_hand.winfo_height()
                v = dealer_hand.winfo_width()
                img2w, img2h = img_croped.size
                cooef = k / img2h
                img2k = cooef * img2w
                k = int(0.67 * k)
                img2k = int(0.67 * img2k)
                img3 = img_croped.resize((img2k, k), Image.ANTIALIAS)
                # converting it into tkinter image and adding it to the list
                self.pil_image_list.append(ImageTk.PhotoImage(img3))
                # making a label with the cropped image, and adding it to the list of labels with cropped images
            for x in self.pil_image_list:
                self.list_of_labels.append(Label(dealer_hand, image=x, bg="#C4C4C4"))
                count2 +=1
            # trying to display labels
        count = 0.3
        for i in self.list_of_labels:

            #i.grid(row=0, column=count)
            #count += 0.44/(0.057*(count2))

            i.place(relx=count, rely=0.1)
            count += 0.44/count2

    #method that shows card score in deck with number deck_n
   def card_score(self, deck_n):
        self.unpack_deck(deck_n)
        summ = 0
        for i in self.deck:
            summ = summ + self.deck[i]
        text =f"score is {summ}"
        dealer_score_lbl.configure(text=text)

        return summ

#method that checks if ace should be counted as 1 or 11 in deck with number dekc_n
   def ace_check(self, deck_n):
        self.unpack_deck(deck_n)
        check = True
        while check:
            for x in range(len(card_suit)):
                if f"A of {card_suit[x]}" in self.deck and self.card_score(deck_n) > 21:
                    self.deck[f"A of {card_suit[x]}"] = 1
                check = False
        rt_value = self.card_score(deck_n)
        return rt_value




# todo gold, name, skill attachment.

def game_init(p_name):
    p1 = player(p_name)
    # dealer inint
    dealer1 = dealer(secrets.choice(dealer_names))
    print(f"Your dealer is: {dealer1.name}")
    a = p1, dealer1

    return a


#buttons functions
def buttons_init(plr, dlr, main_deck, deck_n):
    dlr.show_top_deck()
    #TODO bind buttons to global widged
    global hit_button, split_button, double_button, stand_button

    plr.unpack_deck(deck_n)
    hit_button = Button(root, text="HIT", bg="#969696",
                        command=lambda: button_input(plr, dlr, main_deck, deck_n, "hit"))
    hit_button.configure(font=("Open Sans", 11, "bold"))
    hit_button.place(relheight=0.083, relwidth=0.166, relx=0.126, rely=0.872)

    split_button = Button(root, text="SPLIT", bg="#969696", state=DISABLED,
                          command=lambda: button_input(plr, dlr, main_deck, deck_n, "split"))
    split_button.configure(font=("Open Sans", 11, "bold"))
    split_button.place(relheight=0.083, relwidth=0.166, relx=0.687, rely=0.872)
    if plr.split_check(deck_n):
        split_button["state"]=NORMAL


    double_button = Button(root, text="DOUBLE", bg="#969696",
                           command=lambda: button_input(plr, dlr, main_deck, deck_n, "double"))
    double_button.configure(font=("Open Sans", 11, "bold"))
    double_button.place(relheight=0.083, relwidth=0.166, relx=0.313, rely=0.872)
    if not len(plr.deck) == 2 or plr.bet>=plr.p_data["gold"]:
        double_button["state"]=DISABLED

    stand_button = Button(root, text="STAND", bg="#969696",
                          command=lambda: button_input(plr, dlr, main_deck, deck_n, "stand"))
    stand_button.configure(font=("Open Sans", 11, "bold"))
    stand_button.place(relheight=0.083, relwidth=0.166, relx=0.5, rely=0.872)


def deck_init(plr, dlr, main_deck, deck_n):
    #todo: fix bust check on split decks
    plr.unpack_deck(deck_n)
    a = len(plr.deck.keys())

    if a < 2:
        main_deck.card_deal(plr, deck_n)
    if plr.ace_check(deck_n) == 21 and len(plr.deck)<3:
        plr.show_deck(deck_n)
        text = "black jack"
        win_label.configure(text=text)
        plr.p_data["gold"] = plr.p_data["gold"] + (plr.bet*2.5)
        win_txt.configure(text=f"WON: {plr.bet * 2.5} ")
        plr.save_data()
        a = (plr, dlr)
        if plr.p_data["gold"] <= 0:
            for i in root.winfo_children():
                i.destroy()
            you_owe_me = Label(root, text="You owe me 3000 bucks")
            you_owe_me.pack()
        else:
            start_button_place(a)

    else:

        plr.show_deck(deck_n)
        buttons_init(plr, dlr, main_deck, deck_n)
        plr.ace_check(deck_n)
        plr.card_score(deck_n)


def button_input(plr, dlr, main_deck, deck_n, button_input):
    end_turn = False
    bust = False
    hit_button.destroy()
    split_button.destroy()
    double_button.destroy()
    stand_button.destroy()
    if button_input == "hit":
        main_deck.card_deal(plr, deck_n)
        if plr.ace_check(deck_n) > 21:
            text = "BUST!"
            win_label.configure(text=text)
            a = (plr, dlr)
            bust = True

    elif button_input == "double":
        print("doubling the bet")
        main_deck.card_deal(plr, deck_n)
        plr.show_deck(deck_n)
        plr.card_score(deck_n)
        end_turn = True
        plr.p_data["gold"] = plr.p_data["gold"] - plr.bet
        plr.bet = plr.bet * 2
        if plr.ace_check(deck_n) > 21:
            text = "BUST!"
            win_label.configure(text=text)
            bust = True

    elif button_input == "split":
        plr.split_deck(deck_n, plr.num_of_decks)
        main_deck.card_deal(plr, plr.num_of_decks-1)
        plr.show_deck(plr.num_of_decks-1)
        print(f"{plr.name}'s score is {plr.ace_check(plr.num_of_decks-1)}")
        deck_init(plr, dlr, main_deck, plr.num_of_decks-1)
        plr.unpack_deck(deck_n)
        main_deck.card_deal(plr, deck_n)
        plr.show_deck(deck_n)
    elif button_input == "stand":
        end_turn = True

    if deck_n+2 > plr.num_of_decks and end_turn and not bust:
        game_end(plr, dlr, main_deck)
    elif bust:
        a = (plr, dlr)
        if plr.p_data["gold"] <= 0:
            for i in root.winfo_children():
                i.destroy()
            you_owe_me = Label(root, text="You owe me 3000 bucks")
            you_owe_me.pack()
        else:
            start_button_place(a)
    elif not end_turn and not bust:
        deck_init(plr, dlr, main_deck, deck_n)
    else:
        deck_init(plr, dlr, main_deck, deck_n+1)

def game_end(plr, dlr, main_deck):
    dlr.ai(main_deck)
    for i in range(plr.num_of_decks):
        if plr.ace_check(i) <= 21:
            if not dlr.ace_check(0) > 21:
                if dlr.ace_check(0) < plr.ace_check(i):
                    text = "YOU WON!"
                    plr.p_data["gold"] = plr.p_data["gold"] + (plr.bet*2)
                    plr.save_data()
                    win_label.configure(text=text)
                    win_txt.configure(text=f"WON: {plr.bet * 2} ")

                elif dlr.ace_check(0) == plr.ace_check(i):
                    text = "DRAW"
                    win_label.configure(text=text)
                    plr.p_data["gold"] = plr.p_data["gold"] + plr.bet

                elif dlr.ace_check(0) > plr.ace_check(i):
                    text = "YOU LOST!"
                    win_label.configure(text=text)

            else:
                text = "YOU WON!"
                win_label.configure(text=text)
                plr.p_data["gold"] = plr.p_data["gold"] + (plr.bet*2)
                win_txt.configure(text=f"WON: {plr.bet*2} ")
                plr.save_data()

        else:
            text = "YOU WON!"
            win_label.configure(text=text)
            plr.p_data["gold"] = plr.p_data["gold"] + (plr.bet*2)
            win_txt.configure(text=f"WON: {plr.bet * 2} ")
            plr.save_data()

    a = (plr, dlr)
    print(f"gold at the end{plr.p_data}")
    if plr.p_data["gold"] <= 0:
       for i in root.winfo_children():
           i.destroy()
       you_owe_me = Label (root, text ="You owe me 3000 bucks")
       you_owe_me.pack()
    else:
        start_button_place(a)

def betting(p1, dlr, main_deck,  bet, list):
        p1.p_data["gold"] = p1.p_data["gold"] - int(bet)
        p1.bet = int(bet)
        for i in list:
            i.destroy()
        deck_init(p1, dlr, main_deck, 0)
        win_label.configure(text="")
        bet_txt.configure(text=f"BET: {bet}")
        gold = p1.p_data["gold"]
        plr_gold_lbl.configure(text=f"BALANCE: {gold}")



def game_start(p1, dlr):
    p1.num_of_decks = 1
    # flushing decks
    p1.unpack_deck(0)
    p1.packed_deck = [{},]
    dlr.unpack_deck(0)
    dlr.packed_deck = [{},]
    # creating deck
    main_deck = deck()
    main_deck.create_new_deck()
    # dealing cards

    main_deck.card_deal(p1, 0)
    main_deck.card_deal(dlr, 0)
    main_deck.card_deal(p1, 0)
    main_deck.card_deal(dlr, 0)

    # checking block
    return main_deck

def game(plr, dlr):
    #initing zones
    global dealer_hand, dealer_score_lbl, dealer_name_lbl,\
        player_hand, plr_score_lbl, plr_name_lbl, win_label, plr_gold_lbl,status_bar, leave_the_game\
        ,bet_canvas, bet_txt, win_txt


    # gui
    status_bar = Label(root, text="BLACKJACK", bg="#CFCFCF", anchor="w")
    status_bar.place(relheight=0.044, relwidth=1, relx=0.0, rely=0.0)
    status_bar.configure(font=("Open Sans", 10, "bold"))

    leave_the_game = Button(root, text="LEAVE THE GAME", bg="#434343", fg="#FFFFFF",
                            command=lambda :leave_button(plr, dlr))
    leave_the_game.configure(font=("Open Sans", 10, "bold"))
    leave_the_game.place(relheight=0.044, relwidth=0.182, relx=0.817, rely=0.0)

    bet_canvas = Canvas(root, bg="#BCBCBC", highlightthickness=1, highlightbackground="#A9A9A9")
    bet_canvas.place(relheight=0.06, relwidth=0.491, relx=0.0, rely=0.737)

    bet_txt = Label(bet_canvas, text="Bet:-", fg="#727272", bg="#BCBCBC")
    bet_txt.configure(font=("Open Sans", 18, "bold"))
    bet_txt.place(relx=0.402, rely=0.0287)


    win_canvas = Canvas(root, bg="#BCBCBC", highlightthickness=1, highlightbackground="#A9A9A9")
    win_canvas.place(relheight=0.128, relwidth=0.502, relx=0.498, rely=0.737)

    win_txt = Label(win_canvas, text="WON: - ", fg="#727272", bg="#BCBCBC")
    win_txt.configure(font=("Open Sans", 18, "bold"))
    win_txt.place(relx=0.402, rely=0.0287)


    balance_canvas = Canvas(root, bg="#BCBCBC", highlightthickness=1, highlightbackground="#A9A9A9")
    balance_canvas.place(relheight=0.06, relwidth=0.491, relx=0, rely=0.803)

    gold = plr.p_data["gold"]
    name_upper = plr.name.upper()


    plr_gold_lbl = Label(balance_canvas, text=f"BALANCE: {gold}", fg="#727272", bg="#BCBCBC")
    plr_gold_lbl.configure(font=("Open Sans", 18, "bold"))
    plr_gold_lbl.place(relx=0.268, rely=0.0287)


    #dealer zone

    dealer_hand = Canvas(root, bg="#C4C4C4", highlightthickness=1, highlightbackground="#989898")
    dealer_hand.place(relheight=0.197, relwidth=0.8589, relx=0.0679, rely=0.130)

    dealer_name_lbl = Label(root, text=f"{dlr.name}'S HAND", bg="#C4C4C4")
    dealer_name_lbl.configure(font=("Open Sans", 12, "italic"))
    dealer_name_lbl.place(relheight=0.03, relwidth=0.4, relx=0.30, rely=0.31)

    dealer_score_lbl = Label(root, text=f"{dlr.name}'S SCORE: ???", bg="#D6D6D6", bd=0)
    dealer_score_lbl.configure(font=("Open Sans", 12, "bold"))
    dealer_score_lbl.place(relheight=0.053, relwidth=0.8589, relx=0.0679, rely=0.0769)

    #plr zone

    player_hand = Canvas(root, bg="#C4C4C4", highlightthickness=1, highlightbackground="#989898")
    player_hand.place(relheight=0.197, relwidth=0.8589, relx=0.0679, rely=0.441)

    plr_name_lbl = Label(root, text=f"{name_upper}'S HAND", bg="#C4C4C4")
    plr_name_lbl.configure(font=("Open Sans", 12, "italic"))
    plr_name_lbl.place(relheight=0.03, relwidth=0.4, relx=0.30, rely=0.433)
    print(plr.p_data)


    plr_score_lbl = Label(root, text=f"{name_upper}'S SCORE: ???", bg="#D6D6D6", bd=0)
    plr_score_lbl.configure(font=("Open Sans", 12, "bold"))
    plr_score_lbl.place(relheight=0.053, relwidth=0.8589, relx=0.0679, rely=0.640)

    #win status
    #todo fix scaling issues
    win_label = Label(root, bg="#C4C4C4")
    win_label.configure(font=("Open Sans", 14, "bold"))
    win_label.place(relx=0.38, rely=0.4)

    #    log = LabelFrame(root, text="log", padx=50, pady=100)
#    log.grid(row=1, column=0, rowspan=2)

#    buttons = LabelFrame(root, text="buttons", padx=40, pady=30)
#    buttons.grid(row=4, column=1, rowspan=2)

#    lbl = Label(buttons, text="Choices")
#    lbl.grid(row=0, column=0)

    main_deck = game_start(plr, dlr)
    betting_buttons_place(plr, dlr, main_deck)
    #deck_init(plr, dlr, main_deck, 0)

def betting_buttons_place(plr, dlr, main_deck):
    lst_bet_buttons = list()

    max_bet = Button(root, text="MAX BET", bg="#969696", bd=0,
                     command=lambda :betting(plr, dlr,main_deck, plr.p_data["gold"], lst_bet_buttons))
    max_bet.configure(font=("Open Sans", 11, "bold"))
    max_bet.place(relheight=0.060, relwidth=0.163, relx=0.10, rely=0.906)

    tenth_bet = Button(root, text="1/10 BET", bg="#969696", bd=0,
                       command=lambda :betting(plr, dlr, main_deck, plr.p_data["gold"]/10, lst_bet_buttons))
    tenth_bet.configure(font=("Open Sans", 11, "bold"))
    tenth_bet.place(relheight=0.060, relwidth=0.163, relx=0.285, rely=0.906)


    bet_entry = Entry(root, text="BET", bg="#B4B4B4", bd=0, fg="#969696")
    bet_entry.configure(font=("Open Sans", 10, "bold"))
    bet_entry.place(relheight=0.060, relwidth=0.165, relx=0.735, rely=0.906)

    bet_entry.insert(END, "type your bet here")
    bet_entry.bind("<Key>", on_click)
    bet_entry.focus()

    input_bet = Button(root, text="BET", bg="#969696", bd=0,
                       command=lambda :bet_button(plr, dlr, main_deck, bet_entry.get(), lst_bet_buttons))
    input_bet.configure(font=("Open Sans", 11, "bold"))
    input_bet.place(relheight=0.060, relwidth=0.266, relx=0.47, rely=0.906)


    lst_bet_buttons.append(max_bet)
    lst_bet_buttons.append(tenth_bet)
    lst_bet_buttons.append(input_bet)
    lst_bet_buttons.append(bet_entry)

def bet_button(plr, dlr, main_deck, bet, lst_bet_buttons):
    if int(bet) > int(plr.p_data["gold"]):
        win_label.configure(text="BET'S TOO BIG, MAN")
        for i in lst_bet_buttons:
            i.destroy()
        betting_buttons_place(plr, dlr, main_deck)
    else:
        betting(plr, dlr, main_deck, bet, lst_bet_buttons)

def leave_button(plr, dlr):
    for i in root.winfo_children():
        i.destroy()
    main_menu(plr, dlr)


def start_button(a):
    if len(root.winfo_children())>1:
        '''
        dealer_score_lbl.destroy()
        dealer_name_lbl.destroy()
        dealer_hand.destroy()
        plr_name_lbl.destroy()
        plr_gold_lbl.destroy()
        player_hand.destroy()
        plr_name_lbl.destroy()
        plr_score_lbl.destroy()
        win_label.destroy()
        '''
        for i in root.winfo_children():
            i.destroy()
    game(*a)
    #startb.destroy()


def start_button_place(a):
    global startb
    startb = Button(root, text="PLAY BLACKJACK", bg="#FFEA28", command=lambda: start_button(a))
    startb.configure(font=("Open Sans", 12, "bold"))
    startb.place(relheight=0.0838, relwidth=0.653, relx=0.173, rely=0.864)

def game_loop(p_name):
    p1_d1 = game_init(p_name)
    main_menu(*p1_d1)
    #start_button_place(d1_p1)


def login(p1):
    for i in root.winfo_children():
        i.destroy()
    game_loop(p1)
    root.configure(bg="#C4C4C4")

def main_menu(plr, dlr):
    a = plr, dlr
    plr_info_area = Canvas(root, bg="#CFCFCF", highlightthickness=1, highlightbackground="#BABABA")
    plr_info_area.place(relheight=0.1628, relwidth=1, relx=0, rely=0)
    gold = plr.p_data["gold"]
    plr_stats_area = Label(root, bg="#DADADA", text=f"{gold} |  Stat1 Stat2 Stat3 Stat 4", fg="#727272")
    plr_stats_area.configure(font=("Open Sans", 18, "bold"))
    plr_stats_area.place(relheight=0.0718, relwidth=0.7154, relx=0.2179, rely=0.0615)

    plr_name_area = Label(root, bg="#CFCFCF", text=f"{plr.name}", fg="#000000")
    plr_name_area.configure(font=("Open Sans", 10, "bold"))
    plr_name_area.place(relheight=0.0244, relwidth=0.1397, relx=0.2359, rely=0.0256)

    games_button_section = Canvas(root, bg="#CFCFCF", highlightthickness=2, highlightbackground="#A7A7A7")
    games_button_section.place(relheight=0.7654, relwidth=0.4397, relx=0.4962, rely=0.1987)

    bj_button = Button(root, text="BLACKJACK", fg="#FFFFFF", bg="#4F4F4F", bd=0, command=lambda: start_button(a))
    bj_button.place(relwidth=0.3871, relheight=0.191, relx=0.5205, rely=0.3012)

    cm_button = Button(root, text="CRASH MARKET", fg="#FFFFFF", bg="#4F4F4F", bd=0)
    cm_button.place(relwidth=0.3871, relheight=0.191, relx=0.5205, rely=0.5179)

    pkr_button = Button(root, text="POKER", fg="#FFFFFF", bg="#4F4F4F", bd=0)
    pkr_button.place(relwidth=0.3871, relheight=0.191, relx=0.5205, rely=0.7346)

    image1 = Image.open("data/trump.png")
    test = ImageTk.PhotoImage(image1)

    label1 = Label(image=test)
    label1.image = test
    # Position image
    label1.place(relx=0.02, rely=0.1987)

def on_click(event):
    if event.widget.get()=="TYPE YOUR NAME HERE":
        event.widget.delete(0, END)
    elif event.widget.get()=="type your bet here":
        event.widget.delete(0, END)
def log_in():
    root.configure(bg="#1F1F1F")
    txt = Entry(root, width=10, bg="#303030", fg="#545454", bd=0)
    txt.place(relheight=0.041, relwidth=0.5821, rely=0.4231, relx=0.209)
    txt.focus()
    txt.insert(END, "TYPE YOUR NAME HERE")
    txt.bind("<Key>", on_click)
    #txt.configure(font=())


    login_button = Button(root, text="LOG IN", bg="#FFEA28", command=lambda: login(txt.get()))
    login_button.place(relheight=0.0718, relwidth=0.5821, rely=0.4897, relx=0.209)



if __name__ == "__main__":
    log_in()
    #game_loop()
    #start_button_place()
    root.mainloop()

#todo a gold check on the end of the turn