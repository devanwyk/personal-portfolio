import time

my_time = int(input("Enter the time in seconds:"))

# for x in reversed(range(0,my_time)):
#     print(x)
#     time.sleep(1)

# print("Time's up!")

for x in range(my_time, 0, -1):
    seconds = x % 60
    minutes = (x // 60) % 60
    hours = (x // 3600) % 24
    if hours > 0:
        print(f"{hours:02}:{minutes:02}:{seconds:02}")
    else:
        print(f"00:{minutes:02}:{seconds:02}")
    time.sleep(1)

print("Time's up for real this time!")