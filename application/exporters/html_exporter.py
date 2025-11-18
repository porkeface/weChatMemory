# application/exporters/html_exporter.py
import os
from jinja2 import Environment, FileSystemLoader

class HtmlExporter:
    def __init__(self, template_dir="templates"):
        self.env = Environment(loader=FileSystemLoader(template_dir))

    def export(self, contact, messages, out_path):
        tmpl = self.env.get_template('chat_template.html')
        html = tmpl.render(contact=contact, messages=messages)
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(html)
        return out_path