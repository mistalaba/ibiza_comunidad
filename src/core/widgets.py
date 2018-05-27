from django.forms.widgets import ChoiceFieldRenderer, ChoiceInput, CheckboxSelectMultiple
from django.utils.html import format_html


class CategoryChoiceInput(ChoiceInput):
    def render(self, name=None, value=None, attrs=None):
        if self.id_for_label:
            label_for = format_html(' for="{}"', self.id_for_label)
        else:
            label_for = ''
        attrs = dict(self.attrs, **attrs) if attrs else self.attrs
        return format_html(
            # '{1}<label{0}>{2}</label>'.format(label_for, self.tag(attrs), self.choice_label)
            '{1}<label{0} class="category" title="{2}" data-tooltip aria-haspopup="true" class="has-tip" data-disable-hover="false"><svg class="ic__icon medium ic__tag-{2}"><use xlink:href="#tag-{2}"></use></svg></label>'.format(label_for, self.tag(attrs), self.choice_label)
            # '<label{} class="category">{} {}</label>', label_for, self.tag(attrs), self.choice_label
        )


class CategoryCheckboxChoiceInput(CategoryChoiceInput):
    input_type = 'checkbox'

    def is_checked(self):
        return self.choice_value in self.value


class CategoryCheckboxFieldRenderer(ChoiceFieldRenderer):
    choice_input_class = CategoryCheckboxChoiceInput


class CategoryCheckboxSelectMultiple(CheckboxSelectMultiple):
    renderer = CategoryCheckboxFieldRenderer

