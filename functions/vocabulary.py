

# patient identity
patientID ={
    "Vorname": "Max",
    "Nachname": "Mustermann",
    "Alter": 46,
    "Diagnose": "Burnout wegen der Arbeitsstress",
    "Stationäreaufenthalt":"30 Tage",
    "Hauptsymptome": ["Schlafstörungen", "Antrieblosigkeit", "Panikattaken"],
    "Hobbys": ["Musik hören", "sport treiben"]
}

# List of regular Munchkin Feedbacks
negativeFeedback =[
    "Das hört sich nicht gut an. Aber keine sorgen, das kannst du noch ändern",
    "Kein problem, Wir haben alle solche Tage.",
    "Das ist ok. Du kannst besser machen",
    "Das ist nicht gut. Das kannst du aber verbessern",
    "Das tut mir leid. Wir kriegen es aber zusammen schon hin.",
    "Kopf hoch. Wir können das noch ändern",
    "Kein Problem. Das kannst du nachholen."
    ]

positiveFeedback = [
    "Prima. Weiter so",
    "Gut zu hören.",
    "Wunderbar.",
    "Das freut mich für dich.",
    "Das hast du sehr gut gemacht.",
    "Das ist Klasse. Weiter so.",
    "Hut ab. Weiter so."
]

# List of possible user answers (probable spoken words relevant to guess user's mood)
positiveFeeling = ["ich fühle mich prima Heute", "Ich fühle mich gut", "Ich fühle mich ok",
                  "Es geht mir gut", "hervorragend","nicht schlecht", "gut","prima","klasse","sehr gut", "super"]
negativeFeeling = ["ich fühle mich schlecht", "ich fühle mich nicht gut", "träge", "ich fühle mich träge", "mir geht's schlecht",
                   "beschissen", "schlecht", "es geht so", "verbesserungswürdig","es geht mir schlecht", "nicht gut", "sehr schlecht"]

negativeAnswer = ["nicht gut", "schlecht", "kein antrieb","nie gut"
                "keine motivation", "keine energie", "unmotiviert"]
suicidalBehavior = ["ich bin nutzlos", "sterben", "hasse mich", "ich töte euch", "ich töte mich", "töten", "töte", "ich habe kein wert",
                    "ich bin wertlos", "ich hasse die Welt", "hoffnungslos", "ich hasse ecuh alle ", "ich will nicht leben", "grab", "ich sehe keine hoffnung"]


askForMotivation = ["Wie kann ich mein Mood verbessern?", "Wie kann ich positiv Denken?", "Gib mir ideen.", "mood verbessern"]

needHELP = ["SOS", "ich bin im not", "notruf schalten", "ich brauche hilfe"]

bedYes =["ja", "ich bin schon wach", "ja bin aufgestanden"]
bedNo = ["ne", "nein", "ich hänge noch im bett", "noch im bett"]
sleepGoodYes=["ja", "sehr gut", "prima", "ich habe gut geschlafen", "gut geschlafen","sehr erholsam", "sehr tief geschlafen", "tief geschlafen"]
sleepGoodNo=["nein", "leider nicht", "sehr schlecht geschlafen", "unterbrochen", "bin wach geblieben", "wach"]