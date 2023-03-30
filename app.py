import jmespath
import json
import os
import sys
import pandas


def read_textfile(path):
    with open(path, "r", encoding='utf-8') as f:
        return f.read()


def write_textfile(path, body):
    with open(path, "w") as f:
        f.write(body)


if __name__ == "__main__":
    INPUT_PATH = "resources/input.json"
    OUTPUT_PATH = "resources/output.json"
    CSV_PATH = "resources/view.csv"
    QUERY_PATH = "resources/query.txt"

    try:
        input_file = json.loads(read_textfile(INPUT_PATH))
        query = jmespath.compile(read_textfile(QUERY_PATH))
        exp = query.search(input_file)
        items_count = len(exp)
        os.system("clear")
        if len(sys.argv) > 1:
            if sys.argv[1] == "output":
                body = json.dumps(exp, indent=2)
                write_textfile(OUTPUT_PATH, body)
                message = f"Output updated\n\n{items_count} items"
            elif sys.argv[1] == "csv":
                df = pandas.DataFrame(exp)
                df.to_csv(CSV_PATH, encoding='utf-8')
                message = f"CSV file generated\n\n{items_count} items"
            else:
                message = json.dumps(exp, indent=2)
        print(message)

    except Exception as e:
        os.system("clear")
        print(e)
