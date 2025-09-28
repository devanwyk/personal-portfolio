

for x in reversed(range(1,11)):
    print(x)

print("HAPPY NEW YEAR!")


credit_card = "1234-5678-9876-5432"

for i in range(len(credit_card)-4):
    credit_card = credit_card.replace(credit_card[i], '*', 1)
print(credit_card)

for x in range(1,21):
    if x == 13:
        continue
    else:
        print(x)