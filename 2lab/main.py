def converter():
    print("Введите курсы валют (формат: 'валюта1 валюта2 курс(Дробные числа через точку!!)', пустая строка для завершения):")
    rates = {}
    
    while True:
        kyrs_str = input().strip()
        if not kyrs_str:  
            break
            
        parts = kyrs_str.split()
        if len(parts) != 3:
            print(f"Неверный формат. Используйте: 'валюта1 валюта2 курс'")
            continue
            
        from_kyrs, to_kyrs, kyrs = parts[0], parts[1], parts[2]
        
        try:
            rate_value = float(kyrs)
        except ValueError:
            print(f"Курс должен быть числом.")
            continue
            
        if from_kyrs not in rates:
            rates[from_kyrs] = {}
        rates[from_kyrs][to_kyrs] = rate_value
        print(f"Добавленный курс: 1 {from_kyrs} = {rate_value} {to_kyrs}")

        if rate_value != 0:
            inverse_rate = 1 / rate_value
            if to_kyrs not in rates:
                rates[to_kyrs] = {}
            rates[to_kyrs][from_kyrs] = inverse_rate
            print(f"Обратный курс: 1 {to_kyrs} = {inverse_rate} {from_kyrs}")
        else:
            print(f"Не удалось добавить обратный курс для {from_kyrs} -> {to_kyrs}, так как курс равен 0.")
    
    if not rates:
        print("Не введено ни одного курса валют.")
        return

    print("\nВведите запрос конверсии (формат: 'сумма валюта1 валюта2 ...'):")
    conversion_input = input().strip()
    
    input_parts = conversion_input.split()
    if len(input_parts) < 3:
        print("Неверный формат запроса. Нужно: сумма и минимум 2 валюты.")
        return
    
    try:
        amount = float(input_parts[0])
    except ValueError:
        print("Сумма должна быть числом.")
        return
    
    conversion_path = input_parts[1:]

    for i in range(len(conversion_path) - 1):
        from_kyrs = conversion_path[i]
        to_kyrs = conversion_path[i + 1]
        if from_kyrs not in rates or to_kyrs not in rates[from_kyrs]:
            print(f"Невозможно конвертировать из '{from_kyrs}' в '{to_kyrs}'")
            print(f"Доступные конверсии из {from_kyrs}: {list(rates.get(from_kyrs, {}).keys())}")
            return
            
    current_amount = amount
    steps = [f"{current_amount} {conversion_path[0]}"]
    
    for i in range(len(conversion_path) - 1):
        from_kyrs = conversion_path[i]
        to_kyrs = conversion_path[i + 1]
        current_amount *= rates[from_kyrs][to_kyrs]
        current_amount = round(current_amount, 6)
        steps.append(f"{current_amount} {to_kyrs}")

    print("\nРезультат конверсии:")
    print(" -> ".join(steps))

print("=== КОНВЕРТЕР ВАЛЮТ ===")
converter()
