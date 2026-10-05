# VS-Certify-Delayed — алгоритм в одном месте

Это текущая исполнимая процедура, вокруг которой собран новый variance-sensitive backend.

Главная цель этого файла — чтобы алгоритм можно было понять до чтения теорем и proof outline.

## В двух словах

Алгоритм постепенно уточняет области поиска внутри каждой family, использует empirical-Bernstein confidence для Bernoulli-наблюдений и принимает новое геометрическое решение только после того, как designated feedback для текущего checkpoint успел дозреть.

Короткая схема:

```text
active cells
→ designated pulls
→ synchronized checkpoint
→ w legal filler rounds
→ finalize matured Bernoulli outcomes
→ update empirical-Bernstein intervals
→ prune impossible cells
→ split survivors
→ check family separation
→ CERTIFIED / continue / NOT_CERTIFIED
```

## Что именно модернизировано

По сравнению с более ранним описанием теперь явно зафиксировано:

- статистическое решение принимается на synchronized checkpoints;
- для confidence используется observable empirical-Bernstein radius;
- designated и filler rounds разделены;
- после последнего designated source checkpoint выполняется ровно `w` legal filler deployments;
- unresolved feedback никогда не интерпретируется как zero;
- active set не меняется во время одного flush;
- после flush все дозревшие designated outcomes финализируются одновременно;
- prune/split происходит только после обновления confidence;
- hard cutoff возвращает `NOT_CERTIFIED`, а не искусственную сертификацию;
- при нескольких families confidence budget делится между ними заранее;
- результат переводится из scaled mean `g_i=q_w f_i` обратно в latent-scale certificate перед GADU continuation.

## Пошаговая процедура

### 1. Активные области

Для каждой family поддерживается набор активных dyadic cells.

У каждой cell есть center `c` и geometric uncertainty `a_h`.

### 2. Designated sampling

В центрах unresolved cells собираются designated Bernoulli observations.

Для `n>=2` finalized samples используется empirical-Bernstein radius

```text
r_n =
sqrt(2 V_n log(6/eta) / n)
+
7 log(6/eta) / (3(n-1)).
```

Cell считается statistically resolved на текущем уровне, когда radius достаточно мал относительно `a_h`.

### 3. Synchronized checkpoint

Cumulative sample targets идут геометрически:

```text
n_r = 2^(r+1).
```

До checkpoint все unresolved cells доводятся до текущего target.

### 4. Delayed flush

После последнего designated source текущего checkpoint выполняется ровно `w` legal filler deployments.

Во время flush:

- алгоритм продолжает делать legal deployment каждый calendar round;
- filler feedback не входит в designated estimator;
- active set заморожен до конца flush.

Если `w=0`, flush пустой.

### 5. Finalization

После flush designated source с delay не больше `w` превращается в

```text
B_s^(w) = 1{Z_s=1 and D_s<=w}.
```

Неразрешенная тишина до этого момента не считается нулем.

### 6. Confidence + cell bounds

После finalization пересчитываются:

- empirical mean;
- sample variance;
- empirical-Bernstein interval;
- Lipschitz cell upper bound.

### 7. Prune / split

Cell удаляется, если ее valid upper bound уже ниже лучшего lower bound внутри той же family.

Все surviving cells делятся на dyadic children, и процесс повторяется на следующем уровне.

### 8. Family certification

Для family `i` строятся learner-computable bounds

```text
ell_i^g <= g_i(z_i) <= g_i^* <= U_i^g.
```

Если

```text
ell_i^g > max_{j != i} U_j^g,
```

то family `i` сертифицирована как лучшая в scaled model.

Поскольку `g_i=q_w f_i` и общий `q_w>0`, ordering families сохраняется.

### 9. Возврат в latent scale

Для continuation используются

```text
ell_i = max(0, ell_i^g/q_w)
U_i   = min(1, U_i^g/q_w)
Xi_i  = min(1, xi_i^g/q_w).
```

Критично: downstream gate использует именно latent deployment error `Xi_i`.

### 10. Hard cutoff

Если до заранее заданного calendar cutoff `B` certificate не получен, алгоритм возвращает

```text
NOT_CERTIFIED
```

и может быть запущен clean fallback на оставшемся horizon.

Все source rounds, принадлежавшие certification phase, включая fillers и их поздние arrivals, исключаются из fresh fallback statistics.

## Calendar accounting

Если:

- `D` — число designated source pulls;
- `C_h` — число synchronized checkpoints на уровне `h`;

то до hard-horizon truncation

```text
T_cal = D + w * sum_h C_h.
```

То есть delay cost учитывается явно как pipeline/checkpoint overhead.

## Что этот алгоритм не утверждает

Сам по себе этот файл не означает, что:

- новый backend всегда лучше текущего;
- batching/checkpoint schedule оптимален;
- `q_w^-1` является новой закономерностью;
- текущие GADU Theorem 1/8 или scheduler theorem автоматически заменяются;
- доказана end-to-end superiority на реальных данных.

## Куда идти дальше

- [Upper theorem](theory/UPPER_THEOREM.md)
- [Upper proof outline](theory/UPPER_PROOF.md)
- [Lower theorem](theory/LOWER_THEOREM.md)
- [Lower proof outline](theory/LOWER_PROOF.md)
- [Delayed execution + GADU composition](theory/DELAYED_GADU.md)
- [Mathematical review checklist](MATH_REVIEW.md)
