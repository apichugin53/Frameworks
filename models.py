import datetime

from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.forms.fields import FileField, DateField
from django.forms.models import inlineformset_factory, BaseInlineFormSet, ModelChoiceField
from django.forms.widgets import FileInput, TextInput, Textarea, Select, DateInput
from django.utils.translation import gettext_lazy as _

from dogs.models import Dog, Pedigree


class DogForm(ModelForm):
    photo = FileField(
        label=_('Photo'),
        required=False,
        widget=FileInput(attrs={'class': 'form-control'})
    )
    birth_date = DateField(
        label=_('Birth date'),
        required=False,
        widget=DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
    )
    error_css_class = 'error-wrapper'

    class Meta:
        model = Dog
        exclude = ('owner',)
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'breed': Select(attrs={'class': 'form-select'}),
            'description': Textarea(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pedigree_formset = PedigreeFormSet(data=kwargs.get('data'), instance=self.instance)

    def clean_birth_date(self):
        birth_date = self.cleaned_data['birth_date']
        if birth_date:
            now = datetime.datetime.today().date()
            before = datetime.date(now.year - 20, now.month, now.day)
            if birth_date > now:
                raise ValidationError(_('Birth date must not be in the future'))
            if birth_date < before:
                raise ValidationError(_('Birth date must not be older than 20 years ago'))
        return birth_date

    def clean(self):
        self.pedigree_formset.clean()
        return super().clean()

    def save(self, **kwargs):
        saved_req = super().save(**kwargs)
        self.pedigree_formset.instance = saved_req
        self.pedigree_formset.save()
        return saved_req

    def is_valid(self):
        return self.pedigree_formset.is_valid() and super().is_valid()

    def has_changed(self):
        return self.pedigree_formset.has_changed() and super().has_changed()


class PedigreeForm(ModelForm):
    ancestor = ModelChoiceField(label=_('Ancestor'), queryset=None,
                                widget=Select(attrs={'class': 'form-control'}),
                                required=False)
    error_css_class = 'error-wrapper'

    def __init__(self, *args,  **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ancestor'].queryset = Dog.objects.all()

    class Meta:
        model = Pedigree
        fields = ('ancestor',)


def pedigree_formset_factory():
    return inlineformset_factory(parent_model=Dog, model=Pedigree,
                                 form=PedigreeForm, formset=BaseInlineFormSet,
                                 fk_name='descendant', can_delete=True,
                                 extra=2, max_num=2)


PedigreeFormSet = pedigree_formset_factory()
