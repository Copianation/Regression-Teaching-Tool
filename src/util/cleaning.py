import pandas as pd

def clean(command: str):
    command = command.replace(" ","")
    if not command: return None

    match command[0]:
        case ">":
            if command[1] == "=":
                value = command[2:]
                return lambda df : compare(df, float(value), larger=True, equal=True)
            value = command[1:]
            return lambda df : compare(df, float(value), larger=True, equal=False)
        case "<":
            if command[1] == "=":
                value = command[2:]
                return lambda df : compare(df, float(value), larger=False, equal=True)
            value = command[1:]
            return lambda df : compare(df, float(value), larger=False, equal=False)            
        case "=":
            if command[1:].capitalize() == "Nan":
                return is_na
            value = command[1:]
            return lambda df : equals(df, value)
        case _:
            return None


def is_na(df: pd.DataFrame):
    indices = []
    for column in df:
        indices.extend(df[df[column].isnull()].index)
    return indices

def equals(df: pd.DataFrame, value: str):
    if value.isnumeric():
        value = float(value)
    indices = []
    for column in df:
        indices.extend(df[df[column] == value].index)
    return indices

def compare(df: pd.DataFrame, value, larger, equal):
    indices = []
    for column in df:
        if not pd.api.types.is_numeric_dtype(df[column]): continue
        match (larger, equal):
            case (True, True):
                mask = df[column] >= value
            case (True, False):
                mask = df[column] > value
            case (False, True):
                mask = df[column] <= value
            case (False, False):
                mask = df[column] < value
        indices.extend(df[mask].index)
    return indices