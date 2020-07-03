
import speech_recognition as sr
import os
import time
import random
import vocabulary
import tensorflow
import keras

session = {
    "feeling": "init",
    "Bad":"init",
    "Sleep": "init",
    "outside": "init",
    "eat":   "init",
    "burnout": "init",
    "State": "init"
}

intent = "yesFeedback"
def main():
    print(motivationideas())
    speech = speechtotext()
    time.sleep(0.5)
    #if 'ok' in speech:
    os.system('say ' + welcome() + vocabulary.patientID["Vorname"])
    speech = speechtotext()
    if any(s in speech for s in vocabulary.positiveFeeling):
        os.system('say ' + random.choice(vocabulary.positiveFeedback))
        time.sleep(1)
        os.system('say "Brauchst du sonst noch etwas wo ich helfen kann ?"')
        session["feeling"]="Good"
        session["State"]="Question 0 answered"
    elif any(s in speech for s in vocabulary.negativeFeeling):
        session["feeling"] = "Bad"
        session["State"] = "Question 1 answered"
        os.system('say ' + random.choice(vocabulary.negativeFeedback))
        time.sleep(1)
        os.system('say "Bist du heute aus dem Bett gekommen?"')
    speech = speechtotext()
    if "ja" in speech:
        if session["feeling"] == "Good":
            session["State"] = "motivation"
            os.system('say "ok was kann ich für dich tun? Brauchst du eine weitere Motivationsidee?" ')
        else:
            session["State"] = "Question 2 answered"
            session["Bad"] = "yes"
            os.system('say ' "Das ist Prima.")
            time.sleep(1)
            os.system('say ' "Hast du Gestern gut geschlafen?")
    elif "nein" or "ne" in speech:
        if session["feeling"] == "Good":
            os.system('say "ok auf Wiesderhören" ')
            session["State"] = "end"
        else:
            session["State"] = "Question 2 answered"
            session["Bad"] = "no"
            os.system('say ' "Das ist Schlecht. Du kannst besser machen")
            time.sleep(1)
            os.system('say ' "Hast du Gestern gut geschlafen?")


    speech = speechtotext()
    if "ja" in speech and session["State"] == "motivation":
        os.system('say ' + motivationideas())
        time.sleep(0.5)
        os.system('say ' + "Ich wünsche dir ein schönen Tag und bis sehr Bald.")

    if session["State"] == "Question 2 answered":
        if any(s in speech for s in vocabulary.sleepGoodYes):
            session["State"] = "Question 3 answered"
            session["Sleep"] = "yes"
            os.system('say ' + "Super, Das freut mich zu hören.")
            time.sleep(0.5)
            os.system('say ' "Bist du die letzte Tage rausgegangen?")
        else:
            session["State"] = "Question 3 answered"
            session["Sleep"] = "no"
            os.system('say ' + "Schade. Versuche aber demnächst früher ins Bett zu gehen. ")
            time.sleep(0.5)
            os.system('say ' "Bist du die letzte Tage rausgegangen?")
        speech=speechtotext()
        if "ja" in speech:
            os.system('say ' + "Das hast du sehr gut gemacht. Weiter so!")
            session["outside"] = "yes"
        else:
            session["outside"] = "no"
            os.system('say ' + "Das tut mir leid. Du solltest demnächst versuchen öfter rauszugehen und dich mit Freunde treffen!")
    session["state"] = "end"
    if session["Bad"] == "yes" and session["Sleep"] == "yes" and session["outside"] == "yes":
        time.sleep(1)
        text = "Gute Arbeit bei all diesen Dingen. Wenn Sie depressiv sind, können diese kleinen Dinge am schwierigsten sein"
        os.system('say '+ text)
        time.sleep(0.5)
        os.system('say ' + "Mach weiter so"+ vocabulary.patientID["Vorname"]+ "  .Habe de ehre")
    elif session["Bad"] =="no" and session["Sleep"] == "no" or session["outside"]== "no":
        time.sleep(1)
        os.system('say ' + "Beim nächsten einchecken musst du besser machen. Das schaffst du schon. Da bin ich mir sicher")
        time.sleep(0.5)
        os.system('say ' + "Auf wiedersehen"+ vocabulary.patientID["Vorname"])
def speechtotext():
    r = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        r.adjust_for_ambient_noise(source, duration=0.5)
        audio = r.listen(source)
    s = r.recognize_google(audio, language="de-DE")
    #s = r.recognize_sphinx(audio, language="en-US")
    try:
      print("Benutzer sagt:" + s)
    except sr.UnknownValueError:
      print("Audio input ist nicht verständlich")
    except sr.RequestError as e:
      print("Could not request results;{0}".format(e))
    return s


# functions that will be called during the conversation

def welcome():
    gruss = ["Hallo,", "Servus,", "Hi,",
             "Habe die Ehre, ", "Guten Tag, ", "Grüß Gott, ","schön von dir zu hören, "]
    anfrage=["Wie hast du dich die letzten Tage gefühlt?",
             "Wie gehts dir Heute?", "Wie läuft dein Tag?", "wie ging es dir die letzte Tage?"]
    welcome = (random.choice(gruss) + " " + (random.choice(anfrage)))
    print("Willkomen text ist : " + welcome)
    return welcome


def motivationideas():
    ideas =[" Du kannst dir zum beispiel eine to do Liste für die Woche erstellen. Das hilft dir organisatorisch weiter",
            "Du kannst zum beispiel eine neue rezept kochen",
            "Du kannst deine lieblings Musik abspielen. Das macht dich immer gut gelaunt",
            "Du kannst Yoga treiben. Das hilft dir körperlich und geistlich weiter",
            "Geh eine runde spazieren und frische luft atmen."]
    randIdea=random.choice(ideas)
    return randIdea


if __name__ == "__main__":
    main()
