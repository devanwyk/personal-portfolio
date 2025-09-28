# Python quiz game

questions = ("How many elements are in the periodic table?: ",
             "Which animal lays the largest eggs?: ",
             "What is the capital of Australia?: ",
             "What is the most abundant gas in the Earth's atmosphere?: ",
             "How many bones are in the human body?: ",
             "Which planet in the solar system is the hottest?: ")

options = (("A. 118", "B. 98", "C. 108", "D. 128"),
           ("A. Hydrogen", "B. Helium", "C. Lithium", "D. Beryllium"),
           ("A. Ostrich", "B. Eagle", "C. Penguin", "D. Sparrow"),
           ("A. Canberra", "B. Sydney", "C. Melbourne", "D. Brisbane"),
           ("A. 206", "B. 305", "C. 106", "D. 156"),
           ("A. Venus", "B. Mars", "C. Jupiter", "D. Saturn"))

answers = ("A", "A", "A", "B", "A", "A")
guesses = []
score = 0
question_num = 0

for question in questions:
    print("-------------------------")
    print(question)
    for option in options[question_num]:
        print(option)
    guess = input("Enter (A, B, C, or D): ").upper()
    guesses.append(guess)

    if guess == answers[question_num]:
        score += 1
        print("CORRECT!")
    else:
        print("WRONG!")
        print(f"The correct answer is: {answers[question_num]}")
    question_num += 1

print("answers: ", end="")
for answer in answers:
    print(answer, end=" ")
print()

print("guesses: ", end="")
for guess in guesses:
    print(guess, end=" ")
print()

score = int(score / len(questions) * 100)
print(f"Your score is: {score}%")