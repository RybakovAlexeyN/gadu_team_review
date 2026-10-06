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

## 4. Final procedure (LaTeX algorithmic)

Ниже — конечная reader-facing процедура, которую можно напрямую вставлять в manuscript как **Algorithm 1**.

Полный исходник также лежит отдельно:

→ [theory/VS_CERTIFY_DELAYED_ALGORITHM.tex](theory/VS_CERTIFY_DELAYED_ALGORITHM.tex)

Детальные helper procedures (\textsc{ResolveLevel} и \textsc{FamilyCertificate}) вынесены в:

→ [theory/VS_CERTIFY_DELAYED_SUBROUTINES.tex](theory/VS_CERTIFY_DELAYED_SUBROUTINES.tex)

Используем:

~~~latex
\usepackage{amsmath,amssymb}
\usepackage{algorithm}
\usepackage{algpseudocode}
~~~

~~~latex
\begin{algorithm}[t]
\caption{Delayed variance-sensitive family certification}
\label{alg:vs-certify-delayed}
\small
\begin{algorithmic}[1]
\Require
families $\{(X_i,L_i)\}_{i=1}^K$ with $X_i=[0,1]^{d_i}$;
known $q_w=F(w)>0$ and window $w$;
risks $\{\delta_i\}_{i=1}^K$ with
$\sum_i\delta_i\le\delta_{\rm cert}$;
calendar cutoff $B$
\Ensure
\textsc{Certified}$\bigl(i^\star,\{z_i,\ell_i,U_i,\Xi_i\}_{i=1}^K,\mathsf{Acct}\bigr)$
or \textsc{Not-Certified}$\bigl(\mathsf{Acct}\bigr)$

\State $t\gets0$, $h\gets0$, $\mathcal S_{\rm cert}\gets\varnothing$
\For{$i=1,\ldots,K$}
    \State $\mathcal L_i^g\gets q_wL_i$
    \State initialize $\mathcal C_i(0)\gets\{X_i\}$ with fresh root-cell state
\EndFor

\While{true}
    \If{$\Call{ResolveLevel}{h}=\textsc{Fail}$}
        \State \Return \textsc{Not-Certified}$\bigl(\mathsf{Acct}(t)\bigr)$
    \EndIf

    \For{$i=1,\ldots,K$}
        \State $(z_i,\underline M_i^g,\overline M_i^g,\xi_i^g)
        \gets \Call{FamilyCertificate}{i,h}$
    \EndFor

    \If{some $i$ satisfies
        $\underline M_i^g>\max_{j\ne i}\overline M_j^g$}
        \State let $i^\star$ be the first such family under the fixed order
        \For{$j=1,\ldots,K$}
            \State $\ell_j\gets\max\{0,\underline M_j^g/q_w\}$,
            $U_j\gets\min\{1,\overline M_j^g/q_w\}$
            \State $\Xi_j\gets\min\{1,\xi_j^g/q_w\}$
        \EndFor
        \State \Return \textsc{Certified}$\bigl(i^\star,
        \{z_j,\ell_j,U_j,\Xi_j\}_{j=1}^K,\mathsf{Acct}(t)\bigr)$
    \EndIf

    \For{$i=1,\ldots,K$}
        \State $\mathcal S_i\gets
        \{I\in\mathcal C_i(h):U_{\rm cell}(I)\ge\underline M_i^g\}$
        \State $\mathcal C_i(h+1)\gets$
        all dyadic children of cells in $\mathcal S_i$, each with fresh state
    \EndFor
    \State $h\gets h+1$
\EndWhile
\end{algorithmic}
\end{algorithm}
~~~

Смысл Algorithm 1 теперь читается сверху вниз как одна процедура:

~~~text
resolve current level
→ construct family certificates
→ certify if one family separates
→ otherwise prune and refine
→ repeat
~~~

Вся delayed-механика внутри \textsc{ResolveLevel} формально определена в appendix subroutine:
designated pulls → exactly \(w\) legal filler rounds → finalize matured outcomes → empirical-Bernstein update → resolve cells.

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
