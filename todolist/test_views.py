import pytest
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse
from pytest_django.asserts import *

from .models import Task, Project
from base.models import CustomUser

def initialize_client():
    client = Client()
    client.login(username="testUser", password="testPassword")
    return client


def create_user():
    user = CustomUser.objects.create_user(
        username="testUser",
        password="testPassword",
    )
    return user


@pytest.mark.django_db(True)
def test_task_creation():
    task = Task.objects.create(title='test1',
                               content='test2',
                               status_of_completion=False)
    assert task.title == 'test1'
    assert task.content == 'test2'
    assert task.status_of_completion is False
    assert task.project is None


@pytest.mark.django_db(True)
def test_task_delete():
    task = Task.objects.create(title='test1',
                               content='test2',
                               status_of_completion=False)
    assert Task.objects.all().count() == 1

    Task.objects.filter(title='test1').delete()
    assert Task.objects.all().count() == 0


@pytest.mark.django_db(True)
def test_task_update():
    task = Task.objects.create(title='test1',
                               content='test2',
                               status_of_completion=False)
    assert Task.objects.filter(title='test1').count() == 1

    Task.objects.filter(title='test1').update(title='test2')
    assert Task.objects.filter(title='test1').count() == 0
    assert Task.objects.filter(title='test2').count() == 1


@pytest.mark.django_db(True)
def test_project_creation():
    project = Project.objects.create(title='project1',
                                     description='pro1')
    assert project.title == 'project1'
    assert project.description == 'pro1'
    assert project.user is None


@pytest.mark.django_db(True)
def test_project_delete():
    project = Project.objects.create(title='project1',
                                     description='pro1')
    assert Project.objects.all().count() == 1

    Project.objects.filter(title='project1').delete()
    assert Project.objects.all().count() == 0


@pytest.mark.django_db(True)
def test_project_update():
    project = Project.objects.create(title='project1',
                                     description='pro1')
    assert Project.objects.filter(title='project1').count() == 1

    Project.objects.filter(title='project1').update(title='p2')
    assert Project.objects.filter(title='project1').count() == 0
    assert Project.objects.filter(title='p2').count() == 1


@pytest.mark.django_db
def test_one_task():
    task = Task.objects.create(title='Task 1', user=create_user(),
                               content='This is just content')
    client = initialize_client()
    response = client.get(reverse('todolist:tasks'))
    assertQuerysetEqual(response.context['tasks'], [task])


@pytest.mark.django_db
def test_no_tasks():
    create_user()
    client = initialize_client()
    response = client.get(reverse("todolist:tasks"))
    assert response.status_code == 200
    assertTemplateUsed(response, "todolist/task_list.html")
    assert response.context['tasks'].count() == 0
    assertQuerysetEqual(response.context['tasks'], [])


@pytest.mark.django_db
def test_one_project():
    project = Project.objects.create(title='Project 1', user=create_user(),
                                     description='This is just description')
    client = initialize_client()
    response = client.get(reverse('todolist:project', kwargs={'pk': 1}))
    assertTemplateUsed(response, "todolist/project.html")
    assertQuerysetEqual(response.context['projects'], [project])


@pytest.mark.django_db
def test_no_projects():
    create_user()
    client = initialize_client()
    response = client.get(reverse("todolist:tasks"))
    assert response.status_code == 200
    assertTemplateUsed(response, "todolist/task_list.html")
    assert response.context['projects'].count() == 0
    assertQuerysetEqual(response.context['projects'], [])
