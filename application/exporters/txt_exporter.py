# application/exporters/txt_exporter.py
import os

class TxtExporter:
    def export(self, contact, messages, out_path):
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(f"Chat with: {contact.get('NickName') or contact.get('Remark') or contact.get('UserName')}\n\n")
            for m in messages:
                f.write(f"{m.get('create_time')}\t{m.get('talker')}\t{m.get('content')}\n")
        return out_path