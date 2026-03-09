{% extends 'dogs/layout.html' %}
{% load tags %}
{% block content %}

    <div class="row mt-3">
        <div class="col-auto">
            <img src="{% media dog.photo %}" alt="{{ dog.name }}" class="dog-detail-img">
            <form class="row gap-2 mx-auto mt-2" method="POST" action="{% url 'dogs:dog_delete' dog.id %}">
                {% csrf_token %}
                <a class="btn btn-outline-primary col" href="{% url 'dogs:dog_update' dog.id %}">Изменить</a>
                <button class="btn btn-outline-danger col" type="submit">Удалить</button>
            </form>
        </div>
        <div class="col">
            <p><strong>Кличка: </strong>{{ dog.name }}</p>
            <p><strong>Порода: </strong><a href="{% url 'dogs:breed_details' dog.breed.id %}">{{ dog.breed }}</a></p>
            <strong>Описание:</strong>
            <p>{{ dog.description }}</p>
        </div>
    </div>
{% endblock %}