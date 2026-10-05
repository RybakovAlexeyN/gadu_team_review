# GADU — текущее состояние статьи

Здесь собран текущий научный результат и материалы для командной проверки перед финальной сборкой manuscript.

## Главное обновление: оформлен исполнимый алгоритм

Текущую процедуру немного модернизировали и вынесли в отдельный алгоритм **VS-Certify-Delayed**.

Сейчас execution flow зафиксирован явно:

```text
active cells
→ designated pulls
→ synchronized checkpoint
→ w legal filler rounds
→ finalize matured outcomes
→ empirical-Bernstein confidence
→ prune / split
→ family certification
→ CERTIFIED / continue / NOT_CERTIFIED
```

То есть теперь отдельно видно не только theorem-level идею, но и то, **что алгоритм делает по шагам в каждый момент времени**, включая delayed feedback.

→ [Алгоритм: VS-Certify-Delayed](ALGORITHM.md)

## Что уже сделано по статье

### 1. Сформирован новый научный кандидат

Текущая версия результата состоит из четырех связанных частей:

- variance-sensitive certified-continuum upper bound для Bernoulli-наблюдений;
- scoped fine-gap lower bound с той же локальной information structure;
- исполнимый delayed positive-only механизм;
- интеграция нового backend в GADU через certified-optimizer interface.

Материалы:
- [Алгоритм: VS-Certify-Delayed](ALGORITHM.md)
- [Upper theorem](theory/UPPER_THEOREM.md)
- [Lower theorem](theory/LOWER_THEOREM.md)
- [Delayed execution + GADU composition](theory/DELAYED_GADU.md)

Математическое ядро прошло внутренние проверки, но независимый coauthor review еще нужен.

### 2. Сделан контролируемый эксперимент

Variance-sensitive confidence сравнен с текущим Hoeffding-подходом на одном и том же Bernoulli-потоке.

В выбранных sparse-positive режимах:

```text
mean N_VS / N_H = 0.122852
```

Худший sparse-case в этом наборе — около `0.194`.

При этом есть режимы, где `N_VS / N_H = 2`, поэтому корректный вывод — **instance-dependent выигрыш**, а не uniform superiority.

→ [Controlled benchmark](experiments/README.md)

### 3. Проверена применимость реальных данных

На Criteo Attribution проверено, какие выводы из реальных логов действительно допустимы.

В 1,200-row slice:

- 61 positive impression rows;
- 55 unique physical conversions;
- одна physical conversion может быть связана с несколькими impression rows.

Поэтому наивное соответствие

```text
one positive row = one independent Bernoulli success
```

неверно.

Criteo используется как real-data model-fit / attribution evidence, но не как end-to-end GADU policy benchmark.

→ [Criteo model-fit evidence](data/CRITEO_MODEL_FIT.md)

### 4. Уточнена и оформлена delayed execution процедура

Для нового backend теперь отдельно записан исполнимый алгоритм, а не только execution contract.

В нем явно определено:

- каждый calendar round имеет legal deployment;
- unresolved silence не считается zero;
- confidence обновляется на synchronized checkpoints;
- после designated sampling выполняется ровно `w` filler rounds;
- filler feedback отделен от designated estimator;
- active set не меняется во время flush;
- prune/split выполняется после maturation и обновления confidence;
- hard cutoff возвращает `NOT_CERTIFIED`;
- calendar cost задержки учитывается явно.

→ [Алгоритм: VS-Certify-Delayed](ALGORITHM.md)  
→ [Delayed execution + GADU composition](theory/DELAYED_GADU.md)

## Пул задач после созвона 29 сентября

→ [TASK_POOL.md](TASK_POOL.md)

Там зафиксировано, что требовалось довести по статье, что уже закрыто и что осталось до submission-ready версии.

## Что еще нужно проверить

### Математика
→ [MATH_REVIEW.md](MATH_REVIEW.md)

Независимо проверить upper theorem, lower theorem и delayed/GADU bridge.

### Научная история статьи
→ [PAPER_REVIEW.md](PAPER_REVIEW.md)

Проверить novelty, claims, abstract/contributions и то, складывается ли из текущего результата одна цельная paper story.

### Полный scientific review checklist
→ [REVIEW_REQUEST.md](REVIEW_REQUEST.md)

## Чего мы сейчас не утверждаем

Мы не заявляем:

- что новый метод всегда лучше Hoeffding;
- что сам по себе закон `q^-1` новый;
- полный minimax characterization;
- end-to-end validation GADU на Criteo;
- `first` без отдельной проверки литературы.

Главный следующий вопрос:

> **Есть ли substantive BLOCK, который мешает собирать финальную версию статьи?**
