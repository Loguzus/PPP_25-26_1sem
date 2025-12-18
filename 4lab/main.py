import sys
import json
import abc
class ExchangeRegistry:
    base_currency = "RUB"
    rates = {}

    @classmethod
    def set_base(cls, currency):
        cls.base_currency = currency.strip().upper()
        cls.rates[cls.base_currency] = 1.0 

    @classmethod
    def add_rate(cls, currency, rate):
        cls.rates[currency.strip().upper()] = float(rate)

    @classmethod
    def to_base(cls, amount, currency):
        curr = currency.strip().upper()
        if curr not in cls.rates:
            raise ValueError(f"Неизвестная валюта: {curr}")
        return amount * cls.rates[curr]
class Money(abc.ABC):
    def __init__(self, raw_line):
        self.raw_line = raw_line
        self.amount = 0.0
        self.currency = ExchangeRegistry.base_currency
        self.is_valid = False
        self.error_msg = ""
        
        try:
            self._parse()
            if self.currency not in ExchangeRegistry.rates:
                raise ValueError(f"Нет курса для валюты {self.currency}")
            self.is_valid = True
        except Exception as e:
            self.error_msg = str(e)

    @abc.abstractmethod
    def _parse(self):
        pass

    @property
    def value_in_base(self):
        return ExchangeRegistry.to_base(self.amount, self.currency)
    def __lt__(self, other):
        return self.value_in_base < other.value_in_base

    def __eq__(self, other):
        return self.value_in_base == other.value_in_base

    def __str__(self):
        if not self.is_valid:
            return f"Error: {self.raw_line} ({self.error_msg})"
        base_val = self.value_in_base
        base_curr = ExchangeRegistry.base_currency
        if self.currency == base_curr:
            return f"{self.amount:.2f} {self.currency}"
        
        return f"{self.amount:.2f} {self.currency} = {base_val:.2f} {base_curr}"

class CodeMoney(Money):
    def _parse(self):
        parts = self.raw_line.split()
        self.amount = float(parts[1])
        self.currency = parts[2].upper()

class JsonMoney(Money):
    def _parse(self):
        json_str = self.raw_line[5:] 
        data = json.loads(json_str)
        self.amount = float(data["amount"])
        self.currency = data["currency"].upper()

class LocalMoney(Money):
    SYMBOLS = {'₽': 'RUB', '$': 'USD', '€': 'EUR', '¥': 'CNY'}
    
    def _parse(self):
        content = self.raw_line[6:].strip()
        found_symbol = None
        for sym, code in self.SYMBOLS.items():
            if sym in content:
                found_symbol = sym
                self.currency = code
                break
        
        if not found_symbol:
            raise ValueError("Не найден символ валюты (₽, $, €...)")
        num_str = content.replace(found_symbol, "").replace(" ", "").replace(",", ".")
        self.amount = float(num_str)

class DefaultMoney(Money):
    def _parse(self):
        parts = self.raw_line.split()
        self.amount = float(parts[1])
        self.currency = ExchangeRegistry.base_currency
def create_money_object(line):
    line = line.strip()
    if line.startswith("code"):
        return CodeMoney(line)
    elif line.startswith("json"):
        return JsonMoney(line)
    elif line.startswith("local"):
        return LocalMoney(line)
    elif line.startswith("default"):
        return DefaultMoney(line)
    else:
        m = DefaultMoney(line) 
        m.is_valid = False
        m.error_msg = "Неизвестный формат строки"
        return m

def main():
    print("--- Ввод данных (введите пустую строку, чтобы перейти к следующему этапу) ---")
    print("Введите базовую валюту (например: base RUB):")
    try:
        base_line = input().strip()
        if " " in base_line:
            base_curr = base_line.split()[-1]
        else:
            base_curr = base_line
        ExchangeRegistry.set_base(base_curr)
    except EOFError:
        return

    print(f"Введите курсы (например USD 92.5). Пустая строка для завершения ввода курсов.")
    while True:
        try:
            line = input().strip()
            if not line: break
            parts = line.split()
            if len(parts) == 2:
                ExchangeRegistry.add_rate(parts[0], parts[1])
        except EOFError:
            break
    print("Введите суммы в разных форматах(например: code 10 USD; local 1000,50$; default 500). Введите 'cmd' или пустую строку для перехода к команде.")
    money_collection = []
    
    while True:
        try:
            line = input().strip()
            if not line or line == "cmd": break
            if line in ['sum', 'max', 'min', 'list']:
                command = line
                break 
            
            obj = create_money_object(line)
            if obj.is_valid:
                money_collection.append(obj)
            else:
                print(f"Ошибка в строке: {line} -> {obj.error_msg}")
                
        except EOFError:
            break
    if 'command' not in locals():
        print("Введите команду (sum, max, min, list):")
        try:
            command = input().strip()
        except EOFError:
            return

    if not money_collection:
        print("Нет корректных данных для обработки.")
        return
    if command == 'sum':
        total = sum(m.value_in_base for m in money_collection)
        print(f"Total: {total:.2f} {ExchangeRegistry.base_currency}")
    
    elif command == 'max':
        max_obj = max(money_collection)
        print(f"Max: {max_obj}")
        
    elif command == 'min':
        min_obj = min(money_collection)
        print(f"Min: {min_obj}")
        
    elif command == 'list':
        for m in money_collection:
            print(f"- {m}")
    
    else:
        print("Неизвестная команда")

if __name__ == "__main__":
    main()
