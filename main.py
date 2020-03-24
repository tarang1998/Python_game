from game import Person
from game import bcolors
from magic import spell
from inventory import Item
import random


#create black magic"
fire=spell("Fire",10,100,"black")
thunder=spell("Thunder",10,100,"black")
blizzard=spell("Blizzard",10,100,"black")
meteor=spell("Meteor",20,200,"black")
quake=spell("Quake",14,140,"Black")

#create white magic
cure=spell("Cure",12,120,"white")
cura=spell("Cura",18,200,"white")

#create items
#healing
potion=Item("Potion","potion","Heals 50 HP",50)
hipotion=Item("HiPotion","potion","Heals 100 HP",100)
superpotion=Item("SuperPotion","potion","Heals 500 HP",500)
elixer=Item("Elixer","elixer","Fully restores HP/MP of one party member",9999)
hielixer=Item("HiElixer","elixer","Fully restores party's HP/MP",9999)
#attacking items
grenade=Item("Grenade","attack","Deals 500 damage",500)

player_spells=[fire,thunder,blizzard,meteor,cure,cura]
enemy_spells=[fire,meteor,cure,cura]
player_items=[{"item":potion,"quantity":15},{"item":hipotion,"quantity":5},
              {"item":superpotion, "quantity":5},{"item":elixer,"quantity":5},
              {"item":hielixer, "quantity":2},{"item":grenade,"quantity":5}]

#instantiate people
Player1=Person("Mike  ",1500,300,60,34,player_spells,player_items,"alive")
Player2=Person("Ali   ",2000,200,60,34,player_spells,player_items,"alive")
Player3=Person("Floyd ",1000,100,60,34,player_spells,player_items,"alive")

Enemy1=Person("Devil  ",5000,500,500,25,enemy_spells,[],"alive")
Enemy2=Person("Sutar  ",1000,100,100,25,enemy_spells,[],"alive")
Enemy3=Person("Mago   ",500,100,100,25,enemy_spells,[],"alive")
PlayerL=[Player1,Player2,Player3]
Enemies=[Enemy1,Enemy2,Enemy3]
running=True
i=0
print(bcolors.FAIL + bcolors.BOLD + "AN Enemy Attacks!" + bcolors.ENDC)
while running:
    print("===================")
    print("NAME                 HP                                                   MP")
    for Player in PlayerL:
        if Player.status=="alive":
            Player.get_stats()
    print("\n")
    for Enemy in Enemies:
        if Enemy.status=="alive":
            Enemy.get_enemy_stats()
    j=0
    while(j<3):
        if PlayerL[j].status=="alive":
            print(bcolors.BOLD + bcolors.OKGREEN + "     " + PlayerL[j].name + bcolors.ENDC)
            PlayerL[j].choose_action()
            choice=input("Choose Action:")
            index=int(choice)-1
            if index==0:
                dmg=PlayerL[j].generate_damage()
                choice=PlayerL[j].choose_target(Enemies)
                if Enemies[choice].status=="dead":
                    print(bcolors.OKGREEN+Enemies[choice].name+"is dead.Choose another target"+bcolors.ENDC)
                    continue
                else:
                    Enemies[choice].take_damage(dmg)
                    print(PlayerL[j].name.replace(" ",""),"attacked "+Enemies[choice].name.replace(" ","")+" for",dmg,"points of damage")
            elif index==1:
                PlayerL[j].choose_spell()
                magic_choice=int(input("Choose magic:"))-1
                if magic_choice==-1:
                    continue
                spell=PlayerL[j].magic[magic_choice]
                cost=spell.cost
                magic_dmg=spell.generate_damage()
                current_mp=PlayerL[j].get_mp()
                if spell.cost>current_mp:
                    print(bcolors.FAIL + "\nNot Enough MP\n"+bcolors.ENDC)
                    continue
                PlayerL[j].reduce_mp(spell.cost)
                if spell.type=="white":
                    PlayerL[j].heal(magic_dmg)
                    print(bcolors.OKBLUE+"\n"+spell.name+ " heals for",str(magic_dmg),"HP"+bcolors.ENDC)
                elif spell.type=="black":
                    choice = PlayerL[j].choose_target(Enemies)
                    if Enemies[choice].status == "dead":
                        print(bcolors.OKGREEN + Enemies[choice].name + "is dead.Choose another target" + bcolors.ENDC)
                        continue
                    else:
                        Enemies[choice].take_damage(magic_dmg)
                        print(bcolors.OKBLUE +"\n"+spell.name+" deals",str(magic_dmg),"points of damage"+bcolors.ENDC)

            elif index==2:
                PlayerL[j].choose_item()
                item_choice=int(input("Choose Item:"))-1
                if item_choice==-1:
                    continue
                item=PlayerL[j].items[item_choice]["item"]
                if PlayerL[j].items[item_choice]["quantity"]==0:
                    print(bcolors.FAIL+"You ran out of",item.name+bcolors.ENDC)
                    continue
                PlayerL[j].items[item_choice]["quantity"]-=1
                if item.type=="potion":
                    PlayerL[j].heal(item.prop)
                    print(bcolors.OKGREEN+"\n"+item.name+" heals for",str(item.prop),"HP"+bcolors.ENDC)
                elif item.type=="elixer":
                    if item.name=="HiElixer":
                        for Player in PlayerL:
                            if Player.status=="alive":
                                Player.hp = Player.maxhp
                                Player.mp = Player.maxmp
                        print(bcolors.OKGREEN + "\n" + item.name, " fully restores partys HP/MP" + bcolors.ENDC)
                    else:
                        PlayerL[j].hp=PlayerL[j].maxhp
                        PlayerL[j].mp=PlayerL[j].maxmp
                        print(bcolors.OKGREEN+"\n"+item.name," fully restores HP/MP"+bcolors.ENDC)
                elif item.type=="attack":
                    choice = PlayerL[j].choose_target(Enemies)
                    if Enemies[choice].status == "dead":
                        print(bcolors.OKGREEN + Enemies[choice].name + "is dead.Choose another target" + bcolors.ENDC)
                        continue
                    else:
                        Enemies[choice].take_damage(item.prop)
                        print(bcolors.FAIL+"\n"+item.name,"deals",str(item.prop),"points of damage"+bcolors.ENDC)
        j+=1

    defeated_enemies = 0
    for Enemy in Enemies:
        if Enemy.get_hp() == 0:
            Enemy.status="dead"
            defeated_enemies+= 1
    if defeated_enemies== 3:
        print(bcolors.OKGREEN + "YOU WIN" + bcolors.ENDC)
        running = False

    print(bcolors.FAIL+bcolors.BOLD+"ENEMY ATTACK"+bcolors.ENDC)
    for enemy in Enemies:
        if enemy.status=="alive":
            t=True
            while t:
                enemy_choice = random.randrange(0, 2)#generates 0 and 1
                if enemy_choice==0:
                    enemy_damage=enemy.generate_damage()
                    t=True
                    while t:
                        target=random.randrange(0,3)
                        if PlayerL[target].status=="dead":
                            continue
                        PlayerL[target].take_damage(enemy_damage)
                        print(bcolors.FAIL+enemy.name.replace(" ","")+" attacks "+PlayerL[target].name.replace(" ","") +" for",enemy_damage,"points of damage"+bcolors.ENDC)
                        t=False
                if enemy_choice==1:
                    if enemy.mp<12:
                        continue
                    choice=enemy.choose_enemy_magic()
                    spell=enemy.magic[choice]
                    magic_damage=spell.generate_damage()
                    enemy.reduce_mp(spell.cost)
                    if spell.type=="white":
                        enemy.heal(magic_damage)
                        print(bcolors.FAIL+enemy.name.replace(" ","")+" heals for "+str(magic_damage)+"HP"+bcolors.ENDC)
                        t=False
                    elif spell.type=="black":
                        t = True
                        while t:
                            target = random.randrange(0, 3)
                            if PlayerL[target].status == "dead":
                                continue
                            PlayerL[target].take_damage(magic_damage)
                            print(bcolors.FAIL + enemy.name.replace(" ","") + " attacks "+ PlayerL[target].name.replace(" ","") + " for",str(magic_damage), "points of damage"+"("+str(spell.name) + ")"+bcolors.ENDC)
                            t = False



    dead_players = 0
    for Player in PlayerL:
        if Player.get_hp() == 0:
            Player.status = "dead"
            print(bcolors.FAIL + Player.name + "YOU ARE DEAD" + bcolors.ENDC)
            dead_players += 1
    if dead_players== 3:
        print(bcolors.FAIL + "YOU ARE DEFEATED" + bcolors.ENDC)
        running = False

    print("----------------------")

