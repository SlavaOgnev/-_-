import threading


from abc import ABC, abstractmethod
from database import *
from tkinter import *
from tkinter import ttk, messagebox

window = Tk()
window.title("Крутая Пиццерия")
window.geometry("1080x720")
window.minsize(750, 400)


# реализуем код, использующий статистические методы
class Order:
    order = []
    prices = 0

    @staticmethod
    def clear():
        Order.order = []
        Order.prices = 0

    @staticmethod
    def show():
        frame_clear(window)
        set_order = set(Order.order)
        if len(set_order) > 0:
            for pizza in set_order:
                ttk.Label(text=f'{pizza}, {Order.order.count(pizza)} шт.').pack()
            ttk.Label(text=f'Всего {len(Order.order)} шт.\nСумма заказа: {Order.prices} руб.').pack()
        else:
            ttk.Label(text="Корзина пуста").pack()

    @staticmethod
    def add(pizza):
        Order.order.append(pizza.name)
        Order.prices += pizza.price


# родительсикй класс для всех пицц
class Pizza(ABC):
    @abstractmethod  # элемент абстракции в классе Pizza
    def __init__(self, name="default_name", price=0):
        self.__name = name
        self.__size = "default_size"
        self.__spicy = "default_spicy"
        self.__price = price
        self.testo_ready = False
        self.ingredients_ready = False
        self.baked = False
        self.cutted = False
        self.packed = False
        self.isready = False
        self.after1 = None
        self.after2 = None
        self.after3 = None
        self.after4 = None
        self.after5 = None
        self.after6 = None

    # геттеры и сеттеры для всех атрибутов пиццы (инкапсуляция)
    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, get_name):
        self.__name = get_name

    @property
    def size(self):
        return self.__size

    @size.setter
    def size(self, get_size):
        self.__size = get_size

    @property
    def spicy(self):
        return self.__spicy

    @spicy.setter
    def spicy(self, get_spicy):
        self.__spicy = get_spicy

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, get_price):
        if isinstance(get_price, int):
            self.__price = get_price

    # методы, описывающие приготовление пиццы
    def testo(self, view):
        if view.is_set():
            Label(text="Тесто замешивается...").pack()
        self.testo_ready = True

    def ingredients(self, view):
        if view.is_set():
            Label(text="Сбор ингредиентов...").pack()
        self.ingredients_ready = True

    def bake(self, view):
        if view.is_set():
            Label(text="Пицца запекается...").pack()
        self.baked = True

    def cut(self, view):
        if view.is_set():
            Label(text="Пицца нарезается...").pack()
        self.cutted = True

    def pack(self, view):
        if view.is_set():
            Label(text="Пицца упаковывается...").pack()
        self.packed = True

    def ready(self, view):
        if view.is_set():
            Label(text="Пицца готова!").pack()
        self.isready = True

    def make_pizza(self, view):
        self.after1 = window.after(1500, lambda: self.testo(view))
        self.after2 = window.after(3000, lambda: self.ingredients(view))
        self.after3 = window.after(5000, lambda: self.bake(view))
        self.after4 = window.after(6000, lambda: self.cut(view))
        self.after5 = window.after(7500, lambda: self.pack(view))
        self.after6 = window.after(8500, lambda: self.ready(view))

    def howmuchready(self):
        if self.testo_ready:
            Label(text="Тесто уже замешано").pack()
        if self.ingredients_ready:
            Label(text="Ингредиенты уже собраны").pack()
        if self.baked:
            Label(text="Пицца уже запечена").pack()
        if self.cutted:
            Label(text="Пицца уже нарезана").pack()
        if self.packed:
            Label(text="Пицца уже упакована").pack()
        if self.isready:
            Label(text="Пицца уже готова!").pack()

    def unready(self):
        self.testo_ready = False
        self.ingredients_ready = False
        self.baked = False
        self.cutted = False
        self.packed = False
        self.isready = False
        for i in [self.after1, self.after2, self.after3, self.after4, self.after5, self.after6]:
            window.after_cancel(i)


class PizzaMixin:
    # перегрузка базового оператора сложения
    def __add__(self, other):
        if self == other:
            return self
        if isinstance(self, Pizza):
            new_price = (self.price + other.price) // 2
            if self.name > other.name:
                name1 = self.name
                name2 = other.name
            else:
                name1 = other.name
                name2 = self.name
            new_name = f"Пицца из половинок {name1} + {name2}"
            return HalfPizza(new_name, new_price)
        else:
            raise Exception("Ошибка: складывать можно только пиццы :)")

    # перегрузка базового оператора умножения
    def __mul__(self, other):
        if self == other:
            return self
        if isinstance(self, Pizza):
            new_price = (self.price + other.price) // 2
            if self.name > other.name:
                name1 = self.name
                name2 = other.name
            else:
                name1 = other.name
                name2 = self.name
            new_name = f"Смешанная пицца {name1} + {name2}"
            return HalfPizza(new_name, new_price)
        else:
            raise Exception("Ошибка: складывать можно только пиццы :)")


# подклассы с видами пицц
class Pepperoni(Pizza, PizzaMixin):
    def __init__(self):
        super().__init__()
        self.name = "Пепперони"
        self.size = "30 см"
        self.spicy = "2/3"
        self.price = 600


class BBQ(Pizza, PizzaMixin):
    def __init__(self):
        super().__init__()
        self.name = "Барбекю"
        self.size = "25 см"
        self.spicy = "3/3"
        self.price = 800


class Seafood(Pizza, PizzaMixin):
    def __init__(self):
        super().__init__()
        self.name = "Дары моря"
        self.size = "40 см"
        self.spicy = "1/3"
        self.price = 1000


class HalfPizza(Pizza):
    def __init__(self, name="default_name", price=0):
        super().__init__(name, price)


def frame_clear(frame):
    for widget in frame.winfo_children():
        widget.destroy()


def pizzagui():
    curr_user_login = StringVar()

    def signin():
        def autorize():
            login = login_entry.get()
            if user_exists(login):
                user = get_user(login)
                password = password_entry.get()
                if password == user.password:
                    curr_user_login.set(login)
                    terminal = Terminal(get_user(curr_user_login.get()))
                    terminal.show()
                else:
                    messagebox.showerror("Ошибка", "Неверный пароль")
                    password_entry.delete(0, END)
            else:
                messagebox.showerror("Ошибка", "Неверный логин")
                login_entry.delete(0, END)
                password_entry.delete(0, END)

        frame_clear(window)
        login_entry = ttk.Entry(window)
        login_entry.grid(row=0, column=1)
        ttk.Label(window, text="Введите логин").grid(row=0, column=0)
        password_entry = ttk.Entry(window)
        password_entry.grid(row=1, column=1)
        ttk.Label(window, text="Введите пароль").grid(row=1, column=0)
        ttk.Button(text="Войти", command=autorize).grid(row=2, column=2)
        ttk.Button(text="Назад", command=reg_start).grid(row=3, column=2)

    def signup():
        def register_new_user():
            login = login_entry.get()
            if user_exists(login):
                messagebox.showerror("Ошибка", "Пользователь с таким логином уже существует")
                login_entry.delete(0, END)
                password_entry.delete(0, END)
            elif len(login) < 5:
                messagebox.showerror("Ошибка", "Минимальная длина логина - 5 символов")
                login_entry.delete(0, END)
                password_entry.delete(0, END)
            else:
                password = password_entry.get()
                if len(password) < 5:
                    messagebox.showerror("Ошибка", "Минимальная длина пароля - 5 символов")
                    password_entry.delete(0, END)
                else:
                    create_user(login, password)
                    curr_user_login.set(login)
                    terminal = Terminal(get_user(curr_user_login.get()))
                    terminal.show()

        frame_clear(window)
        login_entry = ttk.Entry(window)
        login_entry.grid(row=0, column=1)
        ttk.Label(window, text="Введите логин").grid(row=0, column=0)
        password_entry = ttk.Entry(window)
        password_entry.grid(row=1, column=1)
        ttk.Label(window, text="Введите пароль").grid(row=1, column=0)

        ttk.Button(text="Создать", command=register_new_user).grid(row=2, column=2)
        ttk.Button(text="Назад", command=reg_start).grid(row=3, column=2)

    def reg_start():
        frame_clear(window)

        regInfo = ttk.Label(window, text="Добро пожаловать!", font=("Arial", 36))
        regInfo.pack(anchor=N, pady=(30, 0))
        signInButton = ttk.Button(text="Войти", command=signin)
        signUpButton = ttk.Button(text="Зарегистрироваться", command=signup)
        signInButton.pack(fill=X, padx=300, pady=(50, 10), ipady=20)
        signUpButton.pack(fill=X, padx=300, pady=10, ipady=20)

        colors = ['#FF0000', '#00FF00', '#0000FF', '#FFFF00', '#FF00FF', '#00FFFF']
        color_index = 0
        def update_color():
            nonlocal color_index
            regInfo.configure(foreground=colors[color_index])
            color_index = (color_index + 1) % len(colors)
            window.after(500, update_color)
        threading.Thread(target=update_color).start()

    reg_start()

    return curr_user_login.get()


class Terminal:
    def __init__(self, current_user):
        self.status = StringVar(value="start")
        self.user = current_user
        self.available_pizzas = [Pepperoni(), BBQ(), Seafood()]  # отношение композиции

    def show(self):

        def add_to_cart(pizza, quantity):
            for _ in range(quantity.get()):
                Order.add(pizza)
            trmnl_order()

        def add_pizza(pizza):
            frame_clear(window)
            quantity = IntVar(value=1)
            ttk.Button(text="-",
                       command=lambda: quantity.set(quantity.get() - 1) if quantity.get() > 1 else None).pack()
            ttk.Button(text="+", command=lambda: quantity.set(quantity.get() + 1)).pack()
            quan_label = ttk.Label(textvariable=quantity)
            quan_label.pack()
            ttk.Button(text="Добавить", command=lambda: add_to_cart(pizza, quantity)).pack()
            ttk.Button(text="Назад", command=trmnl_order).pack()

        def add_sliced(mode):
            frame_clear(window)
            p1 = IntVar(value=0)
            p2 = IntVar(value=0)
            ttk.Label(
                text="Обратите внимание: цена рассчитывается как среднее арифметическое "
                     "цены двух выбранных пицц").pack()
            ttk.Label(text="Выберите первую половинку").pack()
            ttk.Radiobutton(text="Пепперони", variable=p1, value=1).pack()
            ttk.Radiobutton(text="Барбекю", variable=p1, value=2).pack()
            ttk.Radiobutton(text="Дары моря", variable=p1, value=3).pack()
            ttk.Label(text="Выберите первую половинку").pack()
            ttk.Radiobutton(text="Пепперони", variable=p2, value=1).pack()
            ttk.Radiobutton(text="Барбекю", variable=p2, value=2).pack()
            ttk.Radiobutton(text="Дары моря", variable=p2, value=3).pack()
            quantity = IntVar(value=1)
            ttk.Button(text="-",
                       command=lambda: quantity.set(quantity.get() - 1) if quantity.get() > 1 else None).pack()
            ttk.Button(text="+", command=lambda: quantity.set(quantity.get() + 1)).pack()
            quan_label = ttk.Label(textvariable=quantity)
            quan_label.pack()

            def create_mix():
                if mode == "half":
                    new_pizza = self.available_pizzas[p1.get() - 1] + self.available_pizzas[p2.get() - 1]
                else:
                    new_pizza = self.available_pizzas[p1.get() - 1] * self.available_pizzas[p2.get() - 1]
                add_to_cart(new_pizza, quantity)

            ttk.Button(text="Добавить",
                       command=lambda: create_mix() if (p1.get() != 0 and p2.get() != 0) else None).pack()
            ttk.Button(text="Назад", command=trmnl_order).pack()

        def trmnl_start():
            frame_clear(window)
            ttk.Button(text="Сделать заказ", command=trmnl_order).pack()
            ttk.Button(text="Посмотреть корзину", command=trmnl_showorder).pack()
            ttk.Button(text="Очистить корзину", command=trmnl_clearorder).pack()
            ttk.Button(text="Перейти к оплате", command=trmnl_payment).pack()
            ttk.Button(text="Посмотреть историю заказов", command=trmnl_showhistory).pack()
            ttk.Button(text="Выход", command=exit).pack()

        def trmnl_order():
            frame_clear(window)
            ttk.Label(text="Добавить инфу о пиццах").pack()
            ttk.Button(text="Пепперони", command=lambda: add_pizza(self.available_pizzas[0])).pack()
            ttk.Button(text="Барбекю", command=lambda: add_pizza(self.available_pizzas[1])).pack()
            ttk.Button(text="Дары моря", command=lambda: add_pizza(self.available_pizzas[2])).pack()
            ttk.Button(text="Пицца из половинок", command=lambda: add_sliced("half")).pack()
            ttk.Button(text="Смешанная пицца", command=lambda: add_sliced("mix")).pack()
            ttk.Button(text="Назад", command=trmnl_start).pack()

        def trmnl_showorder():
            order.show()
            ttk.Button(text="Назад", command=trmnl_start).pack()

        def trmnl_clearorder():
            frame_clear(window)
            if len(Order.order) > 0:
                order.clear()
                ttk.Label(text="Корзина очищена").pack()
                ttk.Button(text="Назад", command=trmnl_start).pack()
            else:
                ttk.Label(text="Корзина уже пустая").pack()
                ttk.Button(text="Назад", command=trmnl_start).pack()

        def trmnl_payment():
            frame_clear(window)

            def payment_process():
                def another_order():
                    making_view.clear()
                    self.available_pizzas[0].unready()
                    trmnl_start()

                def track_making():
                    frame_clear(window)
                    ttk.Button(text="Сделать ещё заказ", command=another_order).pack()
                    ttk.Button(text="Выйти", command=exit).pack()
                    self.available_pizzas[0].howmuchready()
                    making_view.set()

                frame_clear(window)
                ttk.Label(text="Происходит оплата...").pack()

                window.after(2000, lambda: frame_clear(window))

                window.after(2000, lambda: ttk.Label(text="Заказ оплачен!").pack())
                window.after(3000, lambda: frame_clear(window))
                create_order(Order.prices, self.user)
                order.clear()
                making_view = threading.Event()
                t = threading.Thread(target=self.available_pizzas[0].make_pizza, args=(making_view,))
                window.after(3000, lambda: t.start())
                window.after(3000,
                             lambda: ttk.Button(text="Проследить за приготовлением пиццы", command=track_making).pack())
                window.after(3000, lambda: ttk.Button(text="Сделать ещё заказ", command=another_order).pack())
                window.after(3000, lambda: ttk.Button(text="Выйти", command=exit).pack())

            if len(Order.order) == 0:
                ttk.Label(text="Корзина пуста").pack()
                ttk.Button(text="Назад", command=trmnl_start).pack()
            else:
                ttk.Label(text=f"В вашей корзине {len(Order.order)} товар(ов) на сумму {Order.prices} руб.").pack()
                ttk.Button(text="Оплатить заказ", command=payment_process).pack()
                ttk.Button(text="Назад", command=trmnl_start).pack()

        def trmnl_showhistory():
            frame_clear(window)
            if self.user.order_count > 0:
                Label(text="Список ваших заказов:").pack()
                i = 1
                for zakaz in order_history(self.user):
                    Label(
                        text=f"{i}. Номер заказа: {zakaz.id}, дата: {zakaz.date}, стоимость: {zakaz.price} руб.").pack()
                    i += 1
            else:
                Label(text="Вы ещё не делали заказов").pack()
            ttk.Button(text="Назад", command=trmnl_start).pack()

        trmnl_start()


order = Order()

pizzagui()

window.mainloop()
