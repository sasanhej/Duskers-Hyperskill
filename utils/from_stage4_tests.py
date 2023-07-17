from hstest import CheckResult, dynamic_test
from utils.test_unit import TestData, init_test
from utils.global_tests import TestedProgram, SharedTest, run_for_stages, DEFAULT_CLI_ARGS, new_game_command, \
    INVALID_INPUT_RESPONSE_MSG, INVALID_RETURN_MSG, REDISPLAY_AFTER_INVALID_INPUT_MSG
from typing import List
import os
import glob

MENU_OPTIONS = "ex", "save", "up", "m"

SAVE_FILE_NAME = "*save_file*"
HIGH_SCORE_FILE_NAME = "*high_score*"

class TestAlg:
    def __init__(self, data: TestData):
        self.data = data
        self.gen_results()
        # makes sure that chosen place is not out of range in (all) explorations
        max_choice = min([len(self.results[i])
                         for i in range(len(self.results))])
        if data.chosen > max_choice:
            self.data.chosen = max_choice
        self.calc_expected()
        self.gen_input()
        self.seed = data.seed
        self.places = data.places

    def calc_expected(self):
        """Expected value is sum of titanium after all the explorations"""
        self.expected = str(sum([
            self.results[explr][self.data.chosen - 1][1]
            for explr in range(self.data.explorations)
        ]))

    def gen_input(self):
        self.input = ([MENU_OPTIONS[0]] + ['s'] * (self.data.searches - 1) +
                      [str(self.data.chosen)]) * self.data.explorations

    def gen_results(self):
        self.results = init_test(self.data)

    def regenerate(self, exploration_count: int):
        self.data.explorations = exploration_count
        self.gen_results()
        self.calc_expected()
        self.gen_input()


test_data = [
    TestData(1, 8, "1", 1, "place1,place2"),
    TestData(2, 8, "100", 8, "Middle_of_nowhere,Ice_desert,Underground_city"),
    TestData(20, 9, "hyperskill", 5,
             "Old_power_plant,Abandoned_warehouse,Zombie_canteen"),
    TestData(10, 2, "seed", 1, "Middle_of_nowhere,Ice_desert,Underground_city")
]

tests = [TestAlg(data) for data in test_data]


def clean_game_files():
    """clean up files created by game after test"""
    for file in [SAVE_FILE_NAME, HIGH_SCORE_FILE_NAME]:
        for file_name in glob.glob(file):
            os.remove(file_name)


def file_cleanup(function):
    def wrapper(*args, **kwargs):
        clean_game_files()
        result = function(*args, **kwargs)
        clean_game_files()
        return result

    return wrapper


def restart(pr: TestedProgram, args: List[str] = [], input: List[str] = []) \
        -> TestedProgram:
    pr.stop()
    pr = TestedProgram()
    print("\n**PROGRAM RELOADED**")

    pr.start(*args)
    for command in input:
        pr.execute(command)

    return pr


class FromStage4DuskersTest(SharedTest):

    @dynamic_test
    @run_for_stages(4, 5, 6)
    def test_initial_titanium_balance(self):
        pr = TestedProgram()
        pr.start(*DEFAULT_CLI_ARGS)
        pr.execute(new_game_command(self.stage))

        pr.execute("hyperskill")
        hub = pr.execute("yes").lower()

        for line in hub.splitlines():
            if "titanium" in line:
                if "0" not in line:
                    return CheckResult.wrong(
                        "Wrong titanium balance displayed.\n"
                        "Make sure it is set to 0 when starting a new game."
                    )
                break
        else:
            return CheckResult.wrong(
                "Titanium balance not displayed inside the hub."
            )

        return CheckResult.correct()

    @dynamic_test(data=tests)
    @run_for_stages(4, 5)
    def test_exploration_based_on_seed(self, test: TestAlg):
        pr = TestedProgram()
        pr.start(test.seed, "0", "0", test.places)
        pr.execute(new_game_command(self.stage))
        pr.execute("hyperskill")
        pr.execute("yes")

        for command in test.input:
            output = pr.execute(command)

        if test.expected not in output:
            return CheckResult.wrong(
                "Something went wrong with the exploration.\n\n"
                "Make sure the titanium amount from exploration is based on the seed,\n"
                "and that the exploration data is generated in the exact order mentioned.\n"
                "Make sure that the titanium balance is update accordingly in the hub.\n"
                "It might be helpful to reproduce the input from examples and compare output."
            )

        return CheckResult.correct()

    @dynamic_test(data=["blah", "jibberjabbter", "invalid"])
    @run_for_stages(4, 5, 6)
    def test_invalid_input_in_exploration(self, bad_input):
        pr = TestedProgram()
        pr.start(*DEFAULT_CLI_ARGS)
        pr.execute(new_game_command(self.stage))
        pr.execute("hyperskill")
        hub = pr.execute("yes")
        prompt = pr.execute("ex").split("\n")[-1]

        response_to_invalid_input = pr.execute(bad_input)

        if "invalid input" not in response_to_invalid_input.lower():
            return CheckResult.wrong(INVALID_INPUT_RESPONSE_MSG)

        if hub in response_to_invalid_input:
            return CheckResult.wrong(
                INVALID_RETURN_MSG.format(place="hub")
            )

        if prompt not in response_to_invalid_input:
            return CheckResult.wrong(
                REDISPLAY_AFTER_INVALID_INPUT_MSG.format("command prompt")
            )

        return CheckResult.correct()

    @dynamic_test
    @run_for_stages(4, 5, 6)
    def test_back_button_from_exploration(self):
        pr = TestedProgram()
        pr.start(*DEFAULT_CLI_ARGS)
        pr.execute(new_game_command(self.stage))
        pr.execute("hyperskill")
        hub = pr.execute("yes")
        pr.execute("ex")
        redisplayed_hub = pr.execute("back")

        if hub not in redisplayed_hub:
            return CheckResult.wrong(
                "Game HUB not displayed after selecting back on the exploration"
                " menu."
            )

        return CheckResult.correct()
