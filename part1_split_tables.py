import pandas as pd
from faker import Faker
import numpy as np

fake_ru = Faker('ru_RU')

# Фиксируем seed для воспроизводимости (опционально)
np.random.seed(42)

n_groups = np.random.randint(5, 11)         # 5-10 групп
n_teachers = np.random.randint(5, 11)       # 5-10 учителей
n_classrooms = np.random.randint(5, 11)     # 5-10 аудиторий
n_subjects = np.random.randint(8, 16)       # 8-15 предметов

# Таблица "Группы"
df_groups = pd.DataFrame({
    'id_группы': range(1, n_groups + 1),
    'количество_человек': np.random.randint(10, 31, n_groups),
})

# Таблица "Учителя"
df_teachers = pd.DataFrame({
    'id_преподавателя': range(1000, 1000 + n_teachers),
    'преподаватель': [fake_ru.name() for _ in range(n_teachers)],
})

# Таблица "Аудитории"
df_classrooms = pd.DataFrame({
    'номер_аудитории': range(100, 100 + n_classrooms),
    'вместимость': np.random.randint(15, 30, n_classrooms),
})

# Таблица "Предметы"
df_subjects = pd.DataFrame({
    'id_предмета': range(1, n_subjects + 1),
    'предмет': [f"Предмет {i}" for i in range(1, n_subjects + 1)],
    'id_преподавателя': np.random.choice(df_teachers['id_преподавателя'], n_subjects),
    'id_группы': np.random.choice(df_groups['id_группы'], n_subjects),
    'часов_в_неделю': np.random.choice([1, 2, 3, 4], n_subjects)  # нагрузка
})

# Сохранение
df_groups.to_csv('группы.csv', index=False, encoding='utf-8-sig')
df_teachers.to_csv('учителя.csv', index=False, encoding='utf-8-sig')
df_classrooms.to_csv('аудитории.csv', index=False, encoding='utf-8-sig')
df_subjects.to_csv('предметы.csv', index=False, encoding='utf-8-sig')

