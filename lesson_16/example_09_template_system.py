from trie import Trie
from utils.trie_visualizer import visualize_trie
import re
from collections import defaultdict
import random


class TemplateSystem(Trie):
    def __init__(self):
        super().__init__()
        self.usage_stats = defaultdict(int)
        self.template_patterns = {}

    def add_template(self, keywords, template, description=None, priority=1):
        """
        Додає шаблон відповіді з ключовими словами

        keywords: список ключових слів для пошуку
        template: шаблон з параметрами {ім'я}, {проблема}, {рішення}
        description: опис шаблону
        priority: пріоритет шаблону (чим вище, тим важливіший)
        """
        if not isinstance(keywords, list) or not keywords:
            raise TypeError("keywords must be a non-empty list")
        if not isinstance(template, str) or not template:
            raise TypeError("template must be a non-empty string")

        # Генеруємо унікальний ключ для шаблону
        template_key = f"template_{self.size + 1}"

        template_info = {
            "keywords": [kw.lower().strip() for kw in keywords],
            "template": template,
            "description": description or f"Шаблон для: {', '.join(keywords)}",
            "priority": priority,
            "usage_count": 0,
            "parameters": self._extract_parameters(template),
            "key": template_key,
        }

        # Зберігаємо шаблон
        self.put(template_key, template_info)

        # Додаємо ключові слова до trie для швидкого пошуку
        for keyword in template_info["keywords"]:
            keyword_key = f"kw_{keyword}"
            existing = self.get(keyword_key)
            if existing:
                existing["templates"].append(template_key)
            else:
                self.put(keyword_key, {"type": "keyword", "templates": [template_key]})

        # Зберігаємо інформацію про шаблон
        self.template_patterns[template_key] = template_info

        print(
            f"✅ Додано шаблон '{template_key}' для ключових слів: {', '.join(keywords)}"
        )
        return template_key

    def _extract_parameters(self, template):
        """Витягує імена параметрів з шаблону"""
        pattern = r"\{([^}]+)\}"
        return re.findall(pattern, template)

    def find_relevant_templates(self, query, max_results=5):
        """
        Знаходить релевантні шаблони за запитом користувача
        """
        if not isinstance(query, str) or not query:
            raise TypeError("query must be a non-empty string")

        query_words = query.lower().split()
        template_scores = {}

        # Пошук шаблонів за ключовими словами
        for word in query_words:
            keyword_key = f"kw_{word}"
            keyword_info = self.get(keyword_key)
            if keyword_info and keyword_info["type"] == "keyword":
                for template_key in keyword_info["templates"]:
                    template_info = self.get(template_key)
                    if template_info:
                        # Рахуємо релевантність
                        keyword_matches = len(
                            set(query_words) & set(template_info["keywords"])
                        )
                        score = keyword_matches * template_info["priority"]

                        if template_key in template_scores:
                            template_scores[template_key] += score
                        else:
                            template_scores[template_key] = score

        # Сортуємо за релевантністю
        sorted_templates = sorted(
            template_scores.items(), key=lambda x: x[1], reverse=True
        )

        results = []
        for template_key, score in sorted_templates[:max_results]:
            template_info = self.get(template_key)
            if template_info:
                results.append(
                    {
                        "key": template_key,
                        "template": template_info["template"],
                        "description": template_info["description"],
                        "score": score,
                        "parameters": template_info["parameters"],
                        "keywords": template_info["keywords"],
                    }
                )

        return results

    def fill_template(self, template_key, parameters):
        """
        Заповнює шаблон параметрами
        """
        template_info = self.get(template_key)
        if not template_info:
            raise ValueError(f"Template '{template_key}' not found")

        template = template_info["template"]

        # Замінюємо параметри в шаблоні
        for param_name, param_value in parameters.items():
            template = template.replace(f"{{{param_name}}}", str(param_value))

        # Перевіряємо чи всі параметри замінені
        missing_params = self._extract_parameters(template)
        if missing_params:
            print(f"⚠️  Попередження: не всі параметри заповнені: {missing_params}")

        # Оновлюємо статистику використання
        template_info["usage_count"] += 1
        self.usage_stats[template_key] += 1

        return template

    def get_template_stats(self):
        """Повертає статистику використання шаблонів"""
        stats = []
        all_keys = self.keys()

        for key in all_keys:
            if key.startswith("template_"):
                info = self.get(key)
                if info:
                    stats.append(
                        {
                            "key": key,
                            "description": info["description"],
                            "usage_count": info["usage_count"],
                            "keywords": info["keywords"],
                            "priority": info["priority"],
                        }
                    )

        return sorted(stats, key=lambda x: x["usage_count"], reverse=True)

    def search_in_templates(self, keyword):
        """
        Пошук ключового слова у всіх шаблонах
        """
        if not isinstance(keyword, str) or not keyword:
            raise TypeError("keyword must be a non-empty string")

        keyword = keyword.lower()
        results = []
        all_keys = self.keys()

        for key in all_keys:
            if key.startswith("template_"):
                info = self.get(key)
                if info:
                    # Пошук в ключових словах
                    if keyword in " ".join(info["keywords"]).lower():
                        results.append(
                            {
                                "key": key,
                                "type": "keyword_match",
                                "description": info["description"],
                                "keywords": info["keywords"],
                            }
                        )
                    # Пошук в описі
                    elif keyword in info["description"].lower():
                        results.append(
                            {
                                "key": key,
                                "type": "description_match",
                                "description": info["description"],
                                "keywords": info["keywords"],
                            }
                        )
                    # Пошук в шаблоні
                    elif keyword in info["template"].lower():
                        results.append(
                            {
                                "key": key,
                                "type": "template_match",
                                "description": info["description"],
                                "keywords": info["keywords"],
                            }
                        )

        return results

    def get_suggestions_for_query(self, query):
        """
        Пропонує параметри для запиту на основі шаблонів
        """
        relevant_templates = self.find_relevant_templates(query, max_results=3)
        suggestions = []

        for template_info in relevant_templates:
            template_key = template_info["key"]
            template_data = self.get(template_key)
            if template_data:
                # Аналізуємо запит для вилучення можливих значень параметрів
                extracted_params = {}
                query_lower = query.lower()

                # Простий екстрактор імен
                if (
                    "ім'я" in template_data["parameters"]
                    or "name" in template_data["parameters"]
                ):
                    # Шукаємо імена в запиті (простий приклад)
                    words = query.split()
                    for word in words:
                        if word[0].isupper() and len(word) > 2:
                            extracted_params["ім'я"] = word
                            break

                suggestions.append(
                    {
                        "template_key": template_key,
                        "template": template_data["template"],
                        "extracted_parameters": extracted_params,
                        "confidence": template_info["score"],
                    }
                )

        return suggestions

    def generate_smart_response(self, query, context=None):
        """
        Генерує розумну відповідь на основі запиту та контексту
        """
        suggestions = self.get_suggestions_for_query(query)

        if not suggestions:
            return "На жаль, я не знайшов відповідний шаблон для вашого запиту."

        # Вибираємо найкращий варіант
        best_suggestion = suggestions[0]
        template_key = best_suggestion["template_key"]

        # Заповнюємо параметри
        parameters = best_suggestion.get("extracted_parameters", {})

        # Додаємо контекст якщо є
        if context:
            for key, value in context.items():
                if key in parameters:
                    parameters[key] = value

        # Якщо параметрів не вистачає, використовуємо загальні значення
        template_data = self.get(template_key)
        if template_data:
            for param in template_data["parameters"]:
                if param not in parameters:
                    if param.lower() in ["ім'я", "name"]:
                        parameters[param] = "користувачу"
                    elif param.lower() in ["проблема", "problem"]:
                        parameters[param] = "вашої проблеми"
                    elif param.lower() in ["рішення", "solution"]:
                        parameters[param] = "найближчим часом"
                    else:
                        parameters[param] = "недоступно"

        return self.fill_template(template_key, parameters)


if __name__ == "__main__":
    print("🤖 Система швидких відповідей та шаблонів\n")

    template_system = TemplateSystem()

    # Додаємо шаблони для різних сценаріїв
    templates_to_add = [
        # Підтримка користувачів
        (
            ["помилка", "логін", "доступ", "не можу увійти"],
            "Добрий день, {ім'я}! Ми розуміємо вашу проблему з {проблема}. Наша команда вже працює над {рішення}.",
            "Проблеми з доступом до системи",
            3,
        ),
        (
            ["повернення", "товар", "гроші", "refund"],
            "Шановний {ім'я}, ваше повернення товару '{товар}' по причині '{причина}' оброблено. Рішення: {рішення}.",
            "Обробка повернень товарів",
            3,
        ),
        (
            ["доставка", "замовлення", "терміни", "коли"],
            "Вітаємо, {ім'я}! Ваше замовлення #{номер} буде доставлено {терміни}. Статус: {статус}.",
            "Інформація про доставку",
            2,
        ),
        (
            [" оплата", "картка", "не працює", "помилка"],
            "{ім'я}, виникла проблема з оплатою карткою {тип_картки}. Будь ласка, спробуйте {альтернатива} або зв'яжіться з банком.",
            "Проблеми з оплатою",
            3,
        ),
        # Технічна підтримка
        (
            ["пароль", "забув", "скинути", "відновити"],
            "Для відновлення пароля для акаунту {email}, перейдіть за посиланням {посилання}. Посилання діє {час_дії}.",
            "Відновлення пароля",
            2,
        ),
        (
            ["сервер", "не працює", "падає", "помилка"],
            "Ми знаємо про проблему з сервером {сервер}. Наші інженери працюють над {рішення}. Очікуваний час відновлення: {час}.",
            "Проблеми з серверами",
            4,
        ),
        # Загальні відповіді
        (
            ["дякую", "спасибі", "допомога"],
            "Завжди раді допомогти, {ім'я}! Якщо у вас виникнуть ще питання, звертайтеся.",
            "Подяка користувача",
            1,
        ),
        (
            ["привіт", "добрий день", "hello"],
            "Доброго дня, {ім'я}! Чим можу допомогти сьогодні?",
            "Привітання",
            1,
        ),
    ]

    for keywords, template, description, priority in templates_to_add:
        template_system.add_template(keywords, template, description, priority)

    print(f"\n📊 Всього шаблонів у системі: {template_system.size}")

    # Приклад 1: Пошук релевантних шаблонів
    print("\n🔍 Пошук шаблонів для запиту 'не можу увійти в систему':")
    relevant = template_system.find_relevant_templates("не можу увійти в систему")
    if relevant:
        for i, tmpl in enumerate(relevant, 1):
            print(f"  {i}. {tmpl['description']} (рейтинг: {tmpl['score']})")
            print(f"     Шаблон: {tmpl['template']}")
            print(f"     Ключові слова: {', '.join(tmpl['keywords'])}")
            print()
    else:
        print("  Не знайдено релевантних шаблонів")

    # Приклад 2: Заповнення шаблону
    print("\n✏️  Заповнення шаблону параметрами:")
    if relevant:
        template_key = relevant[0]["key"]
        filled = template_system.fill_template(
            template_key,
            {
                "ім'я": "Іван",
                "проблема": "входом в особистий кабінет",
                "рішення": "відновленням доступу",
            },
        )
        print(f"Результат: {filled}")
    else:
        print("  Немає шаблонів для заповнення")

    # Приклад 3: Інтелектуальна відповідь
    print("\n🤖 Генерація розумної відповіді:")
    queries = [
        "Привіт, мені звати Марія",
        "не можу оплатити карткою",
        "коли буде доставка замовлення 12345?",
        "дякую за допомогу",
    ]

    for query in queries:
        print(f"\nЗапит: '{query}'")
        response = template_system.generate_smart_response(query, {"ім'я": "Марія"})
        print(f"Відповідь: {response}")

    # Приклад 4: Пошук в шаблонах
    print("\n🔎 Пошук слова 'доставка' у всіх шаблонах:")
    search_results = template_system.search_in_templates("доставка")
    for result in search_results:
        print(f"  • {result['description']} (тип: {result['type']})")

    # Приклад 5: Статистика використання
    print("\n📈 Статистика використання шаблонів:")
    stats = template_system.get_template_stats()
    for i, stat in enumerate(stats[:5], 1):
        print(f"  {i}. {stat['description']}: {stat['usage_count']} використань")

    # Приклад 6: Пропозиції параметрів
    print("\n💡 Пропозиції для запиту 'Проблема з доступом для Петра':")
    suggestions = template_system.get_suggestions_for_query(
        "Проблема з доступом для Петра"
    )
    for suggestion in suggestions:
        print(f"  Шаблон: {suggestion['template']}")
        print(f"  Витягнуті параметри: {suggestion['extracted_parameters']}")
        print(f"  Впевненість: {suggestion['confidence']}")
        print()

    # Візуалізація trie
    print("\n🎨 Візуалізація структури trie:")
    # visualize_trie(template_system)
