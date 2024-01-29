from src import runner
"""
Spouštění pro testovací soubory ve složce tests. Přeloží soubory test0.md,...,testN.md.
"""
if __name__ == "__main__":
    indent = 2
    language = "cs"
    for i in range(4):
        i = str(i)
        title = "test" + i
        filename = "./tests/test" + i + ".md"
        file = runner.Runner(language, title, filename, indent, "./tests/test" + i + ".html")
        data = file.run()
        file.make_file()
        file.save_file(data)
