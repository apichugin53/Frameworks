{% extends 'dogs/layout.html' %}
{% block content %}

    {% for breed in breeds %}
        <div class="card mt-3">
            <div class="card-body">
                <h5 class="card-title"><a href="{% url 'dogs:breed_details' breed.id %}">{{ breed.name }}</a></h5>
                <p class='breed-card'>{{ breed.description }}</p>
            </div>
        </div>
    {% empty %}
        <p>Здесь пока ничего нет</p>
    {% endfor %}

{% endblock %}