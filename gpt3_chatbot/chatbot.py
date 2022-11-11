import openai
import colorama
from gpt3_chatbot.listen import Listener
from gpt3_chatbot.read import read_story
from gpt3_chatbot.helper_functions import load_key, load_config_json
from gpt3_chatbot.grammar_correction import GrammarChecker


SETTINGS_DICT = load_config_json("characters/spanish_standard.json")
SETTINGS_DICT = load_config_json("characters/english_stuff.json")
#VOICE = "es-CL-CatalinaNeural"
VOICE = "en-GB-LibbyNeural"
FIX_ERRORS = False#True
STT_LANG = "en-US"

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
    if FIX_ERRORS:
        grammar_checker = GrammarChecker(SETTINGS_DICT["LANGUAGE"])

    conversation = Conversation(SETTINGS_DICT["MAX_NUM_USER_INPUTS"])

    print(colorama.Fore.RED + SETTINGS_DICT["STARTING_REQUEST"] + colorama.Fore.RESET)
    while True:
        user_input = input(colorama.Fore.YELLOW)
        prompt = conversation.get_prompt(user_input)

        if FIX_ERRORS:
            checked_prompt = grammar_checker.check(user_input.strip()).strip()
            if checked_prompt != user_input.strip():
                print(
                    colorama.Fore.RED
                    + f"Correct: {checked_prompt}"
                    + colorama.Fore.RESET
                )

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

def talk_to_chatbot_real_voice():
    listener = Listener()

    openai.api_key = load_key()
    if FIX_ERRORS:
        grammar_checker = GrammarChecker(SETTINGS_DICT["LANGUAGE"])

    conversation = Conversation(SETTINGS_DICT["MAX_NUM_USER_INPUTS"])
    print(colorama.Fore.RED + SETTINGS_DICT["STARTING_REQUEST"] + colorama.Fore.RESET)

    while True:
        user_input = listener.listen(STT_LANG)
        print(user_input)
        if FIX_ERRORS:
            checked_prompt = grammar_checker.check(user_input.strip()).strip()
            if checked_prompt != user_input.strip():
                print(
                    colorama.Fore.RED
                    + f"Correct: {checked_prompt}"
                    + colorama.Fore.RESET
                )
            prompt = conversation.get_prompt(checked_prompt)
        else:
            prompt = conversation.get_prompt(user_input)
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
        read_story(answer_line, VOICE)

