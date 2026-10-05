# Пул задач после созвона 29 сентября

Ниже зафиксированы задачи, которые нужно было довести после командного обсуждения, и их текущее состояние.

## 1. Получить тестируемую версию алгоритма

Нужно было довести идею до формы, которую можно реально запускать и проверять.

**Статус:** закрыто на уровне текущего scientific candidate.

Процедура немного модернизирована и оформлена как отдельный исполнимый алгоритм **VS-Certify-Delayed**.

Он явно задает:

- dyadic active cells;
- designated sampling;
- empirical-Bernstein confidence;
- synchronized checkpoints;
- delayed flush через `w` legal filler rounds;
- finalization matured feedback;
- prune / split;
- family certification;
- hard cutoff с `NOT_CERTIFIED`.

→ [Алгоритм: VS-Certify-Delayed](ALGORITHM.md)

Связанная математика:
- [Upper theorem](theory/UPPER_THEOREM.md)
- [Lower theorem](theory/LOWER_THEOREM.md)
- [Delayed execution + GADU composition](theory/DELAYED_GADU.md)

## 2. Провести эксперименты

Нужно было перейти от обсуждения алгоритма к измеримому сравнению с текущим подходом.

**Статус:** component-level проверка сделана.

В контролируемом benchmark новый confidence mechanism сравнен с Hoeffding на одном и том же Bernoulli-потоке.

В sparse-positive режимах среднее отношение числа наблюдений:

```text
N_VS / N_H = 0.122852
```

Есть и режимы с ratio `2`, поэтому uniform superiority не утверждается.

→ [Controlled benchmark](experiments/README.md)

## 3. Найти и проверить реальные данные

Нужно было найти dataset, соответствующий постановке, и понять, какие реальные выводы на нем допустимы.

**Статус:** dataset/model-fit часть закрыта в корректном scope.

Criteo Attribution использован для проверки delayed-positive / attribution semantics.

Главный результат: одна physical conversion может соответствовать нескольким positive impression rows, поэтому row-level iid Bernoulli mapping неверен.

→ [Criteo model-fit evidence](data/CRITEO_MODEL_FIT.md)

## 4. Устранить неопределенность вокруг ожидания feedback

На обсуждении было важно убрать неопределенное `wait for maturation`: система должна иметь определенное действие в каждый момент времени.

**Статус:** для нового backend разрешено и вынесено в отдельный алгоритм.

Текущая execution logic:

- имеет legal deployment каждый calendar round;
- не кодирует unresolved feedback как zero;
- использует synchronized checkpoints;
- после designated sampling выполняет ровно `w` filler rounds;
- замораживает active set на время flush;
- отдельно учитывает designated и filler rounds;
- делает prune/split только после finalization;
- при hard cutoff возвращает `NOT_CERTIFIED`;
- учитывает calendar cost задержки.

→ [Алгоритм: VS-Certify-Delayed](ALGORITHM.md)  
→ [Delayed execution + GADU composition](theory/DELAYED_GADU.md)

## 5. Собрать итоговую статью и провести командное чтение

После substantive edits нужно получить одну интегрированную версию текста и прочитать ее всей командой.

**Статус:** еще не закрыто.

До этого нужно пройти следующие общие шаги:

### A. Независимая математическая проверка

→ [MATH_REVIEW.md](MATH_REVIEW.md)

Нужно дать по каждому блоку один из вердиктов:

- PASS;
- FIX;
- BLOCK.

### B. Проверка novelty и границ claims

Нужно убедиться, что:

- ближайшая литература не поглощает новый результат;
- формулировки не сильнее доказанного;
- нет необоснованных `first`, `optimal`, `minimax`, `uniformly better`.

### C. Перестройка manuscript

Нужно согласовать:

- title;
- abstract;
- contributions;
- related work;
- порядок theorem pair;
- delayed integration;
- experiment story;
- limitations.

→ [PAPER_REVIEW.md](PAPER_REVIEW.md)

### D. Полное coauthor reading

После математического и содержательного freeze основной текст нужно прочитать целиком и собрать замечания к одной версии.

### E. Финальная сборка

После отсутствия BLOCK:

- убрать оставшиеся TODO;
- проверить proof references и numbering;
- проверить figures/tables/bibliography;
- собрать финальный PDF;
- зафиксировать submission version.

## Что нужно решить на следующем созвоне

1. Есть ли математический BLOCK?
2. Считаем ли variance-sensitive theorem pair основной научной историей статьи?
3. Какие изменения обязательны в manuscript?
4. Как распределяем оставшиеся задачи и сроки?
