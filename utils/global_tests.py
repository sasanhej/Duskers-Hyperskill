import re
from typing import List

from hstest import CheckResult, StageTest, TestedProgram, dynamic_test, WrongAnswer

CASE_INSENSITIVITY_REMINDER = ("Remember, the user's input should be handled "
                               "in a non case-sensitive way.")
TERMINATE_ON_BAD_INPUT_MSG = ("Your program should not terminate if invalid"
                              " input is entered.")

INVALID_INPUT_RESPONSE_MSG = (
    "Your program did not respond properly to invalid input.\n"
    "Make sure to include the message 'Invalid input' before "
    "Re-prompting the user for input."
)

REDISPLAY_AFTER_INVALID_INPUT_MSG = (
    "The {} was not redisplayed after entering invalid input."
)

INVALID_RETURN_MSG = (
    "Your program should not return to the "
    "{place} if invalid input is entered in the high scores.\n"
    "Only entering [Back] should return the user to the {place}."
)

DEFAULT_CLI_ARGS = "hyperskill", "0", "0", "place1,place2"


def new_game_command(stage_no):
    return "play" if stage_no <= 4 else "new"


def run_for_stages(*stageNumbers: int):
    def decorator(function):
        def wrapper(self, *args, **kwargs):
            if self.stage in stageNumbers:
                return function(self, *args, **kwargs)
            else:
                print("Not applicable for this stage, skipped.")
                return CheckResult.correct()

        return wrapper

    return decorator


def get_robot_lines(hub: str) -> List[str]:
    hub_lines = re.split("\n+", hub)

    robots = []
    state = 0
    for line in hub_lines:
        if len(line.strip()) > 0 and line.strip()[0] == '+':
            if state == 1:
                state = 2
                break
            else:
                state = 1
            continue
        if state == 1:
            robots.append(line)

    if state != 2:
        raise WrongAnswer(
            "Please make sure your HUB contains two lines, starting with '+' character\n"
            "Robot images should be placed between first two of them."
        )

    return robots


def check_graphical_robots(robots_display: List[str], number_of_robots: int) \
        -> bool:
    """helper method to check for arbitrary number of robots"""

    result = True

    if number_of_robots == 0:
        return True

    if len(robots_display) == 0:
        return False

    positions = []
    prev_position = -1
    while robots_display[0].find("|", prev_position + 1) != -1:
        prev_position = robots_display[0].find("|", prev_position + 1)
        positions.append(prev_position)
    if len(positions) != number_of_robots - 1:
        return False

    for line in robots_display:
        stripped_lines = [robot_line.strip() for robot_line in re.split("\|", line)]

        if len(stripped_lines) != number_of_robots:
            return False

        prev_position = -1
        for pos in positions:
            if line.find("|", prev_position + 1) != pos:
                return False
            prev_position = pos

        result = result and all(
            (robot == stripped_lines[0] and (robot != "" or number_of_robots == 0)) for robot in stripped_lines[1:])

    return result


class SharedTest(StageTest):
    def __init__(self, stage: int, source_name: str = ''):
        super().__init__(source=source_name)
        self.stage = stage


class GlobalDuskersTest(SharedTest):
    @dynamic_test(data=["exit", "EXIT", "eXiT"])
    @run_for_stages(1, 2, 3, 4, 5, 6)
    def test_exit_option(self, exit_command):
        pr = TestedProgram()
        pr.start(*DEFAULT_CLI_ARGS)
        exit_message = pr.execute(exit_command)

        if not exit_message.strip():
            return CheckResult.wrong(
                "No goodbye message was printed upon choosing [Exit].\n"
                + CASE_INSENSITIVITY_REMINDER
            )

        if not pr.is_finished():
            return CheckResult.wrong(
                "Your program should finish when the [Exit] option is chosen.\n"
                + CASE_INSENSITIVITY_REMINDER
            )

        return CheckResult.correct()

    @dynamic_test(data=["givv", "new", "start", "begin"])
    @run_for_stages(1, 2, 3, 4)
    def test_invalid_input_in_main_menu(self, bad_input):
        pr = TestedProgram()
        menu = pr.start(*DEFAULT_CLI_ARGS)
        prompt = re.split("\n+", menu)[-1]

        response_to_invalid_input = pr.execute(bad_input)

        if pr.is_finished():
            return CheckResult.wrong(TERMINATE_ON_BAD_INPUT_MSG)

        if "invalid input" not in response_to_invalid_input.lower():
            return CheckResult.wrong(INVALID_INPUT_RESPONSE_MSG)

        if prompt not in response_to_invalid_input:
            return CheckResult.wrong(
                REDISPLAY_AFTER_INVALID_INPUT_MSG.format("command prompt")
            )

        return CheckResult.correct()

    @dynamic_test(data=["NAH", "i don't know", "I'm undecided"])
    @run_for_stages(1, 2)
    def test_invalid_input_in_ready_menu(self, bad_input):
        pr = TestedProgram()
        pr.start()
        pr.execute("play")
        ready_menu = pr.execute("hyperskill")
        prompt = re.split("\n+", ready_menu)[-1]

        response_to_invalid_input = pr.execute(bad_input)

        if pr.is_finished():
            return CheckResult.wrong(TERMINATE_ON_BAD_INPUT_MSG)

        if "invalid input" not in response_to_invalid_input.lower():
            return CheckResult.wrong(INVALID_INPUT_RESPONSE_MSG)

        if prompt not in response_to_invalid_input:
            return CheckResult.wrong(
                REDISPLAY_AFTER_INVALID_INPUT_MSG.format("command prompt")
            )

        pr.execute("yes")
        if not pr.is_finished():
            return CheckResult.wrong(
                "Your program did not finish when supplied with a valid input"
                "after entering an invalid input in the ready menu."
            )

        return CheckResult.correct()

    @dynamic_test
    @run_for_stages(2, 3, 4)
    def test_menu_print(self):
        pr = TestedProgram()
        menu = pr.start(*DEFAULT_CLI_ARGS)
        menu_lines = re.split("\n+", menu)

        if len(menu_lines) < 12:
            return CheckResult.wrong(
                "Output too short. Your title should take up exactly 8 non-empty lines, "
                "then the main menu options should be displayed on separate lines."
            )

        play_button = menu_lines[8].lower()
        if "[play]" not in play_button:
            return CheckResult.wrong(
                "Play option should be right underneath the title,"
                " which should take up exactly 8 non-empty lines."
            )

        high_button = menu_lines[9].lower()
        if "[high]" not in high_button:
            return CheckResult.wrong(
                "High scores option should be right under [Play].")

        help_button = menu_lines[10].lower()
        if "[help]" not in help_button:
            return CheckResult.wrong(
                "Help option should be right under [High] scores")

        exit_button = menu_lines[11].lower()
        if "[exit]" not in exit_button:
            return CheckResult.wrong(
                "Exit option should be right under [Help].")

        return CheckResult.correct()

    @dynamic_test(data=[
        ["hyperskill", "yes"],
        ["hyper", "YES"],
        ["automated test", "yES"]])
    @run_for_stages(2, 3, 4, 5)
    def test_play_option(self, player_name, yes):
        pr = TestedProgram()
        pr.start(*DEFAULT_CLI_ARGS)
        pr.execute(new_game_command(self.stage))
        ready_prompt = pr.execute(player_name).lower()

        if player_name not in ready_prompt:
            return CheckResult.wrong("Player not greeted personally.")

        if "[yes]" not in ready_prompt or "[no]" not in ready_prompt:
            return CheckResult.wrong(
                "Player not asked if he/she is ready to begin.\n"
                "Remember to display possible commands for player to choose from."
            )

        hub = pr.execute(yes).strip()

        if not hub or len(hub) == 0:
            return CheckResult.wrong(
                "No hub found after selecting [Yes] from the ready menu.\n"
                "For now this hub can be anything.\n"
                + CASE_INSENSITIVITY_REMINDER
            )

        if not pr.is_finished:
            return CheckResult.wrong(
                "Program should finish after player says that they're ready"
                "and the hub is displayed.\n"
                + CASE_INSENSITIVITY_REMINDER)

        return CheckResult.correct()

    @dynamic_test(data=["HIGH", "high", "High", "hIgH"])
    @run_for_stages(2, 3, 4, 5)
    def test_high_score_option(self, high_command):
        pr = TestedProgram()
        menu = pr.start(*DEFAULT_CLI_ARGS)
        high_scores = pr.execute(high_command).lower()

        if "no scores" not in high_scores:
            return CheckResult.wrong(
                "Make sure to print out 'No scores' on the high scores screen.\n"
                + CASE_INSENSITIVITY_REMINDER
            )

        if "[back]" not in high_scores:
            return CheckResult.wrong(
                "No back option displayed on high score screen."
            )

        back_output = pr.execute("back")
        if menu not in back_output:
            return CheckResult.wrong(
                "Make sure the whole menu including the title is displayed again"
                " after returning to main menu from the high scores screen."
            )

        return CheckResult.correct()

    @dynamic_test(data=["blah", "jibberjabbter", "invalid"])
    @run_for_stages(2, 3, 4, 5)
    def test_invalid_input_in_high_scores(self, bad_input):
        pr = TestedProgram()
        menu = pr.start(*DEFAULT_CLI_ARGS)
        prompt = re.split("\n+", pr.execute("high"))[-1]

        response_to_invalid_input = pr.execute(bad_input)

        if "invalid input" not in response_to_invalid_input.lower():
            return CheckResult.wrong(INVALID_INPUT_RESPONSE_MSG)

        if menu in response_to_invalid_input:
            return CheckResult.wrong(
                INVALID_RETURN_MSG.format(place="main menu")
            )

        if prompt not in response_to_invalid_input:
            return CheckResult.wrong(
                REDISPLAY_AFTER_INVALID_INPUT_MSG.format("command prompt")
            )

        redisplay_menu = pr.execute("back")

        if menu not in redisplay_menu:
            return CheckResult.wrong("Your program should return to the main "
                                     "menu after a correct input of [Back] is entered on the high "
                                     "scores screen."
                                     )

        pr.execute("exit")
        if not pr.is_finished():
            return CheckResult.wrong(
                "Your program failed to finish after returning to the menu "
                "from the high scores screen and selecting [Exit].\n"
                "Check that your menu is still functional after returning to "
                "it from another screen."
            )

        return CheckResult.correct()

    @dynamic_test
    @run_for_stages(2, 3, 4, 5)
    def test_help_option_placeholder(self):
        pr = TestedProgram()
        pr.start(*DEFAULT_CLI_ARGS)

        short_message = pr.execute("help")
        if not short_message or short_message == "":
            return CheckResult.wrong(
                "No placeholder text displayed to the user upon selecting a "
                "menu option that has not yet been implemented: [Help]."
            )

        if not pr.is_finished():
            return CheckResult.wrong(
                "Your program should terminate upon selecting a non-implemented "
                "option: [Help]."
            )

        return CheckResult.correct()

    @dynamic_test
    @run_for_stages(2, 3, 4, 5, 6)
    def test_menu_return_from_play_option(self):
        pr = TestedProgram()
        menu = pr.start(*DEFAULT_CLI_ARGS)
        pr.execute(new_game_command(self.stage))

        ready_prompt = pr.execute("hyperskill").lower()
        if "[menu]" not in ready_prompt:
            return CheckResult.wrong(
                "Make sure that the menu option is available and displayed to "
                "the player when asking for readiness.")

        redisplayed_menu = pr.execute("menu")
        if menu not in redisplayed_menu:
            return CheckResult.wrong(
                "Make sure the whole menu including the title is displayed "
                "again after returning to main menu from the readiness screen."
            )

        return CheckResult.correct()

    @dynamic_test
    @run_for_stages(3, 4, 5, 6)
    def test_keep_asking_for_readiness(self):
        pr = TestedProgram()
        pr.start(*DEFAULT_CLI_ARGS)
        pr.execute(new_game_command(self.stage))
        ready_prompt = re.split("\n+", pr.execute("hyperskill"))[-1]

        for _ in range(3):
            re_ready_prompt = pr.execute("no")

            if ready_prompt not in re_ready_prompt:
                return CheckResult.wrong(
                    "You must keep asking the player if they are ready until "
                    "they choose [Yes] if they chose [No] when asked if ready.\n"
                    + CASE_INSENSITIVITY_REMINDER
                )

        hub = pr.execute("yes").strip()

        if not hub or hub == "":
            return CheckResult.wrong(
                "No hub found after finally selecting yes from the "
                "ready menu. For now this hub can be anything.\n"
                "Take a look where you continuously ask the player if they're "
                "ready.\n" + CASE_INSENSITIVITY_REMINDER
            )

        if pr.is_finished():
            return CheckResult.wrong(
                "Your program should not finish when the player finally decides"
                " that they're ready."
            )

        return CheckResult.correct()

    @dynamic_test
    @run_for_stages(3, 4, 5, 6)
    def test_hub_display(self):
        pr = TestedProgram()
        pr.start(*DEFAULT_CLI_ARGS)
        pr.execute(new_game_command(self.stage))
        pr.execute("hyperskill")
        hub = pr.execute("yes")

        robots = get_robot_lines(hub)

        if not check_graphical_robots(robots, 3):
            return CheckResult.wrong(
                "Your three robots, placed between first two lines, starting with '+' character, "
                "must be identical and be divided by '|' symbol just like in the example.\n"
                "Each line of robot image should contain at least one non-whitespace character"
            )

        return CheckResult.correct()

    @dynamic_test
    @run_for_stages(3, 4, 5, 6)
    def test_game_menu(self):
        pr = TestedProgram()
        main_menu = pr.start(*DEFAULT_CLI_ARGS)
        play_menu = pr.execute(new_game_command(self.stage))
        pr.execute("hyperskill")
        hub = pr.execute("yes")
        menu = pr.execute("m").lower()

        for option in ["[back]", "[main]", "[save]", "[exit]"]:
            if option not in menu:
                return CheckResult.wrong(
                    "Some in-game menu options are missing.\n"
                    "Include the same ones that are in the examples.\n"
                    f"'{option}' not found."
                )

        redisplayed_hub = pr.execute("back")
        if hub not in redisplayed_hub:
            return CheckResult.wrong(
                "Game HUB not displayed after selecting 'back' option on game menu."
            )

        redisplayed_menu = pr.execute("m").lower()
        if menu not in redisplayed_menu:
            return CheckResult.wrong(
                "Your program did not display the in-game menu again after "
                "returning to the hub and selecting the 'menu' option a second "
                "time."
            )

        redisplayed_main_menu = pr.execute("main")
        if main_menu not in redisplayed_main_menu:
            return CheckResult.wrong(
                "Main menu should be displayed after choosing the 'main' option"
                " from the in-game menu.")

        redisplayed_play_menu = pr.execute(new_game_command(self.stage))
        if play_menu not in redisplayed_play_menu:
            return CheckResult.wrong(
                "Your program failed to start another game after returning to "
                "the main menu from an existing game."
            )

        pr.execute("hyperskill")
        pr.execute("yes")
        pr.execute("m")

        goodbye_message = pr.execute("exit")
        if not goodbye_message.strip():
            return CheckResult.wrong(
                "No goodbye message was printed upon choosing [Exit].\n"
                + CASE_INSENSITIVITY_REMINDER
            )

        if not pr.is_finished():
            return CheckResult.wrong(
                "Your program should finish when the [Exit] option is chosen.\n"
                + CASE_INSENSITIVITY_REMINDER
            )

        return CheckResult.correct()

    @dynamic_test(data=["save"])
    @run_for_stages(3, 4)
    def test_placeholders_menu(self, option):
        pr = TestedProgram()
        pr.start(*DEFAULT_CLI_ARGS)
        pr.execute("play")
        pr.execute("hyperskill")
        pr.execute("yes")
        pr.execute("m")

        short_message = pr.execute(option).strip()
        if not short_message:
            return CheckResult.wrong(
                "No placeholder text displayed to the user upon selecting a "
                f"menu option that has not yet been implemented: [{option}]."
            )

        if not pr.is_finished():
            return CheckResult.wrong(
                "Your program should terminate upon selecting a non-implemented "
                f"option: [{option}]."
            )

        return CheckResult.correct()
