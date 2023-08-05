from je_api_testka.requests_wrapper.request_method import test_api_method
from je_api_testka.utils.exception.api_test_eceptions_tag import api_test_execute_action_error
from je_api_testka.utils.exception.api_test_exceptions import APITesterExecuteException


def execute_event(action):
    return test_api_method(action[0], action[1], action[2], **action[3])


def execute_action(action_list):
    execute_record_string = ""
    event_response_list = []
    for action in action_list:
        try:
            event_response = execute_event(action)
        except APITesterExecuteException:
            raise APITesterExecuteException(api_test_execute_action_error)
        print("execute: ", str(action))
        execute_record_string = "".join(execute_record_string)
        event_response_list.append(event_response)
    return execute_record_string, event_response_list


