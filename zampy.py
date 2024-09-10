import pickle as p
import random as r
import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
from tkinter import simpledialog

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

def make_menu_from_options(options: list = ['Yes', 'No'], dictVersion = False) -> str:
    final = ""
    dictv = dict()
    while None in options:
        options.remove(None)
    if dictVersion:
        for index in range(1, len(options) + 1):
            final += f"{index}: {options[index - 1]}\n"
            dictv[index] = options[index - 1]
        return final, dictv
    else:
        for index in range(1, len(options) + 1):
            final += f"{index}: {options[index - 1]}\n"
        return final

def check_record_exists(checkingParameter, indexInRecord, tableData) -> tuple:
    for record in tableData:
        if record[indexInRecord] == checkingParameter:
            return True, record
    return False, None

def checkEmpty(iterable) -> bool:
    return True if len(iterable) == 0 else False

import tkinter as tk
from tkinter import ttk, simpledialog
from tkcalendar import Calendar

def choose_date():
    """Open a graphical popup to select a date. Returns date in 'YYYY-MM-DD' format."""
    root = tk.Tk()
    
    root.withdraw()  # Hide the main window

    # Create a new window for the calendar
    top = tk.Toplevel(root)
    top.title("Choose Date")
    top.focus()
    cal = Calendar(top, selectmode='day', date_pattern='y-mm-dd')
    cal.pack(padx=10, pady=10)

    def on_date_selected():
        selected_date = cal.get_date()  # Get selected date in 'YYYY-MM-DD'
        top.destroy()  # Close the date picker window
        root.quit()  # Quit the mainloop
        return selected_date

    ttk.Button(top, text="Select Date", command=on_date_selected).pack(pady=10)
    
    root.mainloop()
    return cal.get_date()

def choose_time():
    """Open a graphical popup to input time. Returns time in 'HOURS:MINUTES:SECONDS' format."""
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    root.focus_force()
    #root.focus()
    # Get user input for hours, minutes, and seconds
    hours = simpledialog.askstring("Input Time", "Enter hours (HH):", parent=root)
    minutes = simpledialog.askstring("Input Time", "Enter minutes (MM):", parent=root)
    #seconds = simpledialog.askstring("Input Time", "Enter seconds (SS, optional):", parent=root)

    # Validate the inputs and format the time
    if hours is None or minutes is None:
        return None
    time_str = f"{hours.zfill(2)}:{minutes.zfill(2)}"

    
    root.quit()
    return time_str