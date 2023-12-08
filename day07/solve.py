
class Hand:
    cards=['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
    cards_with_joker=['A', 'K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3', '2', 'J']
    
    def __init__(self,input:str):
        self.string=input.split(' ')[0]
        self.bid=int(input.split(' ')[1])
        self.update_score_without_joker(self.string)
    
    def __eq__(self,other):
        return self.string==other.string
    
    def __lt__(self,other):
        if self.score<other.score:
            return True
        elif self.score>other.score:
            return False
        for c1,c2 in zip(list(self.string),list(other.string)):
            if Hand.cards.index(c1)>Hand.cards.index(c2):
                return True
            elif Hand.cards.index(c1)<Hand.cards.index(c2):
                return False
        return False

    def jocker_lt(self,other):
        if self.score<other.score:
            return True
        elif self.score>other.score:
            return False
        for c1,c2 in zip(list(self.string),list(other.string)):
            if Hand.cards_with_joker.index(c1)>Hand.cards_with_joker.index(c2):
                return True
            elif Hand.cards_with_joker.index(c1)<Hand.cards_with_joker.index(c2):
                return False
        return False
    
    def update_score_without_joker(self,string:str):
        ordered_chars=sorted(string)
        diffs=list(map(lambda a,b:Hand.cards.index(a)-Hand.cards.index(b), ordered_chars[1:], ordered_chars[:-1]))
        indexes = [i for i, x in enumerate(diffs) if x == 0]
        if len(indexes)==4:
            self.score=7
        elif len(indexes)==3:
            if indexes[0]+1==indexes[1]==indexes[2]-1:
                self.score=6
            else:
                self.score=5
        elif len(indexes)==2:
            if indexes[1]-indexes[0]==1:
                self.score=4
            else:
                self.score=3
        elif len(indexes)==1:
            self.score=2
        else:
            self.score=1
        
    def update_score_with_joker(self):
        string=self.string
        different_cards=set(string)
        if 'J' in different_cards:
            different_cards.remove('J')
        if len(different_cards)==0:
            different_cards.add('A')
        most_frequent = max(different_cards, key = string.count)
        string=string.replace('J',most_frequent)
        self.update_score_without_joker(string)
    
    def __str__(self):
        return f"Hand {self.string} of type {self.score} -> bid {self.bid}"


def solve_1(data: list[str]) -> int:
    hands=[Hand(string) for string in data]
    hands.sort()
    #for hand in hands:
    #    print(hand)
    from functools import reduce
    return reduce(lambda total_score, next: total_score+(next[0]+1)*next[1].bid,enumerate(hands),0)

def cmp_2_hands(hand1, hand2)->int:
    if hand1==hand2:
        return 0
    elif hand1.jocker_lt(hand2):
        return -1
    return 1

def solve_2(data: list[str]) -> int:
    hands=[Hand(string) for string in data]
    for hand in hands:
        hand.update_score_with_joker()
    from functools import cmp_to_key
    hands.sort(key=cmp_to_key(cmp_2_hands))
    for hand in hands:
        print(hand)
    from functools import reduce
    return reduce(lambda total_score, next: total_score+(next[0]+1)*next[1].bid,enumerate(hands),0)

