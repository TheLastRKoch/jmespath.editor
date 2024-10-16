import jmespath
import json
import os
import sys
import pandas as pd


def read_textfile(path):
    with open(path, "r", encoding='utf-8') as f:
        return f.read()


def write_textfile(path, body):
    with open(path, "w", encoding='utf-8') as f:
        f.write(body)


def load_json(path):
    return json.loads(read_textfile(path))


def save_json(path, data):
    write_textfile(path, json.dumps(data, indent=2))


def save_csv(path, data):
    df = pd.DataFrame(data)
    df.to_csv(path, encoding='utf-8', index=False)


def process_query(input_path, query_path):
    input_data = load_json(input_path)
    query = jmespath.compile(remove_comments(read_textfile(query_path)))
    return query.search(input_data)


def remove_comments(query):
    new_query = ""
    lines = query.split('\n')
    for line in lines:
        if not "#" in line:
            new_query += line + "\n"
    return new_query


def clear_console():
    os.system("clear")


if __name__ == "__main__":
    INPUT_PATH = "resources/input.json"
    OUTPUT_PATH = "resources/output.json"
    CSV_PATH = "resources/view.csv"
    QUERY_PATH = "resources/query.txt"

    try:
        expression = process_query(INPUT_PATH, QUERY_PATH)
        items_count = len(expression)
        clear_console()

        if len(sys.argv) > 1:
            command = sys.argv[1]
            if command == "output":
                save_json(OUTPUT_PATH, expression)
                message = f"Output updated\n\n{items_count} items"
            elif command == "csv":
                save_csv(CSV_PATH, expression)
                message = f"CSV file generated\n\n{items_count} items"
            else:
                message = json.dumps(expression, indent=2)
        else:
            message = json.dumps(expression, indent=2)

        print(message)

    except Exception as e:
        clear_console()
        print(e)
