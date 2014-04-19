"""An interface between the server and the templating system."""

import os

import jinja2


TEMPLATE_PATH = os.path.dirname(os.path.dirname(__file__)) + '/views'

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(TEMPLATE_PATH),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


def render(template_name, template_values):
    """Renders the template with the provided name and values.

    Args:
      template_name: a string with the filename of the Jinja2 template.
      template_values: a dict with the values to be used in the template.

    Returns:
      The rendered template as a string.
    """
    return JINJA_ENVIRONMENT.get_template(template_name).render(template_values)
