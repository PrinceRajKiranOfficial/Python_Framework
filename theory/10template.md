Templates
Flask uses Jinja2 templates.
Used to generate dynamic HTML.
Why important?
Separates logic and design


Example:
html

{% if user %}
    Welcome {{ user }}
{% endif %}