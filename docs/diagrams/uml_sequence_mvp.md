# UML-последовательность для сценария MVP

Поведенческая модель проверки «пропуск + лицо» на этапе пилота.

```mermaid
sequenceDiagram
    actor Employee as Сотрудник
    participant Terminal as Терминал КПП
    participant Camera as Камера
    participant Edge as Edge-узел
    participant API as Access Control API
    participant ML as ML Inference Service
    participant Vector as Vector Storage
    participant Operator as Оператор
    participant Turnstile as Турникет
    participant Audit as Audit Log

    Employee->>Terminal: Прикладывает пропуск
    Terminal->>Camera: Запросить кадр лица
    Camera-->>Edge: Изображение
    Edge->>API: card_id + face_image + checkpoint_id
    API->>ML: Проверить лицо владельца пропуска
    ML->>Vector: Получить эталонный шаблон
    Vector-->>ML: Template vector
    ML-->>API: similarity_score + quality + recommendation

    alt Высокая уверенность
        API->>Turnstile: Открыть проход
        API->>Audit: Записать автоматический допуск
        Turnstile-->>Employee: Проход разрешен
    else Низкая уверенность или плохой кадр
        API->>Operator: Передать спорный случай
        Operator-->>API: Подтвердить или отказать
        alt Оператор подтвердил
            API->>Turnstile: Открыть проход
            API->>Audit: Записать ручное подтверждение
        else Оператор отказал
            API->>Audit: Записать отказ
            API-->>Terminal: Показать отказ
        end
    end
```

![UML sequence MVP](../../diagrams/rendered/uml-sequence-access.png)

Исходник диаграммы: [diagrams/source/uml-sequence-access.mmd](../../diagrams/source/uml-sequence-access.mmd)
