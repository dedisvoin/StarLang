from source.core import tokens
from source.core import operators
import json


def save_tokens_to_file(tokens_list: list[tokens.Token], path: str):
    with open(path, 'w') as file:
        tokens_data = [
            {
                'type': token.type,
                'value': token.value,
                'line': token.line,
                'pos': token.pos
            }
            for token in tokens_list
        ]
        json.dump(tokens_data, file, indent=4)


def load_tokens_file(path: str) -> list[tokens.Token]:
    with open(path, 'r') as file:
        tokens_data = json.load(file)
        tokens_list = []
        for token_data in tokens_data:
            signature = ''
            if operators.this_is_operator(token_data['value']):
                signature = operators.get_operator(token_data['value'])
            token = tokens.Token(
                token_data['type'],
                token_data['value'],
                token_data['line'],
                token_data['pos'],
                signature
            )
            tokens_list.append(token)
        return tokens_list
    
def load_tokens(tokens_list: list[tokens.Token]) -> list[tokens.Token]:
    return_tokens_list = []
    for token in tokens_list:
        signature = operators.Operator(token.value)
        ls = token.lenght - len(token.value)
        if operators.this_is_operator(token.value):
            signature = operators.get_operator(token.value)
        token = tokens.Token(
            token.type,
            token.value,
            token.line,
            token.pos,
            signature
        ).add_len(ls)
        return_tokens_list.append(token)
    return return_tokens_list


def clear_comments(tokens_list: list[tokens.Token]) -> list[tokens.Token]:
    return_tokens_list = []
    for token in tokens_list:
        if token.type != tokens.T_Types.T_COMMENTS:
            return_tokens_list.append(token)
    return return_tokens_list