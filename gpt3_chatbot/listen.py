import speech_recognition as sr


class Listener:
    def __init__(self):
        self.r = sr.Recognizer()

    def listen(self, language: str) -> str:
        while True:
            input("Press enter to record")

            with sr.Microphone() as source:
                print("Say something!")
                audio = self.r.listen(source)
            try:
                said_text = self.r.recognize_google(audio, language=language)
                return said_text
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print(
                    "Could not request results from Google Speech Recognition service; {0}".format(
                        e
                    )
                )


if __name__ == "__main__":

    # obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)

    # recognize speech using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print(
            "Could not request results from Google Speech Recognition service; {0}".format(
                e
            )
        )
