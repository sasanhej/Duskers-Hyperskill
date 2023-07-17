from test.tests import GlobalDuskersTest, STAGE_NO, MODULE_NAME
from utils.from_stage4_tests import FromStage4DuskersTest

if __name__ == '__main__':
    # run tests that are shared among more than 1 stage
    return_code = GlobalDuskersTest(STAGE_NO, MODULE_NAME).run_tests()[0]
    # run tests specific to this stage if global tests pass

    suites = [
        FromStage4DuskersTest(STAGE_NO, MODULE_NAME),
        # DuskersTest(MODULE_NAME) # uncomment when adding stage4 specific tests
    ]
    current_suite = 0

    while return_code == 0 and current_suite < len(suites):
        return_code = suites[current_suite].run_tests()[0]
        current_suite += 1
