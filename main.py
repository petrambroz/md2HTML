from src import runner
import json
from argparse import ArgumentParser

if __name__ == "__main__":
    with open("settings.json", "r") as file:
        settings = json.load(file)
    parser = ArgumentParser()
    parser.add_argument("-i", "--input")
    parser.add_argument("-o", "--output")
    args = parser.parse_args()
    
    language = settings["language"]
    title = settings["title"]
    indent = int(settings["indentation"])
    if args.input is None:
        filename = settings["input-file"]
    else:
        filename = args.input
    if args.output is None:
        outputfilename = settings["output-file"]
    else:
        outputfilename = args.output
    file = runner.Runner(language, title, filename, indent, outputfilename)
    data = file.run()
    file.make_file()
    file.save_file(data)
    print(f"Hotovo, uložen soubor {outputfilename}.")
