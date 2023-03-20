from dataclasses import dataclass

def is_notebook() -> bool:
    try:
        from IPython import get_ipython
        shell = get_ipython().__class__.__name__
        if shell == 'ZMQInteractiveShell':
            return True   # Jupyter notebook or qtconsole
        elif shell == 'TerminalInteractiveShell':
            return False  # Terminal running IPython
        else:
            return False  # Other type (?)
    except NameError:
        return False      # Probably standard Python interpreter
    
@dataclass
class HtmlPrinter:
    font_size:int = 15
    line_height:float = 1.5
    white_space: str = "pre-wrap"
    width: int = 1000
    text_align: str = "justify"
    font_family: str = "HelveticaNeue-Light"


    @property
    def open_tag(self):
        return f'<div style="font-size: {self.font_size}px; line-height:{self.line_height}em; white-space: {self.white_space}; width:{self.width}px; text-align:{self.text_align}; font-family:{self.font_family}">'
    
    @property
    def close_tag(self):
        return "</div>"
    
    def __call__(self, content):
        from IPython.display import display, HTML
        display(HTML(self.open_tag + content + self.close_tag))


@dataclass
class MarkdownPrinter:
    def __call__(self, content):
        from IPython.display import display, Markdown
        display(Markdown(content))




