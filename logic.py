def add_task(tasks, title, note, date):
    tasks.append({"title": title, "note": note, "date": date})
    return tasks

def delete_task(tasks, index):
    if 0 <= index < len(tasks):
        del tasks[index]
    return tasks

def edit_task(tasks, index, new_title, new_note):
    if 0 <= index < len(tasks):
        tasks[index]["title"] = new_title
        tasks[index]["note"] = new_note
    return tasks