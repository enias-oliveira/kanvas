# Kanvas

## Descrição

<p align="center">Uma API de uma versão mais  simplificada do <a href="https://www.instructure.com/pt-br/canvas">Canvas<a/>, uma plataforma para gestão de ensino usada na Kenzie Academy Brasil. </p>

## Tecnologias

- [Django](https://www.djangoproject.com/): Python Web Framework
- [Django REST Framework](https://www.django-rest-framework.org/): Python Toolkit for building Web API

## Endpoints

- `POST /accounts/ - Cadastrando um estudante:`

```json
// REQUEST
{
  "username": "student",
  "password": "1234",
  "is_superuser": false,
  "is_staff": false
}
```

```json
// RESPONSE STATUS -> HTTP 201
{
  "id": 1,
  "username": "student",
  "is_superuser": false,
  "is_staff": false
}
```

- `POST /api/accounts/ - criando um facilitador:`

```json
// REQUEST
{
  "username": "facilitator",
  "password": "1234",
  "is_superuser": false,
  "is_staff": true
}
// RESPONSE STATUS -> HTTP 201
{
  "id": 2,
  "username": "facilitator",
  "is_superuser": false,
  "is_staff": true
}
```

- `POST /api/accounts/ - criando um instrutor:`

```json
// REQUEST
{
  "username": "instructor",
  "password": "1234",
  "is_superuser": true,
  "is_staff": true
}
// RESPONSE STATUS -> HTTP 201
{
  "id": 3,
  "username": "instructor",
  "is_superuser": true,
  "is_staff": true
}
```

- `POST /api/login/ - fazendo login (serve para qualquer tipo de usuário):`

```json
// REQUEST
{
  "username": "student",
  "password": "1234"
}
// RESPONSE STATUS -> HTTP 200
{
  "token": "dfd384673e9127213de6116ca33257ce4aa203cf"
}
```

- `POST /api/courses/ - criando um curso:`

```json
// REQUEST
// Header -> Authorization: Token <token-do-instrutor>
{
  "name": "Javascript 101"
}
// RESPONSE STATUS -> HTTP 201
{
  "id": 1,
  "name": "Javascript 101",
  "user_set": []
}
```

Se for fornecido um token de estudante ou facilitador, o sistema deverá responder da seguinte forma:

```json
// REQUEST
// Header -> Authorization: Token <token-do-facilitador ou token-to-estudante>
{
  "name": "Javascript 101"
}
// RESPONSE STATUS -> HTTP 403
{
  "detail": "You do not have permission to perform this action."
}
```

- `PUT /api/courses/registrations/- atualizando a lista de estudantes matriculados em um curso:`

```json
// REQUEST
// Header -> Authorization: Token <token-do-instrutor>
{
  "course_id": 1,
  "user_ids": [1, 2, 7]
}
// RESPONSE STATUS -> HTTP 200
{
  "id": 1,
  "name": "Javascript 101",
  "user_set": [
    {
      "id": 1,
      "is_superuser": false,
      "is_staff": false,
      "username": "luiz"
    },
    {
      "id": 7,
      "is_superuser": false,
      "is_staff": false,
      "username": "isabela"
    },
    {
      "id": 2,
      "is_superuser": false,
      "is_staff": false,
      "username": "raphael"
    }
  ]
}
```

Desta forma é possível matricular vários alunos simultaneamente. Da mesma maneira, é possível remover vários estudantes ao mesmo tempo ao registrar novamente a lista de alunos.

```json
// REQUEST
// Header -> Authorization: Token <token-do-instrutor>
{
  "course_id": 1,
  "user_ids": [1]
}
// RESPONSE STATUS -> HTTP 200
{
  "id": 1,
  "name": "Javascript 101",
  "user_set": [
    {
      "id": 1,
      "is_superuser": false,
      "is_staff": false,
      "username": "luiz"
    }
  ]
}
```

- `GET /api/courses/ - obtendo a lista de cursos e alunos:`

Este endpoint pode ser acessado por qualquer client (mesmo sem autenticação).

```json
// RESPONSE STATUS -> HTTP 200
[
  {
    "id": 1,
    "name": "Javascript 101",
    "user_set": [
      {
        "id": 1,
        "is_superuser": false,
        "is_staff": false,
        "username": "luiz"
      }
    ]
  },
  {
    "id": 2,
    "name": "Python 101",
    "user_set": []
  }
]
```

- `POST /api/activities/ - criando uma atividade (estudante):`
  Mesmo que o User do tipo estudante faça um request que tem o campo grade, a nota não será registrada no momento da criação.

```json
// REQUEST
// Header -> Authorization: Token <token-do-estudante>
{
  "repo": "gitlab.com/cantina-kenzie",
  "grade": 10 // Esse campo é opcional
}
// RESPONSE STATUS -> HTTP 201
// Repare que o campo grade foi ignorado
{
  "id": 6,
  "user_id": 7,
  "repo": "gitlab.com/cantina-kenzie",
  "grade": null
}
```

- `PUT /api/activities/ - editando a nota de uma atividade (facilitador ou instrutor):`

```json
//REQUEST
//Header -> Authorization: Token <token-do-facilitador ou instrutor>
{
  "id": 6,
  "grade": 10
}
//RESPONSE STATUS -> HTTP 201
{
  "id": 6,
  "user_id": 7,
  "repo": "gitlab.com/cantina-kenzie",
  "grade": 10
}
```

- `GET /api/activities/ - listando atividades (estudante):`

```json
//REQUEST
//Header -> Authorization: Token <token-do-estudante>
[
  {
    "id": 1,
    "user_id": 1,
    "repo": "github.com/luiz/cantina",
    "grade": null
  },
  {
    "id": 6,
    "user_id": 1,
    "repo": "github.com/hanoi",
    "grade": null
  },
  {
    "id": 15,
    "user_id": 1,
    "repo": "github.com/foodlabs",
    "grade": null
  }
]
```

- `GET /api/activities/ - listando atividades (facilitador ou instrutor):`

```json
//REQUEST
//Header -> Authorization: Token <token-do-facilitador ou token-do-instrutor>
[
  {
    "id": 1,
    "user_id": 1,
    "repo": "github.com/luiz/cantina",
    "grade": null
  },
  {
    "id": 6,
    "user_id": 1,
    "repo": "github.com/hanoi",
    "grade": null
  },
  {
    "id": 10,
    "user_id": 2,
    "repo": "github.com/foodlabs",
    "grade": null
  },
  {
    "id": 35,
    "user_id": 3,
    "repo": "github.com/kanvas",
    "grade": null
  }
]
```

- `GET /api/activities/<int:user_id>/ - filtrando atividades fornecendo um user_id opcional (facilitador ou instrutor):`

Como os instrutores e facilitadores podem ver as atividades de todos os alunos, precisamos dar a eles a opção de filtrar esses dados através do user_id. Se o id enviado for 1, o retorno deve ser a lista de todas as atividades do usuário (estudante) que possui user_id = 1.

```json
//REQUEST (/api/activities/1/)
//Header -> Authorization: Token <token-do-facilitador ou token-do-instrutor>
[
  {
    "id": 1,
    "user_id": 1,
    "repo": "github.com/luiz/cantina",
    "grade": null
  },
  {
    "id": 6,
    "user_id": 1,
    "repo": "github.com/hanoi",
    "grade": null
  },
  {
    "id": 15,
    "user_id": 1,
    "repo": "github.com/foodlabs",
    "grade": null
  }
]
```

Caso o user_id enviado seja inválido, você deverá retornar um status HTTP 404 NOT FOUND.

```json
//REQUEST (/api/activities/x/)
//Header -> Authorization: Token <token-do-facilitador ou instrutor>
// RESPONSE STATUS -> HTTP 404 NOT FOUND
{
  "detail": "Invalid user_id."
}
```

## Autor

Enias Oliveira, um desafio da "Kenzie Academy Brasil"
