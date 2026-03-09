{% extends 'dogs/layout.html' %}
{% load i18n %}
{% load dogs.tags %}
{% block content %}

    <div class="d-flex my-3">
        <h3>{% translate 'Our dogs' %}</h3>
        <a class="btn btn-outline-success ms-auto" href="{% url 'dogs:dog_create' %}">{% translate 'Add' %}</a>
    </div>
    <div class="dogs_list">
        {% for dog in object_list %}
            <div class="card dog-card">
                <img src="{% media dog.photo %}" class="card-img-top dog-card-img bg-body-tertiary"
                     alt="{{ dog.breed }}">
                <div class="card-body">
                    <h5 class="card-title">{{ dog.name }}</h5>
                    <a href="{% url 'dogs:dog_details' dog.id %}"
                       class="btn btn-outline-primary">{% translate 'More' %}</a>
                </div>
            </div>
        {% endfor %}
    </div>
{% endblock %}