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
        print("\n> Weighing #{}".format(self.usage))
        print("Checking coins {} (Left) against coins {} (Right)...".format(
            [coin.number for coin in left], [coin.number for coin in right]))
        if left_weight == right_weight:
            print("Both sides are balanced", end=" ")
            return "BALANCED"
        else:
            print("{} side is heavier".format(
                "Left" if left_weight - right_weight > 0 else "Right"), end=" ")
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
        print("so we can ignore coins 9–12 now.\nLet's keep coins 7 & 8 aside and swap coins 3, 4 & 6 to their opposide sides.")
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
        print("")
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
        print("\nThe fake coin will be the one that caused the scale to tip in the direction consistent with the second weighing.")
        return coins[0]
    else:
        print("\nThe fake coin will be the one that caused the scale to tip in the direction consistent with the second weighing.")
        return coins[1]


print("======================================")
print("Welcome to the Counterfeit Coin Puzzle")
print("======================================")
print("\nPlease select an option:")
print("1 - Run a single random simulation")
print("2 - Run a single simulation where you specify the fake coin")
print("3 - Run through all possible outcomes")
print("4 - Run several random trials")

while True:
    selection = input("\nEnter number: ")
    try:
        if selection == "" or int(selection) == 1:
            fake_num = random.randint(0, 11)
            trials = 1
            break
        elif int(selection) == 2:
            fake_num = int(input("Which coin should be the fake? (1-12)"))-1
            trials = 1
            break
        elif int(selection) == 3:
            fake_num = -1
            trials = 12
            break
        elif int(selection) == 4:
            fake_num = -2
            trials = int(input("How many random trials? "))
            break
        else:
            print("\n>> Invalid input")
    except:
        print("\n>> Invalid input")

print("")
for i in range(trials):
    print("--------")
    print("TRIAL {}".format(i+1))
    print("--------")
    coins = [Coin(i+1) for i in range(12)]
    if fake_num == -1:  # Sequential
        coins[i].set_fake()
    elif fake_num == -2:  # Random
        coins[random.randint(0, 11)].set_fake()
    else:
        coins[fake_num].set_fake()

    deduced_fake = solve_all_coins(coins)
    print("\nThe fake coin must be Coin {}".format(deduced_fake.number))
    if deduced_fake.is_fake:
        print("Correct!\n")
    else:
        print("Oops, that is WRONG!\n")
        break
