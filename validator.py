import pandas as pd
from collections import defaultdict


def validate_schedule(file_path: str):
    schedule = pd.read_excel(file_path, header=None, dtype=str)
    
    group_schedule = defaultdict(list)
    room_schedule = defaultdict(list)
    teacher_schedule = defaultdict(list)
    errors = []
    lesson_num = 1
    first_cell_prev = ""

    for _, row in schedule.iterrows():
        first_cell = row[0]
        if pd.isna(first_cell):
            continue
        
        if first_cell.startswith("группа"):
            current_group = first_cell
            continue

        if first_cell == first_cell_prev:
            lesson_num += 1
        else:
            lesson_num = 1
        
        group_schedule[current_group].append({
            "day": first_cell,
            "lesson_num": lesson_num,
            "teacher": row[2],
            "room": row[3]
        })

        first_cell_prev = first_cell
    
    for group_name, lessons in group_schedule.items():
        for lesson in lessons:
            key = (lesson["teacher"], lesson["day"], lesson["lesson_num"])
            teacher_schedule[key].append((group_name, lesson["room"]))
    
    for (teacher, day, lesson), occurrences in teacher_schedule.items():
        if len(occurrences) > 1:
            rooms = [f"{grp}->{room}" for grp, room in occurrences]
            errors.append(
                f"Преподаватель {teacher} в {day} на {lesson} паре "
                f"одновременно в разных аудиториях: {', '.join(rooms)}"
            )
    
    for group_name, lessons in group_schedule.items():
        for lesson in lessons:
            key = (lesson["room"], lesson["day"], lesson["lesson_num"])
            room_schedule[key].append(group_name)
    
    for (room, day, lesson), groups in room_schedule.items():
        if len(groups) > 1:
            errors.append(
                f"Аудитория {room} в {day} на {lesson} паре "
                f"занята одновременно группами: {', '.join(groups)}"
            )
    
    return errors


if __name__ == "__main__":
    file_path = "valid_schedule.xlsx"
    errors = validate_schedule(file_path)
    
    if errors:
        print("Найдены ошибки в расписании:")
        for err in errors:
            print(err)
    else:
        print("👍")
