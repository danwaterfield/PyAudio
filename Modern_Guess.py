import random
import time
import speech_recognition as sr

#this is a voice-recog game which prompts the user to guess a modernist author. 
# The code was taken from geeksforgeeks, then tweaked as a learning exercise.

def recognize_speech_from_mic(recognizer, microphone):
    #first off let's get some error messages out of the way
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source) #identifies ambient noise in order to 
        audio = recognizer.listen(source)

    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response


if __name__ == "__main__":
    WORDS = ["Woolf", "Joyce", "Ford", "Eliot", "Bishop", "Conrad", "Dos Passos", "Lawrence", "Mansfield", "Ellison", "Faulkner"]
    #Long term words will be a longer list. Could implement a dict or tuple with guesses...
    NUM_GUESSES = 3
    PROMPT_LIMIT = 5

    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    word = random.choice(WORDS)

    instructions = (
        "I'm thinking of one of these words:\n"
        "{words}\n"
        "You have {n} tries to guess which one.\n"
    ).format(words=', '.join(WORDS), n=NUM_GUESSES)

    # show instructions and wait 5 seconds before starting the game
    print(instructions)
    time.sleep(5)

    for i in range(NUM_GUESSES):
        for j in range(PROMPT_LIMIT):
            print('Guess {}. Please speak now'.format(i+1))
            guess = recognize_speech_from_mic(recognizer, microphone)
            if guess["transcription"]:
                break
            if not guess["success"]:
                break
            print("Terribly sorry, but I didn't catch that. Could you please repeat your guess?\n")

        if guess["error"]:
            print("ERROR: {}".format(guess["error"]))
            break

        print("You guessed: {}".format(guess["transcription"]))

        guess_is_correct = guess["transcription"].lower() == word.lower()
        user_has_more_attempts = i < NUM_GUESSES - 1

        if guess_is_correct:
            print("Correct! You win! ...Nothing. There are no prizes, only the long chronic traumas of the first world war".format(word))
            break
        elif user_has_more_attempts:
            print("Incorrect. Try again.\n")
        else:
            print("Sorry, you lose!\nI was thinking of '{}'.".format(word))
            break