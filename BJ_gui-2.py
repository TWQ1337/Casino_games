from tkinter import *
from PIL import ImageTk,Image
import secrets
import time

#gui init
root = Tk()
root.title("Casino Games V_0.2")
root.iconbitmap("data/card-games.ico")
root.geometry("600x501")
root["bg"]="#C4C4C4"



# general info

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
        #list with all decks that playrs have
        self.packed_deck = [{},]
        self.num_of_decks = 1
        self.labels = []
        self.labels_score = []
        self.labels_status = []
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
        text =f"PLAYER SCORE IS {summ}"
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
                # actualy cropping image
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

def game_init():
    p1 = player(player)
    # dealer inint
    dealer1 = dealer(secrets.choice(dealer_names))
    print(f"Your dealer is: {dealer1.name}")
    a = p1, dealer1

    return a


#buttons functions
def buttons_init(plr, dlr, main_deck, deck_n):
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
    if not len(plr.deck) == 2:
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
    if plr.ace_check(deck_n) == 21:
        plr.show_deck(deck_n)
        text = "black jack"
        win_label.configure(text=text)
        a = (plr, dlr)
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
            start_button_place(a)
            bust = True

    elif button_input == "double":
        print("doubling the bet")
        main_deck.card_deal(plr, deck_n)
        plr.show_deck(deck_n)
        plr.card_score(deck_n)
        end_turn = True
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
                    win_label.configure(text=text)

                elif dlr.ace_check(0) == plr.ace_check(i):
                    text = "DRAW"
                    win_label.configure(text=text)

                elif dlr.ace_check(0) > plr.ace_check(i):
                    text = "YOU LOST!"
                    win_label.configure(text=text)

            else:
                text = "YOU WON!"
                win_label.configure(text=text)

        else:
            text = "YOU WON!"
            win_label.configure(text=text)

    a = (plr, dlr)
    start_button_place(a)



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

    dlr.show_top_deck()


    return main_deck

def game(plr, dlr):
    #initing zones

    #dealer zone

    global dealer_hand, dealer_score_lbl, dealer_name_lbl, player_hand, plr_score_lbl, plr_name_lbl, win_label
    dealer_hand = Canvas(root, bg="#C4C4C4", highlightthickness=1, highlightbackground="#989898")
    dealer_hand.place(relheight=0.225, relwidth=0.896, relx=0.05, rely=0.116)

    dealer_name_lbl = Label(root, text=f"{dlr.name}'s hand", bg="#C4C4C4")
    dealer_name_lbl.configure(font=("Open Sans", 14, "italic"))
    dealer_name_lbl.place(relheight=0.03, relwidth=0.4, relx=0.30, rely=0.33)

    dealer_score_lbl = Label(root, text=f"{dlr.name}'S SCORE: ???", bg="#D6D6D6", bd=0)
    dealer_score_lbl.configure(font=("Open Sans", 12, "bold"))
    dealer_score_lbl.place(relheight=0.0499, relwidth=0.896, relx=0.05, rely=0.063)

    #plr zone


    player_hand = Canvas(root, bg="#C4C4C4", highlightthickness=1, highlightbackground="#989898")
    player_hand.place(relheight=0.225, relwidth=0.896, relx=0.05, rely=0.566)

    plr_name_lbl = Label(root, text=f"Shrek 2 on dvd", bg="#C4C4C4")
    plr_name_lbl.configure(font=("Open Sans", 14, "italic"))
    plr_name_lbl.place(relheight=0.03, relwidth=0.4, relx=0.30, rely=0.555)

    plr_score_lbl = Label(root, text="PLAYER'S SCORE: ???", bg="#D6D6D6", bd=0)
    plr_score_lbl.configure(font=("Open Sans", 12, "bold"))
    plr_score_lbl.place(relheight=0.0499, relwidth=0.896, relx=0.05, rely=0.791)

    #win status
    #todo fix scaling issues
    win_label = Label(root, bg="#C4C4C4")
    win_label.configure(font=("Open Sans", 25, "bold"))
    win_label.place(relx=0.38, rely=0.4)

    #    log = LabelFrame(root, text="log", padx=50, pady=100)
#    log.grid(row=1, column=0, rowspan=2)

#    buttons = LabelFrame(root, text="buttons", padx=40, pady=30)
#    buttons.grid(row=4, column=1, rowspan=2)

#    lbl = Label(buttons, text="Choices")
#    lbl.grid(row=0, column=0)

    main_deck = game_start(plr, dlr)
    deck_init(plr, dlr, main_deck, 0)


def start_button(a):
    if len(root.winfo_children())>1:
        dealer_hand.destroy()
        dealer_score_lbl.destroy()
        dealer_name_lbl.destroy()

        player_hand.destroy()
        plr_name_lbl.destroy()
        plr_score_lbl.destroy()
        win_label.destroy()

    game(*a)
    startb.destroy()


def start_button_place(a):
    global startb
    startb = Button(root, text="PLAY BLACKJACK", bg="#FFEA28", command=lambda: start_button(a))
    startb.configure(font=("Open Sans", 12, "bold"))
    startb.place(relheight=0.0838, relwidth=0.653, relx=0.173, rely=0.864)

def game_loop():
    d1_p1 = game_init()
    start_button_place(d1_p1)


game_loop()
#start_button_place()
root.mainloop()

