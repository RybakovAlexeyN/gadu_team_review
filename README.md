# GADU — материалы к командному ревью

Это публичный пакет к командному созвону. Здесь только то, что нужно для проверки текущего научного результата: статус, математика, интеграция, контролируемый эксперимент и выводы по реальным данным.

## С чего начать

### Юрий — статус проекта, 3 минуты
→ [PROJECT_STATUS.md](PROJECT_STATUS.md)

Что уже закрыто после созвона 29 сентября, где сейчас главный риск статьи и какие решения нужны от команды.

### Саша — математическая проверка
→ [MATH_REVIEW.md](MATH_REVIEW.md)

Две основные теоремы, конкретные места для атаки и требуемый итог: **PASS / FIX / BLOCK**.

### Ильгам — целостность статьи
→ [PAPER_REVIEW.md](PAPER_REVIEW.md)

Складывается ли из результата одна понятная научная история и что нужно изменить в тексте статьи.

## Технические материалы

- [Upper theorem](theory/UPPER_THEOREM.md)
- [Upper proof outline](theory/UPPER_PROOF.md)
- [Lower theorem](theory/LOWER_THEOREM.md)
- [Lower proof outline](theory/LOWER_PROOF.md)
- [Delayed execution + GADU composition](theory/DELAYED_GADU.md)
- [Controlled benchmark](experiments/README.md)
- [Criteo model-fit evidence](data/CRITEO_MODEL_FIT.md)
- [Полный список вопросов для научного ревью](REVIEW_REQUEST.md)

## Что мы утверждаем

Текущий кандидат состоит из четырех частей:

1. variance-sensitive upper bound для certified Lipschitz continuum optimization с Bernoulli-наблюдениями;
2. fine-gap lower bound с той же локальной Bernoulli information structure;
3. исполнимый delayed positive-only механизм;
4. аккуратная интеграция в GADU через существующий certified-optimizer interface.

## Чего мы не утверждаем

Мы не заявляем:

- что новый метод всегда лучше Hoeffding;
- что сам по себе закон `q^-1` новый;
- полный minimax characterization;
- end-to-end validation GADU на Criteo;
- приоритет формулировки «first» без отдельной проверки литературы.

Главный вопрос к команде перед финальной сборкой статьи:

> **Есть ли substantive BLOCK в математике, интеграции или научной истории?**
