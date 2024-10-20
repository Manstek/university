import os
from django.shortcuts import render
from .forms import LogicChainForm


def load_rules(filename):
    rules = []
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line:
                part_1, part_2 = line.split(" то ")
                condition_1 = part_1.replace("Если ", "").strip()
                condition_2 = part_2.strip()
                rule = (condition_1.split(' = ')[0],
                        condition_1.split(' = ')[1],
                        condition_2.split(' = ')[0],
                        condition_2.split(' = ')[1])
                rules.append(rule)
    return rules


def logical_chain(initial_condition, initial_value, rules):
    current_states = {initial_condition: initial_value}

    changes = True
    while changes:
        changes = False
        for rule in rules:
            obj_1, value_1, obj_2, value_2 = rule
            if obj_1 in current_states and current_states[obj_1] == value_1:
                if obj_2 not in current_states:
                    current_states[obj_2] = value_2
                    changes = True
    if len(current_states) == 1:
        return False
    return current_states


def home(request):
    result = {}
    error = False
    if request.method == 'POST':
        form = LogicChainForm(request.POST)
        if form.is_valid():
            initial_condition = form.cleaned_data['initial_condition']
            initial_value = form.cleaned_data['initial_value']
            rules = load_rules(
                os.path.join(os.path.dirname(__file__), 'rules.txt'))
            result = logical_chain(initial_condition, initial_value, rules)
            if not result:
                error = 'Ошибка ввода данных.'

    else:
        form = LogicChainForm()

    return render(request,
                  'index.html',
                  {'form': form,
                   'result': result,
                   'error': error})
