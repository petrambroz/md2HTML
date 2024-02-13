from src.convertor import html_convertor
import re


class Runner:
    def __init__(self, language: str, title: str, filename="input.md", indent=4, outputfilename="output.html"):
        self.language = language
        self.title = title
        self.filename = filename
        self.outputfilename = outputfilename
        self.syntax_inline = ["*", "*", "_", "_", "~", "`", "=", "^"]
        self.indent = indent

    def make_file(self):
        """Creates a basic head element with language, encoding and title settings.
        """
        html_boilerplate = '<!DOCTYPE html>\n'\
            f'<html lang="{self.language}">\n'\
            '<head>\n'\
            '    <meta charset="UTF-8">\n'\
            '    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n'\
            f'    <title>{self.title}</title>\n'\
            '</head>\n'\
            '<body>\n'
        with open(self.outputfilename, mode="w", encoding="utf-8") as f:
            data = html_boilerplate
            f.write(data)

    def save_file(self, data):
        with open(self.outputfilename, mode="a", encoding="utf-8") as f:
            f.write(data + "\n</body>" + "\n</html>")

    def send_to_edit(self, syntax, string):
        """Receives a string to be formatted by html tags. Depending on the operator character, the string is
        passed to the respective funcion from the html_converter module.
        """
        if syntax == "**" or syntax == "__":
            result = con.bold(string)
        elif syntax == "*" or syntax == "_":
            result = con.italics(string)
        elif syntax == "~~":
            result = con.strikethrough(string)
        elif syntax == "`":
            result = con.code(string)
        elif syntax == "~":
            result = con.subscript(string)
        elif syntax == "==":
            result = con.mark(string)
        elif syntax == "^":
            result = con.superscript(string)
        return result

    def condese(self, list: list):
        """Creates a sigle string from a list of characters created by parseline funcion.
        """
        output = ""
        for i in list:
            output += i
        return output.strip()

    def parseline(self, line: str):
        """Accepts a string, tries to find formatted parts of text which then formatted by the send_to_edit function.
        Returns a string formatted by html tags.
        """
        line = line.strip()
        syntax = [""]
        string = [""]
        skip = False
        link = False
        escape = False
        linkbody = [""]
        temp = ""
        for index, i in enumerate(line):
            if skip:
                skip = False
                continue
            if escape:
                string[-1] += i
                escape = False
                continue
            if i == "\\":
                escape = True
                continue
            if link:
                if i == "]":
                    linkbody = temp
                    temp = ""
                elif i == "(":
                    continue
                elif i == ")":
                    link = False
                    string[-1] += con.link(linkbody, temp)
                    temp = ""
                else:
                    temp += i
                continue
            elif i == "[" and syntax[-1] != "`":
                x = re.search(r"[\[][^\[\]]*[]][(][^\[\])]*[)]", line[index:])
                """uses regular expression to see if the rest of current line contains a sequence of characters
                that mark a link. is processed as regular text otherwise
                """
                if x and x.start() == 0:
                    link = True
                    continue

            if i in self.syntax_inline and (i in syntax or line[index+1:].count(i) % 2 == 1):
                if i != "`" and syntax[-1] == "`":
                    string[-1] += i
                    continue
                if len(line) != index+1:  # current character is an operator and is followed by the same type (e.g. **)
                    if line[index+1] == i and i != syntax[-1]:
                        i += line[index+1]
                        skip = True  # the following char is not processed
                if i == "=":
                    string[-1] += i
                    continue
                if i in syntax:
                    if i == syntax.pop():
                        s = string.pop()
                        if syntax == [""]:
                            string.append("")
                        string[-1] += self.send_to_edit(i, s)
                        if syntax == [""]:
                            string.append("")
                else:
                    syntax.append(i)
                    string.append("")
            else:
                string[-1] += i
        string = self.condese(string)
        return string

    def lists(self, level):
        """Finds any unfinished indented lists and appends them to the correct previous list. "level" variable indicates which
        lists level is to be kept unfinished. -1 finishes all lists and appends them to output.
        """
        for i in range(3, level, -1):
            if level == -1 and i == 0: break
            olists = [self.olist, self.olist1, self.olist2, self.olist3]
            ulists = [self.ulist, self.ulist1, self.ulist2, self.ulist3]
            if olists[i] != [] or ulists[i] != []:
                if olists[i] != []:
                    temp = con.ol(olists[i])
                    olists[i][:] = []
                else:
                    temp = con.ul(ulists[i])
                    ulists[i][:] = []
                if ulists[i-1] != []:
                    ulists[i-1][-1] += "\n" + temp
                elif olists[i-1] != []:
                    olists[i-1][-1] +=  temp
        if level == -1:
            if self.ulist != []:
                self.output += con.ul(self.ulist) + "\n"
                self.ulist[:] = []
            elif self.olist != []:
                self.output += con.ol(self.olist) + "\n"
                self.olist[:] = []

    def parse_heading(self, string):
        """Calculates heading level by the ammount of '#' characters. Formats it with with heading tags.
        The rest of string (without # symbols) is processed as a regular line by the parseline function.
        """
        level = 0
        i = "#"
        id = None
        while i == "#":
            level += 1
            i = string[level]
        if level > 6:
            raise Exception("Markdown a HTML podporuje pouze 6 úrovní nadpisů."
                            "Ve vstupním souboru byl někde nadpis úrovně 7 nebo větší.")
        if string[level] == " ":
            string = string[level+1:]
        else:
            string = string[level:]
        x = re.search(r"[{][#].*[}]", string)  # heading1 {#id}
        if x:
            id = x[0][2:-1]
            string = string[:x.start()]
        string = self.parseline(string)
        return con.heading(str(level), string, id)

    def run(self):
        """Main part of the file processing. Reads the file line by line, determines whether it's a heading, (un)ordered list, codeblock, etc.
        Each line is processed by the parseline funcion (without any leading characters, eg. '* ' for unordered lists) to convert
        any in-line formatting, except for codeblocks which are not formatted.
        """
        self.output = ""
        paragraph = ""
        codeblock = ""
        code = False
        blockquote = ""
        self.ulist = []
        self.ulist1 = []
        self.ulist2 = []
        self.ulist3 = []
        self.olist = []
        self.olist1 = []
        self.olist2 = []
        self.olist3 = []
        bad_indent = False
        olists = [self.olist, self.olist1, self.olist2, self.olist3]
        ulists = [self.ulist, self.ulist1, self.ulist2, self.ulist3]
        with open(self.filename, mode='r', encoding="utf-8") as file:
            for i in file:
                i = i.rstrip("\r\n")  # strips only LF, CR or CRLF
                ol = False
                ul = False
                if i == "":
                    self.lists(-1)
                    if paragraph != "":
                        self.output += con.paragraph(paragraph) + "\n"
                        paragraph = ""
                    if blockquote != "":
                        self.output += con.blockquote(blockquote) + "\n"
                        blockquote = ""
                elif i[0] == "#":  # heading
                    if paragraph != "":
                        self.output += con.paragraph(paragraph) + "\n"
                        paragraph = ""
                    self.lists(-1)
                    self.output += self.parse_heading(i) + "\n"
                elif i == "---" or i == "***":  # horizontal separator
                    if paragraph != "":
                        self.output += con.paragraph(paragraph) + "\n"
                        paragraph = ""
                    self.output += "<br>\n"
                elif i[0:2] == "> ":
                    blockquote += (self.parseline(i[2:])) + "\n"
                    continue
                elif i == "```":  # codeblock
                    if code:
                        code = False
                        self.output += con.codeblock(codeblock) + "\n"
                        codeblock = ""
                    else:
                        if paragraph != "":
                            self.output += con.paragraph(paragraph) + "\n"
                            paragraph = ""
                        self.lists(-1)
                        code = True
                elif code:
                    codeblock += i + "\n"
                    continue
                elif i[0] == "!":  # could be an image
                    x = re.search(r"[!][\[].*[]][(].*[)]", i)
                    # try to find a squence of characters that define an embedded image
                    if x:  # assumes that re.search() returns None if nothing found
                        imgname = re.search(r"[\[].*[]]", i)  # assumes None is not returned since expression on line 251 found something
                        imgname = imgname[0][1:-1]
                        imglink = re.search(r"[(].*[)]", i)
                        imglink = imglink[0][1:-1]
                        self.output += con.img(imgname, imglink) + "\n"
                elif i.lstrip()[0] == "*" or i.lstrip()[0] == "-" or i.lstrip()[0] == "+":
                    for j in range(4):
                        if i[self.indent*j:self.indent*j+2] == "* " or i[self.indent*j:self.indent*j+2] == "- " or i[self.indent*j:self.indent*j+2] == "+ ":
                            ul = True
                            if j < 3:
                                self.lists(j)
                            temp = self.parseline(i[self.indent*j+2:])
                            ulists[j].append(temp)
                            break
                elif i.strip()[0].isdigit():
                    for j in range(4):
                        if len(i) >= self.indent and i[self.indent*j].isdigit() and i[self.indent*j+1:self.indent*j+3] == ". ":
                            ol = True
                            if j < 3:
                                self.lists(j)
                            temp = self.parseline(i[self.indent*j+3:])
                            olists[j].append(temp)
                            break
                elif i[-1] == " ":
                    paragraph += self.parseline(i.rstrip()) + "<br>" + "\n"
                else:
                    paragraph += self.parseline(i) + "\n"
                if (self.olist != [] or self.ulist != []) and not ol and not ul:
                    if not bad_indent:
                        print("V textu byla nalezena chybná indentace seznamů. Zkontrolujte prosím vstupní soubor a "
                            + "nastavení indentace v konfiguračním souboru.")
                        bad_indent = True
                    lists = [self.olist3, self.ulist3, self.olist2, self.ulist2, self.olist1, self.ulist1, self.olist, self.ulist]
                    for j in lists:
                        if j != []:
                            j[-1] += "<br>\n" + self.parseline(i)
                            break
                elif not ol and not ul and i != "" and (i.lstrip()[0] == "*" or i.lstrip()[0].isdigit()):
                    paragraph += self.parseline(i) + "\n"

            self.lists(-1)  # process any lists that weren't processed yet
            if paragraph != "":
                self.output += con.paragraph(paragraph)
            if blockquote != "":
                self.output += con.blockquote(blockquote) + "\n"
        return self.output


con = html_convertor.Convertor()
