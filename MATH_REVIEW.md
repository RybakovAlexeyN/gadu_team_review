# Математическая проверка

Задача этого раздела — независимо попытаться сломать две основные теоремы и их связь с delayed GADU.

Итог по каждому блоку:

- **PASS** — существенной проблемы нет;
- **FIX** — результат жив, но statement/proof нужно поправить;
- **BLOCK** — есть ошибка, которая ломает заявленный результат.

Если есть FIX или BLOCK, полезно указать точный шаг и минимальный ремонт.

## 1. Upper theorem

→ [Формулировка](theory/UPPER_THEOREM.md)  
→ [Proof outline](theory/UPPER_PROOF.md)

Проверить цепочку:

```text
empirical Bernstein confidence
→ valid cell upper bounds
→ safe pruning
→ near-optimality of every sampled child
→ weighted packing
→ packing-to-volume
→ dyadic scale summation
→ final integral bound
```

Особенно важно атаковать:

1. simultaneous confidence при adaptive activation / stopping;
2. переход parent survivor → every sampled child is near-optimal;
3. направление packing-to-volume inequality;
4. boundary handling на `[0,1]^d`;
5. coarse-scale absorption;
6. скрытую зависимость внутри `Lambda`;
7. крайние случаи вроде малых `L`, плоской функции и `epsilon` около 1.

## 2. Lower theorem

→ [Формулировка](theory/LOWER_THEOREM.md)  
→ [Proof outline](theory/LOWER_PROOF.md)

Проверить цепочку:

```text
hard alternatives
→ Bernoulli KL
→ adaptive change of measure
→ disjoint packing inside a layer
→ layer aggregation
→ fine-gap integral
```

Особенно важно:

1. все ли perturbations остаются в заявленном Lipschitz class;
2. действительно ли каждая alternative flips the best family;
3. корректен ли Bernoulli KL bound на всем заявленном диапазоне;
4. честно ли учтен logarithmic loss по слоям;
5. корректен ли fixed fine-gap cutoff;
6. не расширяется ли statement случайно с `A_fine` на весь `X`;
7. достаточно ли точно определены `delta`-correctness и stopping model.

## 3. Связь с delayed GADU

→ [Delayed execution + GADU composition](theory/DELAYED_GADU.md)

Ключевые вопросы:

- каждый ли calendar round имеет legal deployment;
- unresolved feedback нигде не считается нулем;
- clean ли ownership данных при fallback;
- корректно ли переводится scaled certificate обратно в latent scale;
- использует ли continuation gate именно latent deployment error.

## Удобный формат результата

| Блок | Вердикт | Где проблема, если есть |
|---|---|---|
| Upper theorem | PASS / FIX / BLOCK | ... |
| Lower theorem | PASS / FIX / BLOCK | ... |
| Delayed/GADU bridge | PASS / FIX / BLOCK | ... |

Самый ценный результат ревью — конкретный контрпример или точный шаг, который нельзя доказать.
