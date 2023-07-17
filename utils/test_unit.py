import random
from sys import argv

# see interactive_test() for idea how this algorithm should be implemented in
# order to pass tests
# run in command line with same arguments as duskers.py for demo


class TestData:
    def __init__(self, explorations: int, searches: int, seed, chosen: int, places: str):
        self.explorations = explorations
        self.searches = searches
        self.seed = seed
        self.chosen = chosen
        self.places = places

def generate(n):
    result = []
    for _ in range(n):
        place_name = random.choice(place_names)
        place_titanium = random.randint(10, 100)
        result.append((place_name, place_titanium))
    return result

def interactive_test():
    no_of_places = random.randint(1, 9)
    print("Number of places:", no_of_places)
    no_of_searches = int(input("How many searches: "))
    print(generate(no_of_searches))
    print()

def test(no_of_searches):
    no_of_places = random.randint(1, 9)
    if no_of_searches > no_of_places:
        no_of_searches = no_of_places
    return generate(no_of_searches)

def init_test(test_case: TestData):
    global place_names
    random.seed(test_case.seed)
    place_names = []
    argv_places = test_case.places.split(",")
    for item in argv_places:
        place = " ".join(item.split("_"))
        place_names.append(place)

    results = []
    for exploration in range(test_case.explorations):
        results.append(test(test_case.searches))
    return results
        


if __name__ == "__main__":

    if len(argv) == 5:
        random.seed(a=argv[1])
        wait_time_min = int(argv[2])
        wait_time_max = int(argv[3])
        place_names = []
        argv_places = argv[4].split(",")
        for item in argv_places:
            place = " ".join(item.split("_"))
            place_names.append(place)
    else:
        print("Incorrect parameters")
        exit()

    while True:
        comm = input("Type 'exit()' to exit or any other character(s) to continue" \
            " testing: ")
        if comm == "exit()":
            break
        interactive_test()
