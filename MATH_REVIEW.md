# Математическая проверка

Задача этого раздела — независимо попытаться сломать две основные теоремы и их связь с delayed GADU.

После внутреннего red-team формулировки были дополнительно ужесточены: в public theorem files теперь явно зафиксированы confidence allocation, empirical-Bernstein radius, lower-bound correctness model, fine-gap cutoff и delayed execution semantics. Это не заменяет независимый coauthor review.

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
6. корректность явной confidence allocation и определения `Lambda`;
7. переход между clipped coarse levels и fine dyadic regime;
8. крайние случаи `L=0`, малых `L`, плоской функции и `epsilon` около 1.

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
5. корректен ли зафиксированный cutoff `c0=1/6`;
6. не расширяется ли statement случайно с `A_fine` на весь `X`;
7. достаточно ли широк model class для change-of-measure alternatives;
8. корректно ли определены `delta in (0,1/2)`, `delta`-correctness и stopping model.

## 3. Каноническая процедура

→ [VS-Certify-Delayed](ALGORITHM.md)  
→ [Algorithm → proof obligation map](theory/ALGORITHM_PROOF_MAP.md)

Перед theorem review отдельно проверить, что pseudocode определяет одну исполнимую процедуру.

Особенно атаковать:

1. не используется ли одно обозначение для двух разных объектов;
2. различены ли generated designated sources (m_I) и finalized observations (n_I);
3. завершается ли каждый inner loop при фиксированном checkpoint target;
4. определено ли состояние resolved cell и сохраняется ли ее radius после resolution;
5. не наследуются ли samples между разными parent/child centers без отдельного доказательства;
6. возвращает ли `NOT_CERTIFIED` полный accounting/source ownership;
7. отделена ли statistical family certification от downstream GADU commit;
8. совпадает ли within-family core, анализируемый upper theorem, с тем state update, который реально использует delayed controller;
9. корректно ли считается incomplete checkpoint при hard cutoff;
10. имеет ли algorithm legal behavior для всех заявленных input assumptions.

## 4. Связь с delayed GADU

→ [Delayed execution + GADU composition](theory/DELAYED_GADU.md)

Ключевые вопросы:

- каждый ли calendar round имеет legal deployment;
- корректны ли `w=0` и timing source с delay ровно `w`;
- unresolved feedback нигде не считается нулем, включая hard cutoff;
- заморожен ли active set во время flush;
- clean ли ownership данных при fallback, включая later arrivals;
- корректно ли переводится scaled certificate обратно в latent scale;
- использует ли continuation gate именно latent deployment error.

## Удобный формат результата

| Блок | Вердикт | Где проблема, если есть |
|---|---|---|
| Canonical algorithm | PASS / FIX / BLOCK | ... |
| Upper theorem | PASS / FIX / BLOCK | ... |
| Lower theorem | PASS / FIX / BLOCK | ... |
| Delayed/GADU bridge | PASS / FIX / BLOCK | ... |

Самый ценный результат ревью — конкретный контрпример или точный шаг, который нельзя доказать.
