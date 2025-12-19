import re
import sys

class RecursiveParser:
    def init(self):
        self.log = []
        self.tokens = []

    def evaluate(self, expression):
        self.log = []
        expression = expression.replace(" ", "")
        self.tokens = re.findall(r'\d+(?:\.\d+)?|[+\-*/()]', expression)
        
        if not self.tokens:
            return None, ["Пустое выражение"]
        try:
            result, _ = self.parse_expression(0)
            return result, self.log
        except IndexError:
            return "Ошибка", ["Некорректное выражение (возможно, не хватает цифр или скобок)"]
        except ZeroDivisionError:
             return "Ошибка", ["Деление на ноль"]

    def parse_expression(self, index):
        self.log_step("Начало разбора выражения (сумма/разность)", index)
        
        left_val, index = self.parse_term(index)
        
        while index < len(self.tokens) and self.tokens[index] in ('+', '-'):
            op = self.tokens[index]
            right_val, index = self.parse_term(index + 1)
            
            old_val = left_val
            if op == '+': left_val += right_val
            else: left_val -= right_val
            
            self.log_step(f"Вычислено: {old_val} {op} {right_val} = {left_val}", index)
            
        return left_val, index

    def parse_term(self, index):
        left_val, index = self.parse_factor(index)
        
        while index < len(self.tokens) and self.tokens[index] in ('*', '/'):
            op = self.tokens[index]
            right_val, index = self.parse_factor(index + 1)
            
            old_val = left_val
            if op == '*': left_val *= right_val
            else: left_val /= right_val
            
            self.log_step(f"Вычислено: {old_val} {op} {right_val} = {left_val}", index)
            
        return left_val, index

    def parse_factor(self, index):
        if index >= len(self.tokens):
             raise IndexError
             
        token = self.tokens[index]
        
        if token == '(':
            self.log_step("Обнаружена скобка, углубляемся в рекурсию", index)
            val, index = self.parse_expression(index + 1)
            return val, index + 1
        elif token == ')':
            return 0, index
        else:
            val = float(token)
            return val, index + 1

    def log_step(self, message, index):
        remaining = "".join(self.tokens[index:]) if index < len(self.tokens) else "end"
        self.log.append(f"[{remaining:<10}] -> {message}")
def main():
    parser = RecursiveParser()
    print("=== Рекурсивный калькулятор ===")
    print("Введите арифметическое выражение (например: 2 + 2 * (3 - 1))")
    print("Для выхода введите 'exit'")
    print("===============================")

    while True:
        user_input = input("\nВведите выражение: ")
        
        if user_input.lower() in ['exit', 'quit', 'выход']:
            print("Программа завершена.")
            break
            
        if not user_input.strip():
            continue

        result, history = parser.evaluate(user_input)

        print("-" * 40)
        print(f"Результат: {result}")
        print("-" * 40)
        print("Журнал вычислений:")
        for step in history:
            print(step)

if __name__ == "__main__":
    main()
