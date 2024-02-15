import random

class NumberGuessingGame:
    def __init__(self):
        self.digits = 0
        self.answer = []

    def get_user_input(self):
        self.digits = int(input("請輸入要猜的數字位數(3~5位數): "))

    def generate_answer(self):
        digits_range = list(range(1, 10))
        self.answer = random.sample(digits_range, self.digits)

    def play_game(self):
        while True:
            user_guess = input("請猜一個{}位數字: ".format(self.digits))
            user_guess = [int(digit) for digit in user_guess]

            if len(user_guess) != self.digits:
                print("輸入的數字位數不正確，請重新輸入。")
                continue

            a_count = 0
            b_count = 0

            for i in range(self.digits):
                if user_guess[i] == self.answer[i]:
                    a_count += 1
                elif user_guess[i] in self.answer:
                    b_count += 1

            print("{}A{}B".format(a_count, b_count))

            if a_count == self.digits:
                print("恭喜你猜中了！")
                break

game = NumberGuessingGame()
game.get_user_input()
game.generate_answer()
game.play_game()