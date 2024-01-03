from src import runner
import json

if __name__ == "__main__":
    with open("settings.json", "r") as file:
        settings = json.load(file)

    language = settings["language"]
    title = settings["title"]
    indent = int(settings["indentation"])
    filename = settings["input-file"]
    outputfilename = settings["output-file"]
    file = runner.Runner(language, title, filename, indent, outputfilename)
    data = file.run()
    file.make_file()
    file.save_file(data)
    print("Hotovo, uložen soubor output.html.")
