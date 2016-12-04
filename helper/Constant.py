import datetime

TV_CHANNELS = ["NBC",
               "CBS",
               "QVC",
               "ABC",
               "ESPN",
               "Fox",
               "HBO",
               "TNT",
               "HSN",
               "NICKELODEON",
               "SHOWTIME",
               "USA",
               "MTV",
               "CNN",
               "TBS",
               "LIFETIME",
               "DISCOVERY",
               "THE WB",
               "SHOPNBC",
               "DISNEY",
               "FOX NEWS",
               "A&E",
               "CINEMAX",
               "UNIVISION",
               "TLC"]

# GENRES = ["Comedy", "News", "Drama", "Fiction", "Sports", "Science", "History"]
PROGRAMS = [("Science", "Planet Earth II"),
            ("Drama", "Fiction", "Band of Brothers"),
            ("Science", "Planet Earth"),
            ("Drama", "Fiction", "Breaking Bad"),
            ("Drama", "Fiction", "Game of Thrones"),
            ("Drama", "Fiction", "The Wire"),
            ("Science", "Cosmos: A Spacetime Odyssey"),
            ("Comedy", "Fiction", "Rick and Morty"),
            ("Comedy", "Fiction", "Drama", "FRIENDS"),
            ("Comedy", "Fiction", "Drama", "The Silicon Valley"),
            ("Fiction", "Drama", "Sherlock"),
            ("News", "Prime Time"),
            ("Science", "Life"),
            ("History", "The Civil War"),
            ("History", "The World at War"),
            ("Science", "Avatar: The Last Airbende"),
            ("Drama", "Westworld"),
            ("News", "Comedy", "Last Week Tonight with John Olive"),
            ("Comedy", "Fiction", "Drama", "TVF Pitchers"),
            ("Science", "Human Planet"),
            ("Sports", "Olympics"),
            ("Drama", "Fiction", "Prison Break")]

AIR_TOTAL_HR = 30*24
TODAY = datetime.datetime.today()
VWR_DB_FILE="viewer.json"
CHN_DB_FILE="channel.json"
PGM_DB_FILE="program.json"
AIR_DB_FILE="airing.json"
VSHIP_DB_FILE="viewership.json"
