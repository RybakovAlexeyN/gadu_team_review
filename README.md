# GADU — материалы к командному ревью

Это публичный пакет по текущему состоянию статьи. Здесь собраны только материалы, которые нужны для следующего командного шага: общий статус, математическая проверка, научная история, контролируемый эксперимент и выводы по реальным данным.

## С чего начать

### Общий статус статьи
→ [TEAM_STATUS.md](TEAM_STATUS.md)

Что было в общем пуле задач после созвона 29 сентября, что уже закрыто и что еще нужно довести до submission-ready состояния.

### Математическая проверка
→ [MATH_REVIEW.md](MATH_REVIEW.md)

Две основные теоремы, конкретные места для атаки и формат результата: **PASS / FIX / BLOCK**.

### Проверка научной истории статьи
→ [PAPER_REVIEW.md](PAPER_REVIEW.md)

Складывается ли из текущего результата одна понятная статья, достаточно ли честно сформулирована новизна и что нужно изменить в manuscript.

## Технические материалы

- [Upper theorem](theory/UPPER_THEOREM.md)
- [Upper proof outline](theory/UPPER_PROOF.md)
- [Lower theorem](theory/LOWER_THEOREM.md)
- [Lower proof outline](theory/LOWER_PROOF.md)
- [Delayed execution + GADU composition](theory/DELAYED_GADU.md)
- [Controlled benchmark](experiments/README.md)
- [Criteo model-fit evidence](data/CRITEO_MODEL_FIT.md)
- [Полный список вопросов для научного ревью](REVIEW_REQUEST.md)

## Текущий научный кандидат

Он состоит из четырех частей:

1. variance-sensitive upper bound для certified Lipschitz continuum optimization с Bernoulli-наблюдениями;
2. scoped fine-gap lower bound с той же локальной Bernoulli information structure;
3. исполнимый delayed positive-only механизм;
4. интеграция в GADU через существующий certified-optimizer interface.

## Чего мы не утверждаем

Мы не заявляем:

- что новый метод всегда лучше Hoeffding;
- что сам по себе закон `q^-1` новый;
- полный minimax characterization;
- end-to-end validation GADU на Criteo;
- приоритет формулировки «first» без отдельной проверки литературы.

Главный вопрос перед финальной сборкой статьи:

> **Есть ли substantive BLOCK в математике, интеграции или научной истории?**
