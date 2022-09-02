import openai
import colorama

from grammar_correction import GrammarChecker

ENGLISH_THERAPIST_SETTINGS = {
    "STARTING_PROMPT": "A conversation between a patient and a helpful and very nice psychotherapist.",
    "STARTING_REQUEST": "Ask the therapist a question!",
    "MAX_NUM_USER_INPUTS": 3,
    "USER_PREFIX": "P: ",
    "AI_PREFIX": "PT:",
    "CUT_DIALOGUE_PLACEHOLDER": "...",
    "FREQUENCY_PENALTY": 1,
    "PRESENCE_PENALTY": 1,
    "MAX_TOKENS": 120,
}
GERMAN_THERAPIST_SETTINGS = {
    "STARTING_PROMPT": "Ein Gespräch zwischen einem Patienten und einer sehr hilfreichen und netten Psychotherapeutin.",
    "STARTING_REQUEST": "Frage die Therapeutin etwas!",
    "MAX_NUM_USER_INPUTS": 3,
    "USER_PREFIX": "P: ",
    "AI_PREFIX": "PT:",
    "CUT_DIALOGUE_PLACEHOLDER": "...",
    "FREQUENCY_PENALTY": 1,
    "PRESENCE_PENALTY": 1,
    "MAX_TOKENS": 120,
}
GERMAN_PROFESSOR_SETTINGS = {
    "STARTING_PROMPT": "Ein Gespräch zwischen einem Studenten und einem extrem gebildeten und hilfreichen Professor.",
    "STARTING_REQUEST": "Frage den Professor etwas!",
    "MAX_NUM_USER_INPUTS": 3,
    "USER_PREFIX": "S: ",
    "AI_PREFIX": "P:",
    "CUT_DIALOGUE_PLACEHOLDER": "...",
    "FREQUENCY_PENALTY": 1,
    "PRESENCE_PENALTY": 1,
    "MAX_TOKENS": 120,
}
PROPAGANDA_SETTINGS = {
    "STARTING_PROMPT": "Ein Gespräch zwischen einem Mann und einer jungen Frau.",
    "STARTING_REQUEST": "Chatte!",
    "MAX_NUM_USER_INPUTS": 3,
    "USER_PREFIX": "M: ",
    "AI_PREFIX": "F:",
    "CUT_DIALOGUE_PLACEHOLDER": "...",
    "FREQUENCY_PENALTY": 1,
    "PRESENCE_PENALTY": 1,
    "MAX_TOKENS": 120,
}
SPANISH_ROBOT_SETTINGS = {
    "STARTING_PROMPT": "Una conversación entre una chica y un hombre.",
    "STARTING_REQUEST": "Habla!",
    "MAX_NUM_USER_INPUTS": 3,
    "USER_PREFIX": "P: ",
    "AI_PREFIX": "R:",
    "CUT_DIALOGUE_PLACEHOLDER": "...",
    "FREQUENCY_PENALTY": 1,
    "PRESENCE_PENALTY": 1,
    "MAX_TOKENS": 120,
}

SETTINGS_DICT = SPANISH_ROBOT_SETTINGS


def load_key():
    with open("openai-key.txt", "r", encoding="utf-8") as f:
        return f.readline()


class Conversation:
    def __init__(self, max_user_inputs) -> None:
        self.conversation = None
        self.num_user_inputs = 0
        self.max_user_inputs = max_user_inputs

    def get_prompt(self, user_input: str) -> str:
        if self.conversation == None:
            self.conversation = (
                SETTINGS_DICT["STARTING_PROMPT"]
                + "\n"
                + SETTINGS_DICT["USER_PREFIX"]
                + user_input
                + "\n"
                + SETTINGS_DICT["AI_PREFIX"]
            )
        else:
            self.conversation = (
                self.conversation.strip()
                + "\n"
                + SETTINGS_DICT["USER_PREFIX"]
                + user_input
                + "\n"
                + SETTINGS_DICT["AI_PREFIX"]
            )
        self.num_user_inputs += 1

        if self.num_user_inputs > self.max_user_inputs:
            self.conversation = (
                SETTINGS_DICT["STARTING_PROMPT"]
                + "\n"
                + SETTINGS_DICT["CUT_DIALOGUE_PLACEHOLDER"]
                + "\n"
                + SETTINGS_DICT["USER_PREFIX"]
                + self.conversation.split(f"\n{SETTINGS_DICT['USER_PREFIX']}", 2)[2]
            )

        return self.conversation

    def set_completion(self, completion: str):
        self.conversation += completion


def start_conversation():
    openai.api_key = load_key()
    grammar_checker = GrammarChecker("Spanish")

    conversation = Conversation(SETTINGS_DICT["MAX_NUM_USER_INPUTS"])

    print(colorama.Fore.RED + SETTINGS_DICT["STARTING_REQUEST"] + colorama.Fore.RESET)
    while True:
        user_input = input(colorama.Fore.YELLOW)
        prompt = conversation.get_prompt(user_input)

        #print(colorama.Fore.RESET, end="")
        checked_prompt = grammar_checker.check(user_input.strip()).strip()
        if checked_prompt != user_input.strip():
            print(colorama.Fore.RED + f"Correct: {checked_prompt}" + colorama.Fore.RESET)

        completion = openai.Completion.create(
            model="text-davinci-002",
            prompt=prompt,
            stop=SETTINGS_DICT["USER_PREFIX"].strip(),
            user="chatbot-test",
            max_tokens=SETTINGS_DICT["MAX_TOKENS"],
            frequency_penalty=SETTINGS_DICT["FREQUENCY_PENALTY"],
            presence_penalty=SETTINGS_DICT["PRESENCE_PENALTY"],
        )
        # Print the conversation.conversation to a txt file
        with open("conversation.txt", "w", encoding="utf-8") as f:
            f.write(conversation.conversation)
        answer_line = completion.choices[0].text

        conversation.set_completion(answer_line)
        print(colorama.Fore.GREEN + answer_line.strip() + colorama.Fore.RESET)


if __name__ == "__main__":
    start_conversation()
