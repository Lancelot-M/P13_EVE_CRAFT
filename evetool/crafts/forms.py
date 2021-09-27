from django import forms
from config import REACTIONS, COMPOSANTS, ITEMS, REACTION_STRUCTURES, RIGGS_PROD, \
    RIGGS_REACTION, MANUFACTURING_STRUCTURES, ARBORESCENCE, DECRYPTOR, SKILL, ME_LIST, TE_LIST


class CraftForm(forms.Form):
    reaction = forms.MultipleChoiceField(choices=REACTIONS,
                                         widget=forms.CheckboxSelectMultiple(attrs={'class': "form-check-input"}),
                                         required=False)
    composant = forms.MultipleChoiceField(choices=COMPOSANTS,
                                          widget=forms.CheckboxSelectMultiple(attrs={'class': "form-check-input"}),
                                          required=False)
    items = forms.MultipleChoiceField(choices=ITEMS,
                                      widget=forms.CheckboxSelectMultiple(attrs={'class': "form-check-input"}),
                                      required=False)
    reaction_structures = forms.ChoiceField(choices=REACTION_STRUCTURES)
    reaction_rigg = forms.ChoiceField(choices=RIGGS_REACTION)
    item_t1_structures = forms.ChoiceField(choices=MANUFACTURING_STRUCTURES)
    item_t1_rigg = forms.ChoiceField(choices=RIGGS_PROD)
    item_t2_structures = forms.ChoiceField(choices=MANUFACTURING_STRUCTURES)
    item_t2_rigg = forms.ChoiceField(choices=RIGGS_PROD)
    fuel_block = forms.BooleanField(required=False)
    arborescence = forms.ChoiceField(choices=ARBORESCENCE)
    ME = forms.ChoiceField(choices=ME_LIST)
    TE = forms.ChoiceField(choices=TE_LIST)
    science1 = forms.ChoiceField(choices=SKILL)
    science2 = forms.ChoiceField(choices=SKILL)
    encryption = forms.ChoiceField(choices=SKILL)
    decryptor = forms.ChoiceField(choices=DECRYPTOR)
