import openai


class GrammarChecker:
    # Init with language
    def __init__(self, language: str):
        if language == "German":
            self.correction_string = "Behebe die Rechtschreibung."
        elif language == "English":
            self.correction_string = "Fix the spelling."
        elif language == "Spanish":
            self.correction_string = "¡Corrige la ortografía y la gramática (si hay errores)!" 
        elif language == "Czech":
            self.correction_string = "Opravte pravopisné chyby!"

    # Check if the input is correct
    def check(self, input: str) -> str:
        """Returns the correct string"""
        completion = openai.Edit.create(model="text-davinci-edit-001", input=input, instruction=self.correction_string, temperature=0)

        # Sometimes it will needlessly append the correction string
        return completion.choices[0].text.replace(self.correction_string, "")



if __name__ == "__main__":
    gc = GrammarChecker("German")
    gc.check("Ich bin ein Bienen Züchter.")