from numpy import empty
import pytest
from deepcell_evaluator.lambdas.rest_api.utils.evaluator import Evaluator


def test_valid_parameters():
    sub = 'AAA'
    string = 'AAAAAA'
    _, condition = Evaluator(sub, string).get_evaluation()
    assert len(condition) == 0
    
    
def test_valid_any_case_parameters():
    sub = 'AaA'
    string = 'AaAAaA'
    _, condition = Evaluator(sub, string).get_evaluation()
    assert len(condition) == 0
    
    
def test_erro_empty_sub():
    sub = ''
    string = 'AAAAAA'
    _, condition = Evaluator(sub, string).get_evaluation()
    assert len(condition) > 0
    
    
def test_erro_empty_string():
    sub = 'AAA'
    string = ''
    _, condition = Evaluator(sub, string).get_evaluation()
    assert len(condition) > 0
    
    
def test_erro_invalid_evaluation():
    sub = 'ABC'
    string = 'AABCAABC'
    _, condition = Evaluator(sub, string).get_evaluation()
    assert len(condition) > 0
    
def test_erro_sub_not_str():
    sub = 123
    string = '123123'
    _, condition = Evaluator(sub, string).get_evaluation()
    assert len(condition) > 0
    
def test_erro_sub_not_str():
    sub = '123'
    string = 123123
    _, condition = Evaluator(sub, string).get_evaluation()
    assert len(condition) > 0
    
def test_erro_assert_result_value():
    sub = 'ABC'
    string = 'AABBCC'
    result, _ = Evaluator(sub, string).get_evaluation()
    assert result == -len(string)
    
def test_erro_assert_result_type():
    sub = 'ABC'
    string = 'AABBCC'
    result, _ = Evaluator(sub, string).get_evaluation()
    assert isinstance(result, int)