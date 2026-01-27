from datetime import timedelta

while True:
    time = input("HH.MM.SS:\n")
    time = time.split(".")
    hrs, mins, secs = map(int, time)
    duration = timedelta(hours=hrs, minutes=mins, seconds=secs)

    for i in range(100, 0, -10):
        result = duration * (i/100)
        index = str(result).find(".")
        if index == -1:
            print(f"{i}% of {duration} is {str(result)}")
        else:
            print(f"{i}% of {duration} is {str(result)[:index]}")
    print()