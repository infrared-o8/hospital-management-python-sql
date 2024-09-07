import pickle as p
import random as r

names = [
"Arbor",
"Ash",
"Charlie",
"Drew",
"Ellis",
"Everest",
"Jett",
"Lowen",
"Moss",
"Oakley",
"Onyx",
"Phoenix",
"Ridley",
"Remy",
"Robin",
"Royal",
"Sage",
"Scout",
"Tatum",
"Wren",
"Jessie",
"Marion",
"Alva",
"Ollie",
"Cleo",
"Kerry",
"Guadalupe",
"Carey",
"Tommie",
"Sammie",
"Jamie",
"Kris",
"Robbie",
"Tracy",
"Merrill",
"Noel",
"Rene",
"Johnnie",
"Ariel",
"Jan",
"Casey",
"Jackie",
"Kerry",
"Jodie",
"Rene",
"Darian",
"Robbie",
"Milan",
"Jaylin",
"Devan",
"Channing",
"Gerry",
"Monroe",
"Kirby",
"Santana",
"Adair",
"Aubrey",
"Bailey",
"Bellamy",
"Bentley",
"Blair",
"Bowie",
"Campbell",
"Cassidy",
"Cedar",
"Colby",
"Courtney",
"Dallas",
"Dale",
"Darcy",
"Echo",
"Gray",
"Greer",
"Harley",
"Haven",
"Holland",
"Hollis",
"Indigo",
"Kendall",
"Kit",
"Lane",
"Lennox",
"London",
"Loyal",
"Luxury",
"Lyric",
"Marley",
"Morgan",
"Navy",
"Ocean",
"Palmer",
"Peyton",
"Presley",
"Raleigh",
"Reagan",
"Reef",
"Reese",
"Rory",
"Salem",
"Sawyer",
"Shea",
"Shiloh",
"Sidney",
"Sloan",
"Story",
"Sutton",
"Taran",
"Taylor",
"Zion",
]
sports = [
    "Basketball", "Football", "Soccer", "Tennis", "Baseball", "Cricket",
    "Golf", "Rugby", "Hockey", "Badminton", "Volleyball", "Table Tennis",
    "Swimming", "Athletics", "Boxing", "Martial Arts", "Cycling",
    "Ice Hockey", "Field Hockey", "Softball", "Wrestling", "Skiing",
    "Snowboarding", "Surfing", "Skateboarding", "Gymnastics", "Diving",
    "Archery", "Fencing", "Weightlifting", "Rowing", "Canoeing", "Kayaking",
    "Sailing", "Water Polo", "Handball", "Polo", "Lacrosse", "Squash",
    "Pickleball", "Badminton", "Curling", "Bobsleigh", "Skeleton",
    "Biathlon", "Triathlon", "Decathlon", "Pentathlon", "Equestrian",
    "Bouldering", "Mountaineering", "Rock Climbing", "Paragliding",
    "Hang Gliding", "Skydiving", "Bungee Jumping", "Parkour"
]
genres = [
    "Action", "Adventure", "Animation", "Biography", "Comedy",
    "Crime", "Documentary", "Drama", "Family", "Fantasy",
    "Film Noir", "History", "Horror", "Music", "Musical",
    "Mystery", "Romance", "Sci-Fi", "Sport", "Thriller",
    "War", "Western", "Biographical", "Educational", "Experimental"
]

def user_intlist() -> list:
    '''
    Prompts the user to input a specified number of integers and returns them as a list.
    '''
    l = []
    n = int(input("Number of elements: "))
    try:
        for i in range(n):
            l.append(int(input(f"Element {i}: ")))
        print("current list:", l)
        return l
    except Exception as e:
        print("Error:", e)
        return None

def user_strlist() -> list:
    '''
    Prompts the user to input a specified number of strings and returns them as a list.
    '''
    l = []
    n = int(input("Number of elements: "))
    for i in range(n):
        l.append(str(input(f"Element {i}: ")))
    print("current list:", l)
    return l

def rsort(a: list = [1, 2, 3], debug: bool = True) -> tuple:
    '''
    Sorts a list in descending order and returns the largest and smallest elements.
    '''
    try:
        a.sort(reverse=True)
        l = a[0]
        s = a[len(a) - 1]
        if debug:
            print("largest: ", l, "| smallest: ", s)
        return l, s
    except Exception as e:
        print(f"Error: {e}")
        return None

def random_name(n: int = 2) -> str:
    '''
    Generates a random name with a 'n' number of words.
    '''
    chosen = [r.choice(names) for i in range(n)]
    return " ".join(chosen)

def random_number(digits: int = 3, multipleOfTen: bool = True) -> int:
    '''
    Generates a random number with a specified number of digits.
    
    multipleOfTen (bool): If True, generates a number that is a multiple of ten.
    '''
    if multipleOfTen:
        return r.randint(1, 9) * (10**digits)
    return r.randint(1 * (10 ** digits), 9 * (10**digits))

def random_age(min: int = 10, max: int = 60) -> int:
    '''
    Generates a random age within the specified range.
    '''
    return r.randint(min, max)

def random_sport() -> str:
    '''
    Returns a random sport.
    '''
    return r.choice(sports)

def create_file_with_data(file_name="test1", file_type='.dat', data='Lorem ipsum dolor sit amet.'):
    '''
    Creates a file with the specified name and type, and writes the provided data to it. Returns None if error.
    
    data (str): The data to be written to the file.
    '''
    try:
        if file_type.lower() == ".dat":
            p.dump(data, open(file_name+file_type, "wb"))
    except Exception as e:
        print(f"Error: {e}")
        return None

def random_genre() -> str:
    '''
    Returns a random genre.
    '''
    return r.choice(genres)
