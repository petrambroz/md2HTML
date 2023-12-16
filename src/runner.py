from . import convertor
import re


class runner:
    def __init__(self, language: str, title: str, filename="input.md"):
        self.language = language
        self.title = title
        with open(filename, 'r') as file:
            self.text = file.read()
        self.text = self.text.splitlines()
        self.syntax_inline = ["*", "*", "_", "_", "~", "`"]
        # self.synatax_block = ["#", "```"]
        self.indent = 2
        self.indent1 = self.indent*" "
        self.indent2 = 2*self.indent*" "
        self.indent3 = 3*self.indent*" "

    def make_file(self):
        html_boilerplate = '<!DOCTYPE html>\n'\
            f'<html lang="{self.language}">\n'\
            '<head>\n'\
            '    <meta charset="UTF-8">\n'\
            '    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n'\
            f'    <title>{self.title}</title>\n'\
            '</head>\n'\
            '<body>\n'
        with open("output.html", "w") as f:
            data = html_boilerplate
            f.write(data)

    def save_file(self, data):
        with open("output.html", "a") as f:
            f.write(data + "\n</body>")

    def _out(self):  # unused
        print(self.text)

    def send_to_edit(self, syntax, string):
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
        return result

    def condese(self, list):
        output = ""
        for i in list:
            output += i
        return output.strip()

    def parseline(self, line: str):
        line = line.strip()
        syntax = [""]
        string = [""]
        skip = False
        link = False
        linkbody = [""]
        temp = ""
        for index, i in enumerate(line):
            if skip:
                skip = False
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
            elif i == "[":
                x = re.search(r"[\[][^\[\]]*[]][(][^\[\])]*[)]", line[index:])
                """uses regular expression to see if the rest of current line contains a sequence of characters
                that mark a link. skips it otherwise
                """
                if x and x.start() == 0:
                    link = True
                    continue

            if i in self.syntax_inline and (line[index+1:].count(i) % 2 == 1 or i in syntax):
                if len(line) != index+1:
                    if line[index+1] == i and i != syntax[-1]:
                        i += line[index+1]
                        skip = True
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

    def parse_heading(self, string):
        level = 0
        i = "#"
        id = None
        while i == "#":
            level += 1
            i = string[level]
        if level > 6:
            raise Exception("MarkDown and HTML only support 6 levels of headings. There was a heading with level 7 or more in your file.")
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
        output = ""
        paragraph = ""
        codeblock = ""
        code = False
        blockquote = ""
        ulist = []
        ulist1 = []
        ulist2 = []
        ulist3 = []
        olist = []
        olist1 = []
        olist2 = []
        olist3 = []

        for i in self.text:
            if i == "":
                if ulist != []:
                    if ulist1 != []:
                        ulist1.append(con.ul(ulist2))
                        ulist2 = []
                    elif olist1 != []:
                        ulist[-1] += (con.ol(olist1))
                        olist1 = []
                    if ulist2 != []:
                        ulist.append(con.ul(ulist1))
                        ulist1 = []
                    elif olist2 != []:
                        ulist1[-1] += (con.ol(olist2))
                        olist2 = []
                    if ulist3 != []:
                        ulist2.append(con.ul(ulist3))
                        ulist3 = []
                    elif olist3 != []:
                        ulist2[-1] += (con.ol(olist3))
                        olist3 = []
                    output += con.ul(ulist) + "\n"
                    ulist = []

                if olist != []:
                    if olist1 != []:
                        olist.append(con.ol(olist1))
                        olist1 = []
                    elif ulist1 != []:
                        olist[-1] += (con.ul(ulist1))
                        ulist1 = []
                    if olist2 != []:
                        olist1.append(con.ol(olist2))
                        olist2 = []
                    elif ulist2 != []:
                        olist1[-1] += (con.ul(ulist2))
                        ulist2 = []
                    if olist3 != []:
                        olist2.append(con.ol(olist3))
                        olist3 = []
                    elif ulist3 != []:
                        olist2[-1] += (con.ol(ulist3))
                        ulist3 = []
                    output += con.ol(olist) + "\n"
                    olist = []
                """
                if ulist != []:
                    if ulist1 != []:
                        if ulist2 != []:
                            if ulist3 != []:
                                ulist2.append(con.ul(ulist3))
                                ulist3 = []
                            elif olist3 != []:
                                ulist2[-1] += (con.ol(olist3))
                                olist3 = []
                            ulist1.append(con.ul(ulist2))
                            ulist2 = []
                        elif olist2 != []:
                            ulist1[-1] += (con.ol(olist2))
                            olist2 = []
                        ulist.append(con.ul(ulist1))
                        ulist1 = []
                    elif olist1 != []:
                        ulist[-1] += (con.ol(olist1))
                        olist1 = []
                    output += con.ul(ulist) + "\n"
                    ulist = []
                if olist != []:
                    if olist1 != []:
                        if olist2 != []:
                            if olist3 != []:
                                olist2.append(con.ol(olist3))
                                olist3 = []
                            elif ulist3 != []:
                                olist2[-1] += (con.ol(ulist3))
                                ulist3 = []
                            olist1.append(con.ol(olist2))
                            olist2 = []
                        elif ulist2 != []:
                            olist1[-1] += (con.ul(ulist2))
                            ulist2 = []
                        olist.append(con.ol(olist1))
                        olist1 = []
                    elif ulist1 != []:
                        olist[-1] += (con.ul(ulist1))
                        ulist1 = []
                    output += con.ol(olist) + "\n"
                    olist = []"""
                if paragraph != "":
                    output += con.paragraph(paragraph) + "\n"
                    paragraph = ""
                if blockquote != "":
                    output += con.blockquote(blockquote) + "\n"
                    blockquote = ""
            elif i[0] == "#":
                if paragraph != "":
                    output += con.paragraph(paragraph) + "\n"
                output += self.parse_heading(i) + "\n"
            elif i == "---":
                output += "<br>\n"
            elif i[0:2] == "> ":
                blockquote += (self.parseline(i[2:])) + "\n"
                continue
            elif i == "```":
                if code:
                    code = False
                    paragraph += con.codeblock(codeblock)
                else:
                    code = True
            elif i[0] == "!":
                x = re.search(r"[!][\[].*[]][(].*[)]", i)
                if x:
                    imgname = re.search(r"[\[].*[]]", i)
                    imgname = imgname[0][1:-1]
                    imglink = re.search(r"[(].*[)]", i)
                    imglink = imglink[0][1:-1]
                    output += con.img(imgname, imglink) + "\n"

            elif i[:2] == "* " or i[:2] == "- " or i[:2] == "+ ":
                if ulist3 != []:
                    temp = con.ul(ulist3)
                    ulist2.append(temp)
                    ulist3 = []
                elif olist3 != []:
                    temp = con.ol(olist3)
                    ulist2[-1]+=(temp)
                    olist3 = []
                if ulist2 != []:
                    temp = con.ul(ulist2)
                    ulist1.append(temp)
                    ulist2 = []
                elif olist2 != []:
                    temp = con.ol(olist2)
                    ulist1[-1]+=(temp)
                    olist2 = []
                if ulist1 != []:
                    temp = con.ul(ulist1)
                    ulist.append(temp)
                    ulist1 = []
                elif olist1 != []:
                    temp = con.ol(olist1)
                    ulist[-1]+=(temp)
                    olist1 = []
                temp = self.parseline(i[2:])
                ulist.append(temp)

            elif i[:self.indent+2] == self.indent1 + "* " or i[:self.indent+2] == self.indent1 + "+ " or i[:self.indent+2] == self.indent1 + "- ":
                """ line is a list ad 1st depth
                """
                if ulist3 != []:
                    temp = con.ul(ulist3)
                    ulist2.append(temp)
                    ulist3 = []
                elif olist3 != []:
                    temp = con.ol(olist3)
                    ulist2[-1]+=(temp)
                    olist3 = []
                if ulist2 != []:
                    temp = con.ul(ulist2)
                    ulist1.append(temp)
                    ulist2 = []
                elif olist2 != []:
                    temp = con.ol(olist2)
                    ulist1[-1]+=(temp)
                    olist2 = []
                temp = self.parseline(i[self.indent+2:])
                ulist1.append(temp)

            elif i[:self.indent*2+2] == self.indent2 + "* " or i[:self.indent*2+2] == self.indent2 + "+ " or i[:self.indent*2+2] == self.indent2 + "- ":
                if ulist3 != []:
                    temp = con.ul(ulist3)
                    ulist2.append(temp)
                    ulist3 = []
                elif olist3 != []:
                    temp = con.ol(olist3)
                    ulist2[-1]+(temp)
                    olist3 = []
                temp = self.parseline(i[2*self.indent+2:])
                ulist2.append(temp)

            elif i[:self.indent*3+2] == self.indent3 + "* " or i[:self.indent*3+2] == self.indent3 + "+ " or i[:self.indent*3+2] == self.indent3 + "- ":
                temp = self.parseline(i[3*self.indent+2:])
                ulist3.append(temp)

            elif i[0].isdigit() and i[1:3] == ". ":
                if olist3 != []:
                    temp = con.ol(olist3)
                    olist2.append(temp)
                    olist3 = []
                elif ulist3 != []:
                    temp = con.ul(ulist3)
                    olist2[-1]+=(temp)
                    ulist3 = []
                if olist2 != []:
                    temp = con.ol(olist2)
                    olist1.append(temp)
                    olist2 = []
                elif ulist2 != []:
                    temp = con.ul(ulist2)
                    olist1[-1]+=(temp)
                    ulist2 = []
                if olist1 != []:
                    temp = con.ol(olist1)
                    olist.append(temp)
                    olist1 = []
                elif ulist1 != []:
                    temp = con.ul(ulist1)
                    olist[-1]+=(temp)
                    ulist1 = []
                temp = self.parseline(i[3:])
                olist.append(temp)
            elif i[self.indent].isdigit() and i[self.indent+1:self.indent+3] == ". ":
                if olist3 != []:
                    temp = con.ol(olist3)
                    olist2.append(temp)
                    olist3 = []
                elif ulist3 != []:
                    temp = con.ul(ulist3)
                    olist2[-1]+=(temp)
                    ulist3 = []
                if olist2 != []:
                    temp = con.ol(olist2)
                    olist1.append(temp)
                    olist2 = []
                elif ulist2 != []:
                    temp = con.ul(ulist2)
                    olist1[-1]+=(temp)
                    ulist2 = []
                temp = self.parseline(i[self.indent+3:])
                olist1.append(temp)
            elif i[self.indent*2].isdigit() and i[self.indent*2+1:self.indent*2+3] == ". ":
                if olist3 != []:
                    temp = con.ol(olist3)
                    olist2.append(temp)
                    olist3 = []
                elif ulist3 != []:
                    temp = con.ul(ulist3)
                    olist2[-1]+=(temp)
                    ulist3 = []
                temp = self.parseline(i[self.indent*2+3:])
                olist2.append(temp)
            elif i[self.indent*3].isdigit() and i[self.indent*3+1:self.indent*3+3] == ". ":
                temp = self.parseline(i[self.indent*3+3:])
                olist3.append(temp)
            else:
                if code:
                    codeblock += i + "\n"
                    continue
                paragraph += self.parseline(i) + "<br>" + "\n"

        if ulist != []:
            if ulist1 != []:
                ulist1.append(con.ul(ulist2))
                ulist2 = []
            elif olist1 != []:
                ulist[-1] += (con.ol(olist1))
                olist1 = []
            if ulist2 != []:
                ulist.append(con.ul(ulist1))
                ulist1 = []
            elif olist2 != []:
                ulist1[-1] += (con.ol(olist2))
                olist2 = []
            if ulist3 != []:
                ulist2.append(con.ul(ulist3))
                ulist3 = []
            elif olist3 != []:
                ulist2[-1] += (con.ol(olist3))
                olist3 = []
            output += con.ul(ulist) + "\n"
            ulist = []

        elif olist != []:
            if olist1 != []:
                olist.append(con.ol(olist1))
                olist1 = []
            elif ulist1 != []:
                olist[-1] += (con.ul(ulist1))
                ulist1 = []
            if olist2 != []:
                olist1.append(con.ol(olist2))
                olist2 = []
            elif ulist2 != []:
                olist1[-1] += (con.ul(ulist2))
                ulist2 = []
            if olist3 != []:
                olist2.append(con.ol(olist3))
                olist3 = []
            elif ulist3 != []:
                olist2[-1] += (con.ol(ulist3))
                ulist3 = []
            output += con.ol(olist) + "\n"
            olist = []

        """if ulist != []:
            if ulist1 != []:
                if ulist2 != []:
                    if ulist3 != []:
                        ulist2.append(con.ul(ulist3))
                        ulist3 = []
                    elif olist3 != []:
                        ulist2[-1] += (con.ol(olist3))
                        olist3 = []
                    ulist1.append(con.ul(ulist2))
                    ulist2 = []
                elif olist2 != []:
                    ulist1[-1] += (con.ol(olist2))
                    olist2 = []
                ulist.append(con.ul(ulist1))
                ulist1 = []
            elif olist1 != []:
                ulist[-1] += (con.ol(olist1))
                olist1 = []
            output += con.ul(ulist) + "\n"
            ulist = []
        if olist != []:
            if olist1 != []:
                if olist2 != []:
                    pass
            output += con.ol(olist)
            olist = []
        if olist != []:
            if olist1 != []:
                if olist2 != []:
                    if olist3 != []:
                        olist2.append(con.ol(olist3))
                        olist3 = []
                    elif ulist3 != []:
                        olist2[-1] += (con.ol(ulist3))
                        ulist3 = []
                    olist1.append(con.ol(olist2))
                    olist2 = []
                elif ulist2 != []:
                    olist1[-1] += (con.ul(ulist2))
                    ulist2 = []
                olist.append(con.ol(olist1))
                olist1 = []
            elif ulist1 != []:
                olist[-1] += (con.ul(ulist1))
                ulist1 = []
            output += con.ol(olist) + "\n"
            olist = []"""


        """
        if ulist3 != []:
            temp = con.ul(ulist3)
            ulist2.append(temp)
        if ulist2 != []:
            temp = con.ul(ulist2)
            ulist1.append(temp)
        if ulist1 != []:
            temp = con.ul(ulist1)
            ulist.append(temp)
        if ulist != []:
            output += con.ul(ulist)

        if olist3 != []:
            temp = con.ol(olist3)
            olist2.append(temp)
        if olist2 != []:
            temp = con.ol(olist2)
            olist1.append(temp)
        if olist1 != []:
            temp = con.ol(olist1)
            olist.append(temp)
        if olist != []:
            output += con.ol(olist)"""
        if paragraph != "":
            output += con.paragraph(paragraph)
        if blockquote != "":
            output += con.blockquote(blockquote) + "\n"
        return output


con = convertor.convertor()

if __name__ == "__main__":
    a = runner("cs", "ahoj")
    print(a.parseline("ah **j*s*e** máš?"))
