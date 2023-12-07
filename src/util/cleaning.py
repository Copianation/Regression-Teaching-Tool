import pandas as pd

def clean(command: str, selected_cols):
    command = command.replace(" ","")
    if not command: return None

    match command[0]:
        case ">":
            if command[1] == "=":
                value = command[2:]
                return lambda df : compare(df, selected_cols, float(value), larger=True, equal=True)
            value = command[1:]
            return lambda df : compare(df, selected_cols, float(value), larger=True, equal=False)
        case "<":
            if command[1] == "=":
                value = command[2:]
                return lambda df : compare(df, selected_cols, float(value), larger=False, equal=True)
            value = command[1:]
            return lambda df : compare(df, selected_cols, float(value), larger=False, equal=False)            
        case "=":
            if command[1:].capitalize() == "Nan":
                return lambda df : is_na(df, selected_cols)
            value = command[1:]
            return lambda df : equals(df, selected_cols, value)
        case _:
            if command.capitalize() == "Nan":
                return lambda df : is_na(df, selected_cols)
            value = command
            return lambda df : equals(df, selected_cols, value)


def is_na(df: pd.DataFrame, selected_cols):
    indices = []
    for column in selected_cols:
        indices.extend(df[df.iloc[:, column].isnull()].index)
    return indices

def equals(df: pd.DataFrame, selected_cols, value: str):
    if value.isnumeric():
        value = float(value)
    indices = []
    for column in selected_cols:
        indices.extend(df[df.iloc[:, column] == value].index)
    return indices

def compare(df: pd.DataFrame, selected_cols, value, larger, equal):
    indices = []
    for column in selected_cols:
        if not pd.api.types.is_numeric_dtype(df.iloc[:, column]): continue
        match (larger, equal):
            case (True, True):
                mask = df.iloc[:, column] >= value
            case (True, False):
                mask = df.iloc[:, column] > value
            case (False, True):
                mask = df.iloc[:, column] <= value
            case (False, False):
                mask = df.iloc[:, column] < value
        indices.extend(df[mask].index)
    return indices