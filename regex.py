import re
from datetime import datetime, timedelta

motif = re.compile(r"(?P<date>\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2}\s+\d{2}:\d{2}:\d{2}\b).*Failed password for (?P<invalid_user>invalid user )?(?P<user>\w+) from (?P<IP>\d+\.\d+\.\d+\.\d+)")

compteurs = {}
seuil = 3
delta = timedelta(seconds=10)

with open("/home/elyak/Dev/projet-cybersecu/sample.log", "r", encoding="utf-8") as file:
    for line in file:
        match = re.search(motif, line)
        if match:
            date_texte = match.group("date")
            date_avec_annee = f"{datetime.now().year} {date_texte}"
            user = match.group("user")
            IP = match.group("IP")
            date = datetime.strptime(date_avec_annee, "%Y %b %d %H:%M:%S")
            if IP in compteurs:
                compteurs[IP].append(date)
            else:
                compteurs[IP] = [date]
for IP, dates in compteurs.items():
    total = len(dates)
    print(f"IP: {IP}, Failed Attempts: {total}")
    for debut in dates:
        date_fin = debut + delta
        count = sum(1 for d in dates if debut <= d <= date_fin)
        if count >= seuil:
            print(f"Alert: IP {IP} has more than {seuil} failed login attempts!")
            print(f"Dates of failed attempts: {', '.join(date.strftime('%Y-%m-%d %H:%M:%S') for date in dates)}")
            break