import random


class Coin():
    def __init__(self, number, fake=False):
        self.number = number
        self.is_fake = fake
        self.weight = 1 + random.choice([-0.1, 0.1]) * fake

    def set_fake(self):
        self.is_fake = True
        self.weight = 1 + random.choice([-0.1, 0.1])

    def __str__(self):
        return "Coin #{} {}".format(
            self.number, "[FAKE] (Weight {})".format(self.weight) if self.is_fake else "")

    def __repr__(self):
        return "Coin #{} {}".format(
            self.number, "[FAKE] (Weight {})".format(self.weight) if self.is_fake else "")


class Balance_Scale():
    def __init__(self, max_usage=3):
        self.usage = 0
        self.max_usage = max_usage

    def weigh_coins(self, left, right):
        if len(set([coin.number for coin in left] + [coin.number for coin in right])) != len(left) + len(right):
            raise Exception("Can't have same coin on both sides of balance")
        if self.usage >= self.max_usage:
            raise Exception("Balance scale has exceeded maximum usage!")
        left_weight = sum([coin.weight for coin in left])
        right_weight = sum([coin.weight for coin in right])
        self.usage += 1
        print("\nWeighing #{}".format(self.usage))
        print("Checking coins {} (Left) against coins {} (Right)...".format(
            [coin.number for coin in left], [coin.number for coin in right]))
        if left_weight == right_weight:
            print("Both sides are balanced")
            return "BALANCED"
        else:
            print("{} side is heavier".format(
                "Left" if left_weight - right_weight > 0 else "Right"))
            return "LEFT" if left_weight - right_weight > 0 else "RIGHT"


def solve_all_coins(coins):
    scale = Balance_Scale()
    if len(coins) != 12:
        raise Exception("Can only solve for TWELVE coins!")
    # 1st weighing
    result1 = scale.weigh_coins(coins[0:4], coins[4:8])
    if result1 == "BALANCED":
        print("so we know fake is amongst coins 9–12.")
        return solve_four_coins(coins[8:12], scale)
    else:
        print("so now we'll keep coins 7 & 8 aside and")
        print("swap coins 3, 4 & 6 to their opposide sides.")
        return solve_eight_coins(coins[0:8], result1, scale)


def solve_four_coins(coins, scale):
    if len(coins) != 4:
        raise Exception("Can only solve for FOUR coins!")
    # 2nd weighing
    result2 = scale.weigh_coins([coins[0]], [coins[1]])
    if (result2 == "BALANCED"):
        # 3rd weighing
        print("Therefore fake is either 11 or 12.")
        result3 = scale.weigh_coins([coins[2]], [coins[0]])
        if result3 == "BALANCED":
            return coins[3]
        else:
            return coins[2]
    else:
        # 3rd weighing
        result3 = scale.weigh_coins([coins[0]], [coins[2]])
        if result3 == "BALANCED":
            return coins[1]
        else:
            return coins[0]


def solve_eight_coins(coins, result1, scale):
    if len(coins) != 8:
        raise Exception("Can only solve for EIGHT coins!")
    new_left = coins[0:2] + [coins[5]]
    new_right = coins[2:4] + [coins[4]]
    # 2nd weighing
    result2 = scale.weigh_coins(new_left, new_right)
    if result2 == "BALANCED":
        print("so the fake must be either 7 or 8.")
        # 3rd weighing
        result3 = scale.weigh_coins([coins[6]], [coins[0]])
        if result3 == "BALANCED":
            return coins[7]
        else:
            return coins[6]
    if result2 == result1:
        print("so the fake must be one of the non-swapped coins (1, 2 or 5),\nsince the scale tipped the same way.")
        return solve_final_three_coins(coins[0:2] + [coins[4]], result2, scale)
    else:
        print("so the fake must be one of the swapped coins (3, 4 or 6),\nsince the scale tipped the other way this time.")
        # Fake is among swapped coins (i.e. 3, 4, 6)
        return solve_final_three_coins(coins[2:4] + [coins[5]], "RIGHT" if result2 == "LEFT" else "LEFT", scale)


def solve_final_three_coins(coins, result2, scale):
    # 3rd weighing
    result3 = scale.weigh_coins([coins[0]], [coins[1]])
    if result3 == "BALANCED":
        return coins[2]
    elif result3 == result2:
        print("The fake coin will be the one that caused the scale to tip\nin the direction consistent with the second weighing.")
        return coins[0]
    else:
        print("The fake coin will be the one that caused the scale to tip\nin the direction consistent with the second weighing.")
        return coins[1]


for i in range(12):
    coins = [Coin(i+1) for i in range(12)]
    # coins[random.randint(0, 11)].set_fake()
    coins[i].set_fake()

    deduced_fake = solve_all_coins(coins)
    print("The fake coin must be Coin {}".format(deduced_fake.number))
    if deduced_fake.is_fake:
        print("Correct!\n")
    else:
        print("Oops, that is WRONG!\n")
        break
