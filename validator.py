import pandas as pd


def get_df_grouped(df: pd.DataFrame, check: str):
    cols = [check] + ['day', 'lesson_number']
    duplicates = df[cols].duplicated(keep=False)
    df_grouped = df[duplicates].groupby(cols)
    return df_grouped


def check_teachers(df: pd.DataFrame, errors: list[str]):
    df_grouped = get_df_grouped(df, 'teacher')
    for (teacher, day, lesson_number), df_group in df_grouped:
        rooms = df_group['room']
        errors.append(f"Teacher {teacher} is in {', '.join(rooms)} at {day}, lesson №{lesson_number}")


def check_rooms(df: pd.DataFrame, errors: list[str]):
    df_grouped = get_df_grouped(df, 'room')
    for (room, day, lesson_number), df_group in df_grouped:
        groups = df_group['group']
        errors.append(f"Room {room} occupied by groups {', '.join(groups)} at {day}, lesson №{lesson_number}")


def check_groups(df: pd.DataFrame, errors: list[str]):
    df_grouped = get_df_grouped(df, 'group')
    for (group, day, lesson_number), df_group in df_grouped:
        rooms = df_group['room']
        errors.append(f"Group {group} is in rooms {', '.join(rooms)} at {day}, lesson №{lesson_number}")


def validate_schedule(filepath: str) -> list[str]:
    df = pd.read_csv(filepath).astype(str)
    errors = []
    check_teachers(df, errors)
    check_rooms(df, errors)
    check_groups(df, errors)
    return errors


if __name__ == '__main__':
    errors = validate_schedule("test_schedule.csv")

    for err in errors:
        print(err)
