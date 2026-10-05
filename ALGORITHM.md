# VS-Certify-Delayed — каноническая процедура

Это текущая исполнимая версия variance-sensitive certification backend.

Цель этого файла — дать **один формально определенный алгоритм**, который можно проверить построчно: все обозначения ниже имеют одну роль, состояние каждой cell определено явно, а связь с upper theorem вынесена отдельно.

## 1. Model and fixed quantities

Families индексируются \(i=1,\ldots,K\), их domains:

\[
X_i=[0,1]^{d_i}.
\]

Для каждой family известен валидный положительный latent Lipschitz bound \(L_i>0\). Он может быть строгим upper bound на истинную Lipschitz constant; минимальность не требуется.

Фиксируем:

- attribution window \(w\in\mathbb Z_{\ge0}\);
- общий известный \(q_w=F(w)>0\);
- certification risk \(\delta_{\rm cert}\);
- hard calendar cutoff \(B\);
- per-family risks \(\delta_i>0\) с
  \[
  \sum_i\delta_i\le\delta_{\rm cert}.
  \]

Чтобы не смешивать Lipschitz constants и confidence bounds, используем отдельное обозначение

\[
\mathcal L_i^g:=q_w L_i.
\]

Для dyadic depth \(h\),

\[
\rho_h:=2^{-h-1},
\qquad
a_{i,h}:=\min\{1,\mathcal L_i^g\rho_h\}.
\]

Checkpoint targets:

\[
n_r:=2^{r+1},
\qquad r=0,1,2,\ldots.
\]

Для каждой возможной level-\(h\) cell \(I\) family \(i\) и checkpoint \(r\) заранее выделяется

\[
\eta_{i,h,I,r}
=
\frac{36\delta_i}
{\pi^4\,2^{d_i h}(h+1)^2(r+1)^2}.
\]

Для \(n\ge2\) finalized designated Bernoulli samples определим

\[
\operatorname{rad}(n,V,\eta)
=
\sqrt{\frac{2V\log(6/\eta)}{n}}
+
\frac{7\log(6/\eta)}{3(n-1)}.
\]

## 2. State

Для family \(i\) на depth \(h\) хранится active set

\[
\mathcal C_i(h).
\]

Для каждой active cell \(I\in\mathcal C_i(h)\) с center \(c_I\) хранятся:

- generated designated-source count \(m_I\);
- finalized designated count \(n_I\);
- finalized designated observations \(B_s^{(w)}\), пришедшие именно из deployments в \(c_I\);
- empirical mean \(\widehat g_I\);
- sample variance \(V_I\);
- stored confidence radius \(\operatorname{rad}_I\);
- Boolean flag `resolved`.

Когда cell впервые становится resolved на текущем depth, сохраняются \(\widehat g_I\), \(V_I\), \(\operatorname{rad}_I\) и checkpoint index \(r_I^\star\). Эти значения больше не меняются до prune/split этого level.

**Samples не наследуются между разными centers.** После split каждый child получает новый estimator:

\[
m_J=n_J=0,\qquad \texttt{resolved}(J)=\texttt{false}.
\]

Это консервативная версия алгоритма; reuse samples между parent/child здесь не предполагается.

Глобально хранятся:

- calendar time \(t\);
- complete certification-owned source set \(\mathcal S_{\rm cert}\).

## 3. Output contract

Алгоритм возвращает либо

\[
\textsc{Certified}
\bigl(i,\{z_j,\ell_j,U_j,\Xi_j\}_{j=1}^K,\mathsf{Acct}\bigr),
\]

либо

\[
\textsc{Not-Certified}(\mathsf{Acct}).
\]

Accounting record \(\mathsf{Acct}\) в обоих случаях содержит как минимум:

- consumed calendar time \(t\);
- declared failure budget \(\delta_{\rm cert}\);
- complete owned-source set \(\mathcal S_{\rm cert}\).

`CERTIFIED` здесь означает **статистически сертифицированную лучшую family**. Это ещё не означает автоматический GADU commit: внешний continuation/fallback gate проверяется отдельно.

## 4. Canonical procedure

Готовый reader-facing LaTeX алгоритм вынесен отдельно:

→ [`VS_CERTIFY_DELAYED_ALGORITHM.tex`](theory/VS_CERTIFY_DELAYED_ALGORITHM.tex)

Это короткий **Algorithm 1 для основного текста статьи**: только основной flow, без визуальной перегрузки.

Детальные процедуры вынесены рядом:

→ [`VS_CERTIFY_DELAYED_SUBROUTINES.tex`](theory/VS_CERTIFY_DELAYED_SUBROUTINES.tex)

В manuscript их можно подключать отдельно через `\input{...}`.  
Используется `algorithm + algpseudocode`.

Нужные packages:

```latex
\usepackage{amsmath,amssymb}
\usepackage{algorithm}
\usepackage{algpseudocode}
```

Если убрать LaTeX-синтаксис, процедура выглядит так:

```text
initialize one active dyadic cell per family

repeat:
    for each unresolved active center:
        add designated pulls up to the next geometric checkpoint

    freeze the active sets
    make exactly w legal filler deployments

    finalize all designated outcomes that have matured
    update empirical-Bernstein confidence intervals

    for each family:
        build cell lower/upper bounds
        build family lower/upper bounds
        choose the current recommendation

    if one family lower bound is above every competing upper bound:
        return CERTIFIED with the full family certificate bundle

    prune cells that can no longer contain a family maximizer
    split every surviving cell
    continue at the next dyadic depth

if the calendar cutoff is exhausted at any point:
    return NOT_CERTIFIED with full accounting
```

Так основной Algorithm 1 остается коротким и читаемым, а вся формальная детализация живет в отдельных subroutines и не забивает основной текст статьи.

## 5. Round chronology

A designated source created in round \(s\) is **not** used immediately.

After the last designated source of a checkpoint, the algorithm emits exactly \(w\) legal filler deployments while the active sets are frozen.

The checkpoint update happens only after this flush. Under the paper's timing convention, a source with delay exactly \(w\) is visible at that update. Hence every designated source included in the checkpoint can be finalized as

\[
B_s^{(w)}
=
\mathbf 1\{Z_s=1,D_s\le w\}.
\]

Before that update, unresolved silence is never treated as zero.

If the cutoff \(B\) is hit in the middle of designated sampling or a flush, the algorithm returns `NOT_CERTIFIED` with full accounting; it does not finalize incomplete sources as zeros.

## 6. Why pruning is safe

On the simultaneous confidence event,

\[
\mathrm{LCB}(I)
\le
g_i(c_I).
\]

By Lipschitzness,

\[
\sup_{x\in I}g_i(x)
\le
U_{\rm cell}(I).
\]

Therefore, if

\[
U_{\rm cell}(I)
<
\underline M_i^g,
\]

cell \(I\) cannot contain a maximizer of family \(i\).

At least one active cell survives in every family because the cell attaining \(\underline M_i^g\) has

\[
U_{\rm cell}(I)\ge\mathrm{LCB}(I)=\underline M_i^g.
\]

## 7. Why family certification is correct

For every family,

\[
\underline M_i^g
\le
g_i^\star
\le
\overline M_i^g.
\]

Hence

\[
\underline M_i^g
>
\max_{j\ne i}\overline M_j^g
\]

implies

\[
g_i^\star>g_j^\star
\qquad
\forall j\ne i.
\]

Because \(g_i=q_wf_i\) with the same \(q_w>0\) for every family, the same family is uniquely best in the latent problem.

For every family \(j\), the returned bundle satisfies

\[
\ell_j
\le
f_j(z_j)
\le
f_j^\star
\le
U_j,
\qquad
0\le f_j^\star-f_j(z_j)\le\Xi_j.
\]

The named index \(i\) is the family whose strict separation condition fired.

## 8. Relation to the upper theorem

The upper theorem and the multi-family delayed controller are **not the same stopping rule**.

The theorem analyzes the **single-family within-family core** in the direct Bernoulli oracle model:

1. use the same dyadic cells;
2. use the same empirical-Bernstein resolution rule;
3. use the same safe pruning rule;
4. continue until the first resolved depth \(h\) such that
   \[
   a_h\le\frac{2\varepsilon}{5};
   \]
5. return the center \(z\) attaining the largest LCB and
   \[
   \xi=\min\{1,U^g-\ell^g\}.
   \]

At that stopping depth,

\[
g^\star-g(z)\le\xi\le\varepsilon.
\]

`VS-Certify-Delayed` uses exactly this within-family state update for every family, but it may stop **earlier** when strict family separation is already available.

Thus:

- the upper theorem controls designated Bernoulli sample complexity of the within-family core;
- the delayed controller adds multi-family stopping and calendar execution;
- the calendar proposition adds the \(w\)-round flush overhead.

## 9. Calendar accounting

Let:

- \(D\) be the total number of designated source pulls;
- \(C_h\) be the number of **completed** synchronized checkpoints at depth \(h\).

Before hard-cutoff truncation,

\[
T_{\rm cal}
=
D+w\sum_h C_h.
\]

If the cutoff interrupts a checkpoint, the procedure returns `NOT_CERTIFIED`; that incomplete checkpoint is not counted as completed.

## 10. Integration boundary

`CERTIFIED` is the output of the statistical primitive.

GADU commits only if the separate downstream gate accepts the returned latent certificate, using actual calendar time and \(\Xi_i\). If the gate rejects—or if the primitive returns `NOT_CERTIFIED`—a clean fallback may be started using the accounting record to exclude every certification-owned source round and any later arrival tagged to it.

## 11. Current scope

This algorithm assumes a fixed common known \(q_w>0\).

It does **not** by itself claim:

- uniform superiority over Hoeffding;
- optimality of the checkpoint schedule;
- novelty of the \(q_w^{-1}\) factor;
- automatic replacement of current GADU Theorem 1/8 or Theorem 9;
- end-to-end superiority on real data.

## 12. Related files

- [Algorithm → proof obligation map](theory/ALGORITHM_PROOF_MAP.md)
- [Upper theorem](theory/UPPER_THEOREM.md)
- [Upper proof outline](theory/UPPER_PROOF.md)
- [Lower theorem](theory/LOWER_THEOREM.md)
- [Lower proof outline](theory/LOWER_PROOF.md)
- [Delayed execution + GADU composition](theory/DELAYED_GADU.md)
- [Mathematical review checklist](MATH_REVIEW.md)
