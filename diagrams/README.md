# Диаграммы проекта

| Модель | Нотация | Описание | Markdown | PNG | Исходник |
| --- | --- | --- | --- | --- | --- |
| **AS-IS** | **BPMN 2.0** | Ручная проверка на КПП | [business_process_before.md](../docs/diagrams/business_process_before.md) | [PNG](rendered/business-process-as-is.png) | [PlantUML](source/business-process-as-is.puml) |
| **TO-BE** | **BPMN 2.0** | Процесс после внедрения ML-системы | [business_process_after.md](../docs/diagrams/business_process_after.md) | [PNG](rendered/business-process-to-be.png) | [PlantUML](source/business-process-to-be.puml) |
| MVP процесс | Mermaid | Пропуск + проверка лица (пилот) | [business_process_mvp.md](../docs/diagrams/business_process_mvp.md) | [PNG](rendered/business-process-to-be.png) | [Mermaid](source/business-process-to-be.mmd) |
| Данные | Mermaid ER | Структура и распределение данных | [data_model.md](../docs/diagrams/data_model.md) | [PNG](rendered/data-er-diagram.png) | [Mermaid](source/data-er-diagram.mmd) |
| Архитектура | Mermaid | Распределенная система | [system_architecture.md](../docs/diagrams/system_architecture.md) | [PNG](rendered/system-architecture.png) | [Mermaid](source/system-architecture.mmd) |
| UML компоненты | Mermaid | Программные компоненты | [uml_components.md](../docs/diagrams/uml_components.md) | [PNG](rendered/uml-components.png) | [Mermaid](source/uml-components.mmd) |
| UML sequence | Mermaid | Проход через КПП (1:N) | [uml_sequence.md](../docs/diagrams/uml_sequence.md) | [PNG](rendered/uml-sequence-access.png) | [Mermaid](source/uml-sequence-access.mmd) |
| UML sequence MVP | Mermaid | Проход «пропуск + лицо» | [uml_sequence_mvp.md](../docs/diagrams/uml_sequence_mvp.md) | [PNG](rendered/uml-sequence-access.png) | [Mermaid](source/uml-sequence-access.mmd) |

Бизнес-процессы AS-IS и TO-BE выполнены в **PlantUML** с дорожками BPMN (lanes), типами задач и XOR-шлюзами, как требует задание.
