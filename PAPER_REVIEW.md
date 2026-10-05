# Проверка научной истории статьи

Главный вопрос этого раздела:

> **Получается ли из текущего результата одна понятная и защищаемая статья?**

## Научная история в одном абзаце

Мы рассматриваем certified optimization / family selection в ситуации, где положительные события могут быть редкими, а обратная связь приходит с задержкой.

Текущий Hoeffding-style подход использует глобально консервативную статистическую цену. Новый variance-sensitive backend использует локальную Bernoulli information structure и в sparse-positive режимах может существенно уменьшать число наблюдений.

При этом мы не утверждаем uniform improvement: controlled benchmark специально содержит режимы, где новый вариант хуже.

Для delayed setting результат доведен до исполнимого механизма: каждый календарный раунд имеет действие, unresolved feedback не считается нулем, а новый backend подключается к существующему GADU certified-optimizer interface.

## Что доказано

- [Variance-sensitive upper theorem](theory/UPPER_THEOREM.md)
- [Scoped fine-gap lower theorem](theory/LOWER_THEOREM.md)
- [Delayed execution and GADU composition](theory/DELAYED_GADU.md)

## Что показано экспериментально

→ [Controlled benchmark](experiments/README.md)

В заранее выбранных sparse-positive regimes:

```text
mean N_VS/N_H ≈ 0.123
```

Но есть regimes с ratio `2.0`.

Следовательно правильный empirical claim:

> **instance-dependent sparse-positive sample efficiency**

а не «новый метод всегда лучше».

## Что дали реальные данные

→ [Criteo model-fit evidence](data/CRITEO_MODEL_FIT.md)

Criteo показал, что наивное соответствие

```text
one positive row = one independent Bernoulli success
```

неверно: один physical conversion может быть связан с несколькими impression rows.

Поэтому Criteo — полезное model-fit/falsification evidence, но не end-to-end validation GADU.

## Что нужно проверить с точки зрения статьи

1. Понятна ли проблема с первых абзацев без знания внутренней истории проекта?
2. Ясно ли, чем новый результат отличается от старого GADU-Cover?
3. Достаточно ли узко и честно сформулирована novelty?
4. Должен ли theorem pair быть главным результатом основной части статьи?
5. Правильно ли experiment section поддерживает theorem, а не обещает больше?
6. Достаточно ли четко разделены:
   - теория;
   - controlled evidence;
   - real-data model-fit evidence?
7. Какие 2–3 изменения сильнее всего улучшат abstract / contributions / story?

## Удобный формат результата

1. **Да / нет:** складывается ли из этого одна paper story?
2. Что сейчас мешает читателю понять главный contribution?
3. Какие изменения текста обязательны до общего финального чтения?

Если математика получает PASS, следующий шаг — перестроить manuscript вокруг той истории, которая выдержала review.
