import random


class bcolors:
    HEADER='\033[95m'
    OKBLUE='\033[94m'
    OKGREEN='\033[92m'
    WARNING='\033[93m'
    FAIL='\033[91m'
    ENDC='\033[0m'
    BOLD='\033[1m'
    UNDERLINE='\033[4m'

class Person:
    def __init__(self,name,hp,mp,atk,df,magic,items,status):
        self.maxhp=hp
        self.hp=hp
        self.maxmp=mp
        self.mp=mp
        self.atkl=atk-10
        self.atkh=atk+10
        self.df=df
        self.magic=magic
        self.actions=["Attack","Magic","Items"]
        self.items=items
        self.name=name
        self.status=status #use del Enemies[choice] instead

    def generate_damage(self):
        return random.randrange(self.atkl,self.atkh)

    def take_damage(self,dmg):
        self.hp-=dmg
        if self.hp <0:
            self.hp=0
        return self.hp

    def choose_target(self,enemies):
        i=1
        print(bcolors.FAIL+"    Enemies:"+bcolors.ENDC)
        for enemy in enemies:
            if enemy.status=="dead":
                print("    "+str(i)+":"+enemy.name+bcolors.FAIL+"(DEAD)"+bcolors.ENDC)
            else:
                print("    "+str(i) + ":" + enemy.name)
            i+=1
        target=input("Enter target:")
        choice=int(target)-1
        return choice


    def heal(self,dmg):
        self.hp+=dmg
        if self.hp>self.maxhp:
            self.hp=self.maxhp
        return self.hp

    def get_hp(self):
        return self.hp

    def get_max_hp(self):
        return self.maxhp

    def get_mp(self):
        return self.mp

    def get_max_mp(self):
        return self.maxmp

    def reduce_mp(self,cost):
        self.mp-=cost

    def choose_action(self):
        i=1
        print(bcolors.OKBLUE+bcolors.BOLD+"     ACTION"+bcolors.ENDC)
        for item in self.actions:
            print("     ",str(i)+":",item)
            i+=1

    def choose_spell(self):
        i = 1
        print("\n",bcolors.OKBLUE + bcolors.BOLD + "MAGIC" + bcolors.ENDC)
        for spell in self.magic:
            print("    ",str(i) + ":",spell.name ,"(Cost:",str(spell.cost)+")")
            i += 1

    def reduce_mp(self,mp_cost):
        self.mp-=mp_cost
        if self.mp<0:
            self.mp=0
        return self.mp

    def choose_item(self):
        i=1

        print("\n",bcolors.OKGREEN+bcolors.BOLD+"ITEMS"+bcolors.ENDC)
        for item in self.items:
            print("    ",str(i)+":",item["item"].name,",",item["item"].description,",quantity:",str(item["quantity"]))
            i+=1
    def get_stats(self):
        hp_bar=""
        bar_ticks=(self.hp/self.maxhp)*100/4
        mp_bar=""
        mpbar_ticks=(self.mp/self.maxmp)*10
        while bar_ticks>0:
            hp_bar+="█"
            bar_ticks-=1

        while mpbar_ticks>0:
            mp_bar+="█"
            mpbar_ticks-=1

        while len(hp_bar)<25:
            hp_bar += "░"

        while len(mp_bar)<10:
            mp_bar+="░"

        hp_string=str(self.hp)+"/"+str(self.maxhp)
        current_hpstring=""
        if len(hp_string)<9:
            decreased=9-len(hp_string)
            while decreased >0:
                current_hpstring+=" "
                decreased-=1
            current_hpstring+=hp_string
        else:
            current_hpstring=hp_string

        mp_string=str(self.mp)+"/"+str(self.maxmp)
        current_mpstring=""
        if len(mp_string)<7:
            decreased=7-len(mp_string)
            while decreased>0:
                current_mpstring+=" "
                decreased-=1
            current_mpstring+=mp_string
        else:
            current_mpstring=mp_string
        print("                     ________________________________________            ________________")
        print(bcolors.BOLD +self.name+ "     " +
              current_hpstring+"|" + bcolors.OKGREEN +hp_bar+ bcolors.ENDC + bcolors.BOLD + "|    "
              +current_mpstring+"|" + bcolors.OKBLUE + mp_bar + bcolors.ENDC + "| ")

    def get_enemy_stats(self):
            hp_bar=""
            bar_ticks=(self.hp/self.maxhp)*100/2
            while bar_ticks>0:
                hp_bar+="█"
                bar_ticks-=1
            while len(hp_bar)<50:
                hp_bar+="░"
            hp_string=str(self.hp)+"/"+str(self.maxhp)
            current_hpstring=""
            if len(hp_string)<9:
                decrease=9-len(hp_string)
                while decrease>0:
                    current_hpstring+=" "
                    decrease-=1
                current_hpstring+=hp_string
            else:
                current_hpstring=hp_string
            print("                  _______________________________________________________________________________")
            print(bcolors.BOLD + self.name + " " +
                  current_hpstring + "|" + bcolors.FAIL + hp_bar + bcolors.ENDC + bcolors.BOLD + "|    "
                  + bcolors.ENDC )

    def choose_enemy_magic(self):
        while True:
            choice=int(random.randrange(len(self.magic)))
            spell=self.magic[choice]
            magic_damage=spell.generate_damage()
            pct = (self.hp/self.maxhp)*100
            if  spell.cost>self.mp or spell.type=="white" and pct>50:
                choice=self.choose_enemy_magic()
                continue
            return choice

