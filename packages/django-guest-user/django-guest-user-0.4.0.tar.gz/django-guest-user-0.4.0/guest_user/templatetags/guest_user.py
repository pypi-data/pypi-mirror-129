from django.template import Library

from ..functions import is_guest_user as is_guest_user_func

register = Library()

is_guest_user = register.filter(is_guest_user_func)
"""
Template filter to check if the passed object is a guest user.

Usage

.. code:: jinja

  {% load guest_user %}

  {% if user|is_guest_user %}
    Hello guest.
  {% endif %}

"""
