class Convertor:
    def __init__(self) -> None:
        pass

    def heading(self, level, text, id):
        if type(level) is not str:
            level = str(level)
        if id:
            element = "<h" + level + " id=" + f'"{id}"' + ">" + text + "</h" + level + ">"
        else:
            element = "<h" + level + ">" + text + "</h" + level + ">"
        return element

    def bold(self, string):
        element = f"<em>{string}</em>"
        return element

    def italics(self, string):
        element = f"<i>{string}</i>"
        return element

    def strikethrough(self, string):
        element = f"<s>{string}</s>"
        return element

    def subscript(self, string):
        element = f"<sub>{string}</sub>"
        return element

    def code(self, string):
        element = f"<code>{string}</code>"
        return element

    def mark(self, string):
        element = f"<mark>{string}</mark>"
        return element

    def codeblock(self, string):
        element = f"<pre><code>{string}</code></pre>"
        return element

    def blockquote(self, string):
        element = f"<blockquote>{string}</blockquote>"
        return element

    def link(self, string, linkto):
        element = f'<a href="{linkto}">{string}</a>'
        return element

    def paragraph(self, string):
        element = f"<p>{string.strip()}</p>"
        return element

    def ol(self, strings):
        element = "<ol>\n"
        for i in strings:
            if i[:4] == "<ol>":
                element += i + "\n"
            else:
                element += "<li>" + i + "</li>" + "\n"
        element += "</ol>"
        return element

    def ul(self, strings):
        element = "<ul>\n"
        for i in strings:
            if i[:4] == "<ul>":
                element += i + "\n"
            else:
                element += "<li>" + i + "</li>" + "\n"
        element += "</ul>"
        return element

    def img(self, imgname, imglink):
        element = f'<img src="{imglink}" alt="{imgname}">'
        return element
