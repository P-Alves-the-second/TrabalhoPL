import csv

def load_csv(file_path):
    with open(file_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(filter(lambda row: not row.strip().startswith('#'), f))
        return list(reader)

def save_csv(file_path, rows, columns=None):
    if not rows:
        return
    with open(file_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=columns or rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
