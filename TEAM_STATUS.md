# Общий статус статьи

Этот файл фиксирует общий пул задач по статье после созвона 29 сентября и текущее состояние работы.

Это не отчет одного человека. Часть задач изначально имела конкретных исполнителей, но результат нужен один: **целостная, проверенная и готовая к подаче статья**.

## Что было в общем пуле задач

### 1. Получить тестируемую версию алгоритма

На созвоне требовалось как можно быстрее довести идею до формы, которую можно реально запускать и проверять.

**Текущий статус:** существенно закрыто, но с изменением научного фокуса.

Вместо раннего delayed-UCB варианта основным кандидатом стал variance-sensitive certified-continuum backend с явной delayed execution логикой.

Материалы:
- [Upper theorem](theory/UPPER_THEOREM.md)
- [Lower theorem](theory/LOWER_THEOREM.md)
- [Delayed execution + GADU composition](theory/DELAYED_GADU.md)

### 2. Провести эксперименты

На созвоне было важно не оставаться только на уровне теории и synthetic discussion, а проверить рабочий механизм.

**Текущий статус:** component-level проверка сделана.

В контролируемом benchmark variance-sensitive confidence сравнивался с текущим Hoeffding-подходом на одном и том же Bernoulli-потоке.

В заранее выбранных sparse-positive режимах:

```text
mean N_VS / N_H = 0.122852
```

Худший sparse-case в этом наборе — около `0.194`.

При этом найдены режимы, где `N_VS / N_H = 2`. Поэтому корректный вывод: **instance-dependent выигрыш**, а не uniform superiority.

→ [Controlled benchmark](experiments/README.md)

### 3. Проверить работу с реальными данными

На созвоне отдельно обсуждалось, что synthetic evidence, скорее всего, недостаточно, и нужно понять, какие реальные данные действительно соответствуют постановке.

**Текущий статус:** dataset/model-fit часть закрыта настолько, насколько данные позволяют делать корректные выводы.

Criteo Attribution дал важный отрицательный результат:

- 61 positive impression rows;
- 55 unique physical conversions;
- одна physical conversion может быть связана с несколькими impression rows.

Поэтому наивная интерпретация

```text
one positive row = one independent Bernoulli success
```

неверна.

Criteo полезен как real-data model-fit / attribution evidence, но не как end-to-end GADU policy benchmark.

→ [Criteo model-fit evidence](data/CRITEO_MODEL_FIT.md)

### 4. Устранить неопределенность вокруг delayed execution

На созвоне отдельно обсуждалась проблема `wait for maturation`: система не может просто ничего не делать во время ожидания feedback.

**Текущий статус:** для нового promoted backend это разрешено.

Текущий механизм:

- делает legal deployment каждый calendar round;
- не превращает unresolved silence в zero;
- использует явные synchronized checkpoints;
- отделяет filler feedback от designated estimator;
- явно учитывает calendar cost задержки.

→ [Delayed execution + GADU composition](theory/DELAYED_GADU.md)

### 5. Собрать итоговую статью и провести командное чтение

Это была общая задача после substantive edits.

**Текущий статус:** еще не закрыто.

Научные компоненты собраны, но перед финальной версией нужно пройти несколько общих ворот качества.

## Что еще нужно сделать, чтобы статья состоялась

### A. Независимо проверить математику

Нужно независимо пройти:

- upper theorem;
- lower theorem;
- delayed/GADU bridge.

Формат результата: **PASS / FIX / BLOCK**.

→ [MATH_REVIEW.md](MATH_REVIEW.md)

### B. Проверить novelty и границы claims

Нужно убедиться, что:

- новый результат действительно не поглощается ближайшими работами;
- формулировки не сильнее доказанного;
- нет необоснованных `first`, `optimal`, `minimax`, `uniformly better`.

### C. Перестроить manuscript вокруг выжившего результата

Нужно согласовать между собой:

- title;
- abstract;
- contributions;
- related work;
- порядок theorem pair;
- delayed integration;
- experiment story;
- limitations.

→ [PAPER_REVIEW.md](PAPER_REVIEW.md)

### D. Провести полное coauthor reading

После математического и содержательного freeze основной текст нужно прочитать целиком всем соавторам и собрать замечания уже к одной версии.

### E. Финальная сборка

После отсутствия BLOCK:

- убрать оставшиеся TODO;
- проверить proof references и numbering;
- проверить figures/tables/bibliography;
- собрать финальный PDF;
- зафиксировать одну submission version.

## Что предлагается решить на следующем созвоне

1. Есть ли математический BLOCK?
2. Считаем ли variance-sensitive theorem pair основной научной историей статьи?
3. Какие обязательные изменения нужны в manuscript?
4. Кто берет каждый оставшийся блок и какой у него срок?

Итоговая цель общая:

> **не закрыть отдельные индивидуальные задачи, а довести одну общую статью до состояния, которое все соавторы готовы защищать.**
