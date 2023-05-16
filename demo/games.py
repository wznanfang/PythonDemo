import random


# 猜数字游戏
def game1():
    number = random.randint(1, 10)
    chances = 3
    while chances > 0:
        guess = int(input("请输入一个介于1到10的整数: "))
        if guess == number:
            print("恭喜你猜对了!")
            break
        else:
            chances -= 1
            hint = "大"
            if number < guess:
                hint = "小"
            print("抱歉,你猜错啦,数字比", guess, hint, ",你还有", chances, "机会")
    if chances == 0:
        print("游戏结束，答案是：", number)


if __name__ == "__main__":
    game1()
