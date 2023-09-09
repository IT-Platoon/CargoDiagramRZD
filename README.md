CargoDiagramRZD

### Требования

Необходимо, чтобы были установлены следующие компоненты:

- `Docker` и `docker-compose`

### Запуск

1. Генерация переменных окружения:
```commandline
make env
```

1. Запуск приложения:
```commandline
make docker-run
```

### Статический анализ

- Запуск линтеров:
```commandline
make lint
```

- Запуск форматирования кода:
```commandline
make format
```

### Дополнительные команды

- Открытие контейнера внутри Docker-контейнера:
```commandline
make open-server
```

- Вывести список всех команд и их описание:
```commandline
make help
```
