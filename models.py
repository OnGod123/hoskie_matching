# forms.py
from django import forms

class SexualFantasiesForm(forms.Form):
    sex_orientation = forms.ChoiceField(
        choices=[
            ("BDSM", "BDSM fantasy"),
            ("threesome", "Threesome fantasy"),
            ("public_sex", "Public sex fantasy"),
            ("voyeurism", "Voyeurism fantasy"),
            ("roleplay", "Roleplay fantasy"),
            ("blindfolding", "Blindfolding fantasy"),
            ("adventure", "Adventure fantasy"),
            ("caregiving", "Fantasy of caregiving"),
            ("cross_dressing", "Cross-dressing fantasy"),
            ("power_exchange", "Fantasy of power exchange"),
            ("romantic", "Romantic fantasies"),
        ],
        required=False,
        label="Select a Sexual Fantasy"
    )
    custom_sexual_fantasy = forms.CharField(max_length=255, required=False, label="Or enter your own Fantasy")
    fantasy_description = forms.CharField(widget=forms.Textarea, required=False, label="Describe your Fantasy")


class PhysicalAppearanceForm(forms.Form):
    physical_preference = forms.ChoiceField(
        choices=[
            ("muscular", "Muscular Build"),
            ("slim", "Slim Build"),
            ("curvy", "Curvy Build"),
            ("average", "Average Build"),
        ],
        required=False,
        label="Select a Physical Preference"
    )
    custom_physical_preference = forms.CharField(max_length=255, required=False, label="Or enter your own Physical Preference")
    appearance_description = forms.CharField(widget=forms.Textarea, required=False, label="Describe the Physical Appearance Preference")


class SpecificTraitsForm(forms.Form):
    facial_feature = forms.ChoiceField(
        choices=[
            ("strong_jawline", "Strong Jawline"),
            ("full_lips", "Full Lips"),
            ("facial_hair", "Distinctive Facial Hair Styles"),
        ],
        required=False,
        label="Select a Facial Feature"
    )
    custom_facial_feature = forms.CharField(max_length=255, required=False, label="Or enter your own Facial Feature")
    trait_description = forms.CharField(widget=forms.Textarea, required=False, label="Describe the Facial Feature Preference")
