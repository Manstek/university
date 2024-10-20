from django import forms
import os

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

rules = load_rules(os.path.join(os.path.dirname(__file__), 'rules.txt'))
condition = []
value = []
for i in range(0, len(rules), 1):
    value.append((rules[i][1], rules[i][1]))

for i in range(0, len(rules), 2):
    condition.append((rules[i][0], rules[i][0]))

class LogicChainForm(forms.Form):
    initial_condition = forms.ChoiceField(
        label='Объект',
        choices=condition,
        widget=forms.Select(attrs={'class': 'form-select'})  # Добавляем класс Bootstrap
    )
    initial_value = forms.ChoiceField(
        label='Значение',
        choices=value,
        widget=forms.Select(attrs={'class': 'form-select'})  # Добавляем класс Bootstrap
    )
