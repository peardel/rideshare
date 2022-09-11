import math
import random

EARTH_RADIUS = 6371 # in km
def lat_lon_euclidean_dist(lat1: float, lon1: float, lat2: float, lon2: float, use_radians:bool=False) -> float:
    """
        d = acos( sin φ1 ⋅ sin φ2 + cos φ1 ⋅ cos φ2 ⋅ cos Δλ ) ⋅ R 
        lat/longs should be in degrees,
        distance will be given in km
    """
    if not use_radians:
        lat1, lon1, lat2, lon2 = (math.radians(x) for x in (lat1, lon1, lat2, lon2))
    return math.acos( math.sin(lat1)*math.sin(lat2) + math.cos(lat1)*math.cos(lat2)*math.cos(lon2-lon1) ) * EARTH_RADIUS


FIRST_NAMES = ["Liam", "Noah", "Oliver", "Elijah", "James", "William", "Benjamin", "Lucas", "Henry", "Theodore", "Jack", "Levi", "Alexander", "Jackson", "Mateo", "Daniel", "Michael", "Mason", "Sebastian", "Ethan", "Logan", "Owen", "Samuel", "Jacob", "Asher", "Aiden", "John", "Joseph", "Wyatt", "David", "Leo", "Luke", "Julian", "Hudson", "Grayson", "Matthew", "Ezra", "Gabriel", "Carter", "Isaac", "Jayden", "Luca", "Anthony", "Dylan", "Lincoln", "Thomas", "Maverick", "Elias", "Josiah", "Charles", "Caleb", "Christopher", "Ezekiel", "Miles", "Jaxon", "Isaiah", "Andrew", "Joshua", "Nathan", "Nolan", "Adrian", "Cameron", "Santiago", "Eli", "Aaron", "Ryan", "Angel", "Cooper", "Waylon", "Easton", "Kai", "Christian", "Landon", "Colton", "Roman", "Axel", "Brooks", "Jonathan", "Robert", "Jameson", "Ian", "Everett", "Greyson", "Wesley", "Jeremiah", "Hunter", "Leonardo", "Jordan", "Jose", "Bennett", "Silas", "Nicholas", "Parker", "Beau", "Weston", "Austin", "Connor", "Carson", "Dominic", "Xavier", "Jaxson", "Jace", "Emmett", "Adam", "Declan", "Rowan", "Micah", "Kayden", "Gael", "River", "Ryder", "Kingston", "Damian", "Sawyer", "Luka", "Evan", "Vincent", "Legend", "Myles", "Harrison", "August", "Bryson", "Amir", "Giovanni", "Chase", "Diego", "Milo", "Jasper", "Walker", "Jason", "Brayden", "Cole", "Nathaniel", "George", "Lorenzo", "Zion", "Luis", "Archer", "Enzo", "Jonah", "Thiago", "Theo", "Ayden", "Zachary", "Calvin", "Braxton", "Ashton", "Rhett", "Atlas", "Jude", "Bentley", "Carlos", "Ryker", "Adriel", "Arthur", "Ace", "Tyler", "Jayce", "Max", "Elliot", "Graham", "Kaiden", "Maxwell", "Juan", "Dean", "Matteo", "Malachi", "Ivan", "Elliott", "Jesus", "Emiliano", "Messiah", "Gavin", "Maddox", "Camden", "Hayden", "Leon", "Antonio", "Justin", "Tucker", "Brandon", "Kevin", "Judah", "Finn", "King", "Brody", "Xander", "Nicolas", "Charlie", "Arlo", "Emmanuel", "Barrett", "Felix", "Alex", "Miguel", "Abel", "Alan", "Beckett", "Amari", "Karter"]
LAST_NAMES = ["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor", "Anderson", "Thomas", "Jackson", "White", "Harris", "Martin", "Thompson", "Garcia", "Martinez", "Robinson", "Clark", "Rodriguez", "Lewis", "Lee", "Walker", "Hall", "Allen", "Young", "Hernandez", "King", "Wright", "Lopez", "Hill", "Scott", "Green", "Adams", "Baker", "Gonzalez", "Nelson", "Carter", "Mitchell", "Perez", "Roberts", "Turner", "Phillips", "Campbell", "Parker", "Evans", "Edwards", "Collins", "Stewart", "Sanchez", "Morris", "Rogers", "Reed", "Cook", "Morgan", "Bell", "Murphy", "Bailey", "Rivera", "Cooper", "Richardson", "Cox", "Howard", "Ward", "Torres", "Peterson", "Gray", "Ramirez", "James", "Watson", "Brooks", "Kelly", "Sanders", "Price", "Bennett", "Wood", "Barnes", "Ross", "Henderson", "Coleman", "Jenkins", "Perry", "Powell", "Long", "Patterson", "Hughes", "Flores", "Washington", "Butler", "Simmons", "Foster", "Gonzales", "Bryant", "Alexander", "Russell", "Griffin", "Diaz", "Hayes"]
def get_random_name() -> str:
    return f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"

def time_string_to_int(time_str: str) -> int:
    hours, mins = [int(x) for x in time_str.split(":")]
    return hours*60 + mins

def int_to_time_string(time_int: int) -> str:
    hours, mins = [str(x) for x in (time_int // 60, time_int % 60)]
    return f"{hours.zfill(2)}:{mins.zfill(2)}"