from django.utils.translation import gettext_lazy as _

NON_FORM_VALUES = ['page', 'csrfmiddlewaretoken', 'save_to_favorites']

MESSAGE_SUBJECT = 'Comment on SCRPR'
LOGIN_MESSAGE = _('Please log in to access this page.')
PASSWORD_MATCH_ERROR = _("Passwords do not match")
PSPLUS_PRICE_LABEL = _('PS Plus offer')
INITIAL_PRICE_LABEL = _('With discount')
FREE_LABEL = _('FREE')
NUMERIC_MIN_LABEL = _('From')
NUMERIC_MAX_LABEL = _('To')
WITH_SALARY_LABEL = _('Only with salary')
GAMES_TITLE_LABEL = _('Game title')
JOBS_TITLE_LABEL = _('Job title')
NOTIFICATION_LABEL = _('Notify me')

RATE_NAME_ATTRS = {
    'class': 'rate_field field',
    'placeholder': _('Name')
}
RATE_COMMENT_ATTRS = {
    'class': 'rate_field field',
    'placeholder': _('Comment')
}
USERNAME_ATTRS = {
    'class': 'auth_field field',
    'placeholder': _('Username')
}
EMAIL_ATTRS = {
    'class': 'auth_field field',
    'placeholder': _('Email')
}
PASSWORD_ATTRS = {
    'class': 'auth_field field',
    'placeholder': _('Password')
}
CONFIRM_PASSWORD_ATTRS = {
    'class': 'auth_field field',
    'placeholder': _('Confirm password')
}

GAMES_INPUT_ATTRS = {
    'class': 'field search_field_games',
    'Placeholder': _('Game title...'),
}
CHECKBOX_ATTRS = {
    'class': 'checkbox'
}
JOBS_INPUT_ATTRS = {
    'class': 'field search_field_jobs',
    'placeholder': _('Job title...'),
}
CITY_CHOICES = [
    (None, _('All Ukraine')),
    ('Киев', _('Kyiv')),
    ('Одесса', _('Odessa')),
    ('Днепр', _('Dnipro')),
    ('Харьков', _('Kharkov')),
    ('Львов', _('Lviv')),
]
CITIES_ATTRS = {
    'class': 'field city_filter city_separate',
}
NUMERIC_FILTER_ATTRS = {
    'class': 'field numeric_filter',
}

NOTIFICATION_CHOICES = [
    (None, _('Never')),
    (1, _('Every day')),
    (7, _('Every week')),
    (30, _('Every month')),
]
CHOICES_DICT = {
    None: _('Never'),
    1: _('Every day'),
    7: _('Every week'),
    30: _('Every month'),
}
