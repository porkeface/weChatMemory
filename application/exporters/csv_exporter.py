# application/exporters/csv_exporter.py
import os
import csv

class CsvExporter:
    def export(self, contact, messages, out_path):
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['create_time', 'talker', 'content', 'type'])
            for m in messages:
                writer.writerow([m.get('create_time'), m.get('talker'), m.get('content'), m.get('type')])
        return out_path