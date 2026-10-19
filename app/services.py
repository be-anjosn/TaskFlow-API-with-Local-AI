import csv
import os
import ollama
from schemas import TarefaModelo
from datetime import date
from pydantic import ValidationError

INPUT_FILE = "D:/vscode/Estudos-IA/Project-2/data/input_tasks.csv"
OUTPUT_FILE = "D:/vscode/Estudos-IA/Project-2/data/output_tasks.csv"
OUTPUT_HEADERS = ["id", "title", "description", "priority", "status", "due_date"]
VALID_STATUSES = {"pending", "in_progress", "completed"}

def ai_generation(argument):
    message = {
        'role': 'user',
        'content': f"""
            Extract the information from the text below and return EXCLUSIVELY a SINGLE JSON object. Do not use arrays and do not add extra text. If necessary, translate to english.

            RULES:
            1. "title": Maximum of 5 words. Create a descriptive title based on the main content. NEVER repeat generic titles from previous tests.
            2. "description": Detailed context of the task.
            3. "priority": Strictly "low", "medium", or "high" (Convert "medium urgency" to "medium").
            4. "status": Strictly "pending", "in_progress", or "completed".
            5. "due_date": Format "YYYY-MM-DD" or null.

            TEXT:
            {argument}
        """
    }

    awnser = ollama.chat(
        model='llama3.2:1b', 
        messages=[message],
        format=TarefaModelo.model_json_schema(),
        options={'temperature': 0.1}
    )

    return awnser['message']['content']


def get_next_output_id(file_path: str) -> int:
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        return 1

    last_id = 0
    with open(file_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("id"):
                try:
                    last_id = max(last_id, int(row["id"]))
                except ValueError:
                    continue
    return last_id + 1

def append_to_output(file_path: str, processed_data: dict, fieldnames: list[str]) -> None:
    file_exists = os.path.exists(file_path) and os.path.getsize(file_path) > 0
    next_id = get_next_output_id(file_path)
    processed_data["id"] = next_id

    with open(file_path, mode="a", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(processed_data)

def process_new_task(new_row: dict) -> dict:
    
    try:
        text_response = ai_generation(new_row)
        validated_model = TarefaModelo.model_validate_json(text_response)
        parsed_task = validated_model.model_dump()
    except ValidationError as e:
        raise RuntimeError(f"Pydantic blocked by AI: {e}")

    if os.path.exists(OUTPUT_FILE) and os.path.getsize(OUTPUT_FILE) > 0:
        with open(OUTPUT_FILE, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get("title") == parsed_task["title"]:
                    raise ValueError(f"Tasks already exists with title: {parsed_task['title']}")

    append_to_output(OUTPUT_FILE, parsed_task, fieldnames=OUTPUT_HEADERS)
    return parsed_task

def change_task(task_id: int, new_status: str) -> dict:
    if new_status not in VALID_STATUSES:
        raise ValueError(f"Invalid Status: '{new_status}'. Use: {VALID_STATUSES}")

    if not os.path.exists(OUTPUT_FILE) or os.path.getsize(OUTPUT_FILE) == 0:
        raise FileNotFoundError(f"File not found or empty: {OUTPUT_FILE}")

    changed_lines = []
    modified = None

    with open(OUTPUT_FILE, mode="r", encoding="utf-8") as f_in:
        reader = csv.DictReader(f_in)
        fieldnames = reader.fieldnames or OUTPUT_HEADERS
        
        for row in reader:
            if str(row.get("id")) == str(task_id):
                row["status"] = new_status
                modified = row
            changed_lines.append(row)

    if not modified:
        raise ValueError(f"Task with ID: {task_id} not found")

    with open(OUTPUT_FILE, mode="w", encoding="utf-8", newline="") as f_out:
        writer = csv.DictWriter(f_out, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(changed_lines)

    return modified

def get_all_tasks(status_filter = None, priority_filter = None) -> list[dict]:
    if not os.path.exists(OUTPUT_FILE) or os.path.getsize(OUTPUT_FILE) == 0:
        return []

    tasks = []
    with open(OUTPUT_FILE, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("id"):
                try:
                    row["id"] = int(row["id"])
                except ValueError:
                    pass

            if status_filter and row.get("status") != status_filter:
                continue
            if priority_filter and row.get("priority") != priority_filter:
                continue

            tasks.append(row)
    return tasks

def find_task_in_csv(task_id: int) -> dict | None:
    if not os.path.exists(OUTPUT_FILE) or os.path.getsize(OUTPUT_FILE) == 0:
        return None

    with open(OUTPUT_FILE, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("id"):
                try:
                    if int(row["id"]) == task_id:
                        row["id"] = int(row["id"])
                        return row
                except ValueError:
                    continue
    return None

def delete_task_from_csv(task_id: int) -> bool:
    if not os.path.exists(OUTPUT_FILE) or os.path.getsize(OUTPUT_FILE) == 0:
        return False

    all_lines = []
    task = None

    with open(OUTPUT_FILE, mode="r", encoding="utf-8") as f_in:
        reader = csv.DictReader(f_in)
        fieldnames_out = reader.fieldnames or OUTPUT_HEADERS
        
        for row in reader:
            if row.get("id"):
                try:
                    if int(row["id"]) == task_id:
                        task = row
                        continue
                except ValueError:
                    pass
            all_lines.append(row)

    if not task:
        return False

    with open(OUTPUT_FILE, mode="w", encoding="utf-8", newline="") as f_out:
        writer = csv.DictWriter(f_out, fieldnames=fieldnames_out)
        writer.writeheader()
        writer.writerows(all_lines)

    if os.path.exists(INPUT_FILE) and os.path.getsize(INPUT_FILE) > 0:
        all_lines_input = []
        with open(INPUT_FILE, mode="r", encoding="utf-8") as f_in_input:
            reader_input = csv.DictReader(f_in_input)
            fieldnames_in = reader_input.fieldnames
            
            for row in reader_input:
                if row.get("title") == task.get("title"):
                    continue
                all_lines_input.append(row)

        if fieldnames_in:
            with open(INPUT_FILE, mode="w", encoding="utf-8", newline="") as f_out_input:
                writer_input = csv.DictWriter(f_out_input, fieldnames=fieldnames_in)
                writer_input.writeheader()
                writer_input.writerows(all_lines_input)

    return True

def update_full_task(task_id: int, updated_data: dict) -> dict:
    if not os.path.exists(OUTPUT_FILE) or os.path.getsize(OUTPUT_FILE) == 0:
        raise FileNotFoundError(f"❌ Arquivo não encontrado ou vazio: {OUTPUT_FILE}")

    changed_lines = []
    changed_task = None

    with open(OUTPUT_FILE, mode="r", encoding="utf-8") as f_in:
        reader = csv.DictReader(f_in)
        fieldnames = reader.fieldnames or OUTPUT_HEADERS
        
        for row in reader:
            if str(row.get("id")) == str(task_id):
                for key, value in updated_data.items():
                    if key in row and key != "id":
                        row[key] = value
                changed_task = row
            changed_lines.append(row)

    if not changed_task:
        raise ValueError(f"❌ Nenhuma tarefa com ID {task_id} foi encontrada.")

    with open(OUTPUT_FILE, mode="w", encoding="utf-8", newline="") as f_out:
        writer = csv.DictWriter(f_out, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(changed_lines)

    return changed_task

def get_overdue_tasks() -> list[dict]:
    if not os.path.exists(OUTPUT_FILE) or os.path.getsize(OUTPUT_FILE) == 0:
        return []

    overdue = []
    today = date.today()

    with open(OUTPUT_FILE, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("status") == "completed":
                continue

            due_date_str = row.get("due_date")
            if due_date_str:
                try:
                    due_on = date.fromisoformat(due_date_str)
                    if due_on < today:
                        if row.get("id"):
                            row["id"] = int(row["id"])
                        overdue.append(row)
                except ValueError:
                    pass

    return overdue