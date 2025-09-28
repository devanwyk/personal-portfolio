principle = 0
rate = 0
time = 0

while True:
    principle = float(input("Enter the principle amount: "))
    if principle <= 0:
        print("Principle must be positive.")
    else:
        break

while True:
    rate = float(input("Enter the rate of interest: "))
    if rate <= 0:
        print("Rate must be positive.")
    else:
        break

while True:
    time = float(input("Enter the time period (in years): "))
    if time <= 0:
        print("Time must be positive.")
    else:
        break

total = principle * pow(1 + rate / 100, time)
print(f"Balance after {time} years: {total:.2f}")