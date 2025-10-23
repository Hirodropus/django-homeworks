from django.shortcuts import render

DATA = {
    'omlet': {
        'яйца, шт': 2,
        'молоко, л': 0.1,
        'соль, ч.л.': 0.5,
    },
    'pasta': {
        'макароны, г': 0.3,
        'сыр, г': 0.05,
    },
    'buter': {
        'хлеб, ломтик': 1,
        'колбаса, ломтик': 1,
        'сыр, ломтик': 1,
        'помидор, ломтик': 1,
    },
}


def get_recipe(request, dish_name):
    """
    Обработчик для отображения рецепта блюда
    """
    # Получаем рецепт из DATA по названию блюда
    recipe = DATA.get(dish_name)

    if recipe:
        # Создаем копию рецепта для корректировки количеств
        adjusted_recipe = recipe.copy()

        # Проверяем параметр servings из GET-запроса
        servings_param = request.GET.get('servings')

        if servings_param:
            try:
                # Конвертируем в число и проверяем, что оно положительное
                servings = int(servings_param)
                if servings > 0:
                    # Умножаем количество каждого ингредиента на servings
                    for ingredient in adjusted_recipe:
                        adjusted_recipe[ingredient] *= servings
            except (ValueError, TypeError):
                # Если servings не число, используем исходный рецепт
                pass

        context = {
            'recipe': adjusted_recipe
        }
    else:
        # Если рецепт не найден, передаем пустой словарь
        context = {
            'recipe': {}
        }

    return render(request, 'calculator/index.html', context)