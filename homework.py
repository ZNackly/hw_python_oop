from dataclasses import dataclass, asdict
from typing import Dict, Type, ClassVar


@dataclass
class InfoMessage:
    """
    Класс для создания объектов сообщений.
    Информационное сообщение о тренировке.
    """

    training_type: str  # Название тренировки
    duration: float     # Длительность (в часах)
    distance: float     # Дистанция в (в км)
    speed: float        # Скорость (в км/ч)
    calories: float     # Килокалории
    message: str = ('Тип тренировки: {training_type}; '
                    'Длительность: {duration:.3f} ч.; '
                    'Дистанция: {distance:.3f} км; '
                    'Ср. скорость: {speed:.3f} км/ч; '
                    'Потрачено ккал: {calories:.3f}.')

    # числовые значения округляются при выводе до тысячных долей с помощью
    # format specifier (.3f)
    def get_message(self) -> str:
        """Метод возвращает строку сообщения"""
        return self.message.format(**asdict(self))


@dataclass
class Training:
    # Каждый класс, описывающий определённый вид тренировки, будет
    # дополнять и расширять этот базовый класс.
    """
    Базовый класс тренировки.
    Содержит все основные свойства и методы для тренировок.

    Входные переменные:
    - action - количество совершённых действий
    - duration - длительность тренировки
    - weight - вес спортсмена
    """

    # расстояние, которое спортсмен преодолевает
    LEN_STEP: ClassVar[float] = 0.65
    # константа для перевода значений из метров в километры.
    M_IN_KM: ClassVar[float] = 1000
    # константа для перевода времени.
    TIME_CONST: ClassVar[float] = 60

    action: int         # Действие
    duration: float     # Продолжительность
    weight: float       # Вес

    def get_distance(self) -> float:
        """
        Возвращает дистанцию (в километрах), которую преодолел пользователь
        за время тренировки.
        """
        return self.action * self.LEN_STEP / self.M_IN_KM

    # возвращает значение средней скорости движения во время тренировки в км/ч
    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        # формула из задания
        # преодоленная_дистанция_за_тренировку / время_тренировки
        return self.get_distance() / self.duration

    # метод определяется в дочерних классах, расчет калорий отличается
    # в зависимости от тренировки
    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError("Требуется определить get_spent_calories()")

    def show_training_info(self) -> InfoMessage:
        """
        Возвращает объект класса - информационное сообщение
        о выполненной тренировке.
        """
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories()
                           )


@dataclass
class Running(Training):
    """Тренировка: бег."""

    coeff_calorie_1: ClassVar[float] = 18
    coeff_calorie_2: ClassVar[float] = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.coeff_calorie_1 * self.get_mean_speed()
                - self.coeff_calorie_2) * self.weight
                / self.M_IN_KM * self.duration * self.TIME_CONST)


@dataclass
class SportsWalking(Training):
    """
    Тренировка: спортивная ходьба.
    Дополнительный параметр height — рост спортсмена
    """

    coeff_calorie_1: ClassVar[float] = 0.035
    coeff_calorie_2: ClassVar[float] = 0.029
    coeff_calorie_3: ClassVar[float] = 2

    action: int         # Действие
    duration: float     # Продолжительность
    weight: float       # Вес
    height: float       # Рост

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.coeff_calorie_1
                * self.weight
                + (self.get_mean_speed() ** self.coeff_calorie_3
                    // self.height)
                * self.coeff_calorie_2 * self.weight)
                * self.TIME_CONST * self.duration)


@dataclass
class Swimming(Training):
    """
    Тренировка: плавание.

    Дополнительные входные переменные:
    - length_pool — длина бассейна в метрах;
    - count_pool — сколько раз пользователь переплыл бассейн.

    Переопределённые переменные:
    - LEN_STEP - теперь один гребок

    Переопределёны методы:
    - get_spent_calories() - расчета калорий
    - get_mean_speed() - рассчитывает среднюю скорость
    """

    # расстояние, которое спортсмен преодолевает за один гребок 1.38 метра
    LEN_STEP: ClassVar[float] = 1.38
    coeff_calorie_1: ClassVar[float] = 1.1
    coeff_calorie_2: ClassVar[float] = 2

    action: int         # Действие
    duration: float     # Продолжительность
    weight: float       # Вес
    length_pool: float  # Длина
    count_pool: float   # Количество

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.get_mean_speed() + self.coeff_calorie_1)
                * self.coeff_calorie_2 * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """
    Прочитать данные полученные от датчиков.

    Входные параметры:
    - Словарь из двух параметров
        - Строка с кодом тренировки
        - Класс обработчик тренировки

    Возвращает:
    - Объект класса тренировки
    """
    workout: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }

    if workout_type not in workout:
        raise ValueError(f"Такой тренировки - {workout_type}, не найдено")
    return workout[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
