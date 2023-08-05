from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    message: str = ('Тип тренировки: {training_type}; '
                    'Длительность: {duration:.3f} ч.; '
                    'Дистанция: {distance:.3f} км; '
                    'Ср. скорость: {speed:.3f} км/ч; '
                    'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        """Выводим информацию о тренировке."""
        return self.message.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65  # Путь за 1 шаг (метр).
    M_IN_KM: int = 1000  # Метров в 1 км.
    MIN_IN_H = 60        # Минут в 1 часе.

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight_kg = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        # NotImplementedError: Определите get_spent_calories
        # в Running, SportsWalking, Swimming.
        raise NotImplementedError(
            'Определите get_spent_calories в %s.' % (self.__class__.__name__))

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return (InfoMessage(self.__class__.__name__,
                self.duration,
                self.get_distance(),
                self.get_mean_speed(),
                self.get_spent_calories()))


class Running(Training):
    """Тренировка: бег."""
    COEFF_1 = 18  # Константа калорий - 18.
    COEFF_2 = 1.79  # Константа калорий - 1.79.

    def get_spent_calories(self) -> float:
        """Количество калорий во время бега."""
        return ((self.COEFF_1 * self.get_mean_speed() + self.COEFF_2)
                * self.weight_kg / self.M_IN_KM
                * (self.duration * self.MIN_IN_H))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    COEFF_3 = 0.035  # Константа калорий - 0.035.
    COEFF_4 = 0.029  # Константа калорий - 0.029.
    M_IN_SEC = 0.278  # Перевод км/ч в м/с.
    H_MET = 100       # Перевод из м. в см.

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height_cm = height

    def get_spent_calories(self) -> float:
        """Количество калорий во время ходьбы."""
        self.speed_ms = self.get_mean_speed() * self.M_IN_SEC
        self.height_cm = self.height_cm / self.H_MET
        self.time_in_min = self.duration * self.MIN_IN_H
        return ((self.COEFF_3 * self.weight_kg + (self.speed_ms ** 2
                / self.height_cm) * self.COEFF_4 * self.weight_kg)
                * self.time_in_min)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38  # Путь за 1 гребок (метр).
    COEFF_5 = 1.1  # Константа калорий - 1.1.
    COEFF_6 = 2  # Константа калорий - 2.

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Средняя скорость во время плавания."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Количество калорий во время плавания."""
        return ((self.get_mean_speed() + self.COEFF_5) * self.COEFF_6
                * self.weight_kg * self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_data: dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }

    if workout_type not in training_data:
        raise ValueError('Введён неверный идентификатор тренировки.')
    return training_data[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages: list[tuple[str, list[int]]] = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
