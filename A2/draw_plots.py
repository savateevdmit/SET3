import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from matplotlib import rc


# Загрузка данных
standard_df = pd.read_csv('standard_results.csv')
hybrid_df = pd.read_csv('hybrid_results.csv')

# 1. Графики для стандартного Merge Sort

# График 1: Случайные данные
plt.figure(figsize=(10, 6))
random_data = standard_df[standard_df['type'] == 'random']
plt.plot(random_data['size'], random_data['time'], 'b-', linewidth=2.5, label='Случайные данные')
plt.xlabel('Размер массива (N)', fontsize=12)
plt.ylabel('Время выполнения (мкс)', fontsize=12)
plt.title('Время работы стандартного Merge Sort\nна случайных данных', fontsize=14, fontweight='bold')
plt.grid(True, alpha=0.3)
plt.legend(fontsize=11)
plt.tight_layout()
plt.savefig('standard_random.png', dpi=300)
plt.close()

# График 2: Обратно отсортированные данные
plt.figure(figsize=(10, 6))
reversed_data = standard_df[standard_df['type'] == 'reversed']
plt.plot(reversed_data['size'], reversed_data['time'], 'r-', linewidth=2.5, label='Обратно отсортированные данные')
plt.xlabel('Размер массива (N)', fontsize=12)
plt.ylabel('Время выполнения (мкс)', fontsize=12)
plt.title('Время работы стандартного Merge Sort\nна обратно отсортированных данных', fontsize=14, fontweight='bold')
plt.grid(True, alpha=0.3)
plt.legend(fontsize=11)
plt.tight_layout()
plt.savefig('standard_reversed.png', dpi=300)
plt.close()

# График 3: Почти отсортированные данные
plt.figure(figsize=(10, 6))
almost_sorted_data = standard_df[standard_df['type'] == 'almost_sorted']
plt.plot(almost_sorted_data['size'], almost_sorted_data['time'], 'g-', linewidth=2.5,
         label='Почти отсортированные данные')
plt.xlabel('Размер массива (N)', fontsize=12)
plt.ylabel('Время выполнения (мкс)', fontsize=12)
plt.title('Время работы стандартного Merge Sort\nна почти отсортированных данных', fontsize=14, fontweight='bold')
plt.grid(True, alpha=0.3)
plt.legend(fontsize=11)
plt.tight_layout()
plt.savefig('standard_almost_sorted.png', dpi=300)
plt.close()

# График 4: Общий график для стандартного Merge Sort
plt.figure(figsize=(10, 6))
plt.plot(random_data['size'], random_data['time'], 'b-', linewidth=2.5, label='Случайные данные')
plt.plot(reversed_data['size'], reversed_data['time'], 'r-', linewidth=2.5, label='Обратно отсортированные')
plt.plot(almost_sorted_data['size'], almost_sorted_data['time'], 'g-', linewidth=2.5, label='Почти отсортированные')
plt.xlabel('Размер массива (N)', fontsize=12)
plt.ylabel('Время выполнения (мкс)', fontsize=12)
plt.title('Сравнение времени работы стандартного Merge Sort\nна разных типах данных', fontsize=14, fontweight='bold')
plt.grid(True, alpha=0.3)
plt.legend(fontsize=11)
plt.tight_layout()
plt.savefig('standard_comparison.png', dpi=300)
plt.close()

# 2. Графики для гибридного алгоритма (с оптимальными пороговыми значениями)

# Находим оптимальные пороговые значения для каждого типа данных
optimal_thresholds = {}
for data_type in ['random', 'reversed', 'almost_sorted']:
    type_data = hybrid_df[hybrid_df['type'] == data_type]
    # Для каждого размера находим оптимальный threshold
    optimal_times = []
    sizes = sorted(type_data['size'].unique())
    for size in sizes:
        size_data = type_data[type_data['size'] == size]
        # Находим минимальное время для этого размера
        min_time_row = size_data.loc[size_data['time'].idxmin()]
        optimal_times.append(min_time_row['time'])
    optimal_thresholds[data_type] = optimal_times

# График 5: Случайные данные для гибридного алгоритма
plt.figure(figsize=(10, 6))
plt.plot(sizes, optimal_thresholds['random'], 'b-', linewidth=2.5, label='Случайные данные')
plt.xlabel('Размер массива (N)', fontsize=12)
plt.ylabel('Время выполнения (мкс)', fontsize=12)
plt.title('Время работы гибридного сортировщика\nна случайных данных', fontsize=14, fontweight='bold')
plt.grid(True, alpha=0.3)
plt.legend(fontsize=11)
plt.tight_layout()
plt.savefig('hybrid_random.png', dpi=300)
plt.close()

# График 6: Обратно отсортированные данные для гибридного алгоритма
plt.figure(figsize=(10, 6))
plt.plot(sizes, optimal_thresholds['reversed'], 'r-', linewidth=2.5, label='Обратно отсортированные данные')
plt.xlabel('Размер массива (N)', fontsize=12)
plt.ylabel('Время выполнения (мкс)', fontsize=12)
plt.title('Время работы гибридного сортировщика\nна обратно отсортированных данных', fontsize=14, fontweight='bold')
plt.grid(True, alpha=0.3)
plt.legend(fontsize=11)
plt.tight_layout()
plt.savefig('hybrid_reversed.png', dpi=300)
plt.close()

# График 7: Почти отсортированные данные для гибридного алгоритма
plt.figure(figsize=(10, 6))
plt.plot(sizes, optimal_thresholds['almost_sorted'], 'g-', linewidth=2.5, label='Почти отсортированные данные')
plt.xlabel('Размер массива (N)', fontsize=12)
plt.ylabel('Время выполнения (мкс)', fontsize=12)
plt.title('Время работы гибридного сортировщика\nна почти отсортированных данных', fontsize=14, fontweight='bold')
plt.grid(True, alpha=0.3)
plt.legend(fontsize=11)
plt.tight_layout()
plt.savefig('hybrid_almost_sorted.png', dpi=300)
plt.close()

# График 8: Общий график для гибридного алгоритма
plt.figure(figsize=(10, 6))
plt.plot(sizes, optimal_thresholds['random'], 'b-', linewidth=2.5, label='Случайные данные')
plt.plot(sizes, optimal_thresholds['reversed'], 'r-', linewidth=2.5, label='Обратно отсортированные')
plt.plot(sizes, optimal_thresholds['almost_sorted'], 'g-', linewidth=2.5, label='Почти отсортированные')
plt.xlabel('Размер массива (N)', fontsize=12)
plt.ylabel('Время выполнения (мкс)', fontsize=12)
plt.title('Сравнение времени работы гибридного сортировщика\nна разных типах данных', fontsize=14, fontweight='bold')
plt.grid(True, alpha=0.3)
plt.legend(fontsize=11)
plt.tight_layout()
plt.savefig('hybrid_comparison.png', dpi=300)
plt.close()

# Вывод информации о завершении
print("Все 8 графиков успешно созданы и сохранены в директорию ../SET3/A2/plots/")
print("\nСписок созданных графиков:")
print("1. standard_random.png - Стандартный Merge Sort на случайных данных")
print("2. standard_reversed.png - Стандартный Merge Sort на обратно отсортированных данных")
print("3. standard_almost_sorted.png - Стандартный Merge Sort на почти отсортированных данных")
print("4. standard_comparison.png - Сравнение стандартного Merge Sort на всех типах данных")
print("5. hybrid_random.png - Гибридный сортировщик на случайных данных")
print("6. hybrid_reversed.png - Гибридный сортировщик на обратно отсортированных данных")
print("7. hybrid_almost_sorted.png - Гибридный сортировщик на почти отсортированных данных")
print("8. hybrid_comparison.png - Сравнение гибридного сортировщика на всех типах данных")

# Дополнительный анализ для выводов
print("\nАнализ оптимальных пороговых значений для гибридного алгоритма:")
for data_type in ['random', 'reversed', 'almost_sorted']:
    type_data = hybrid_df[hybrid_df['type'] == data_type]
    best_thresholds = []
    for size in sorted(type_data['size'].unique()):
        size_data = type_data[type_data['size'] == size]
        best_threshold = size_data.loc[size_data['time'].idxmin()]['threshold']
        best_thresholds.append(best_threshold)

    avg_threshold = np.mean(best_thresholds[-10:])  # Среднее для больших размеров
    print(f"{data_type.replace('_', ' ')}: оптимальный порог ≈ {avg_threshold:.0f} элементов")