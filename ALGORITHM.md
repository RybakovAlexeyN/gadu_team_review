# VS-Certify-Delayed — каноническая процедура

Это текущая исполнимая версия variance-sensitive certification backend.

Цель этого файла — дать **один формально определенный алгоритм**, который можно проверить построчно: все обозначения ниже имеют одну роль, состояние каждой cell определено явно, а связь с upper theorem вынесена отдельно.

## 1. Model and fixed quantities

Families индексируются \(i=1,\ldots,K\), их domains:

\[
X_i=[0,1]^{d_i}.
\]

Для каждой family известен latent Lipschitz bound \(L_i\).

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
(i,z_i,\ell_i,U_i,\Xi_i,\mathsf{Acct}),
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

## 4. Canonical pseudocode

```latex
\begin{algorithm}[t]
\caption{\textsc{VS-Certify-Delayed}}
\label{alg:vs-certify-delayed}
\begin{algorithmic}[1]
\REQUIRE Families \(i=1,\ldots,K\), domains \(X_i=[0,1]^{d_i}\),
         latent Lipschitz bounds \(L_i\), common known \(q_w>0\),
         window \(w\in\mathbb Z_{\ge0}\), risks \((\delta_i)_i\)
         with \(\sum_i\delta_i\le\delta_{\rm cert}\), cutoff \(B\).
\ENSURE \textsc{Certified}\((i,z_i,\ell_i,U_i,\Xi_i,\mathsf{Acct})\)
        or \textsc{Not-Certified}\((\mathsf{Acct})\).

\STATE \(t\leftarrow0\), \(h\leftarrow0\),
       \(\mathcal S_{\rm cert}\leftarrow\varnothing\).
\FOR{each family \(i\)}
    \STATE \(\mathcal L_i^g\leftarrow q_wL_i\);
           initialize \(\mathcal C_i(0)=\{X_i\}\) with fresh cell state.
\ENDFOR

\WHILE{true}
    \STATE \(\rho_h\leftarrow2^{-h-1}\);
           \(a_{i,h}\leftarrow\min\{1,\mathcal L_i^g\rho_h\}\).
    \STATE Mark every \(I\in\mathcal C_i(h)\) unresolved and set \(r\leftarrow0\).

    \WHILE{some active cell is unresolved}
        \STATE \(n_r\leftarrow2^{r+1}\).

        \FOR{unresolved active cells in a fixed round-robin order}
            \WHILE{\(m_I<n_r\)}
                \IF{\(t=B\)}
                    \STATE Build \(\mathsf{Acct}\) from
                           \(t,\delta_{\rm cert},\mathcal S_{\rm cert}\).
                    \RETURN \textsc{Not-Certified}\((\mathsf{Acct})\).
                \ENDIF
                \STATE Deploy \((i,c_I)\) as a designated source at round \(t+1\).
                \STATE Tag round \(t+1\) as certification-owned,
                       add it to \(\mathcal S_{\rm cert}\), increment
                       \(m_I\leftarrow m_I+1\), and set \(t\leftarrow t+1\).
            \ENDWHILE
        \ENDFOR

        \STATE Freeze all active sets during the flush.
        \FOR{\(u=1,\ldots,w\)}
            \IF{\(t=B\)}
                \STATE Build \(\mathsf{Acct}\) from
                       \(t,\delta_{\rm cert},\mathcal S_{\rm cert}\).
                \RETURN \textsc{Not-Certified}\((\mathsf{Acct})\).
            \ENDIF
            \STATE Deploy the center of the first active cell under a fixed
                   deterministic order as a legal filler.
            \STATE Tag the filler source round as certification-owned,
                   exclude its feedback from designated estimators,
                   add it to \(\mathcal S_{\rm cert}\),
                   and set \(t\leftarrow t+1\).
        \ENDFOR

        \STATE Finalize every newly generated designated source since the previous
               checkpoint update as
               \(B_s^{(w)}=\mathbf 1\{Z_s=1,D_s\le w\}\).
        \FOR{each still-unresolved active cell \(I\)}
            \STATE Set \(n_I\leftarrow m_I\) and recompute
                   \(\widehat g_I,V_I\) from finalized
                   designated observations generated at \(c_I\).
            \STATE
            \(\operatorname{rad}_I\leftarrow
              \operatorname{rad}
              (n_I,V_I,\eta_{i,h,I,r})\).
            \IF{\(\operatorname{rad}_I\le a_{i,h}/8\)}
                \STATE Mark \(I\) resolved and store
                       \((\widehat g_I,V_I,\operatorname{rad}_I,r_I^\star=r)\).
            \ENDIF
        \ENDFOR
        \STATE \(r\leftarrow r+1\).
    \ENDWHILE

    \FOR{each family \(i\)}
        \FOR{each \(I\in\mathcal C_i(h)\)}
            \STATE
            \(\mathrm{LCB}(I)\leftarrow
              \max\{0,\widehat g_I-\operatorname{rad}_I\}\).
            \STATE
            \(U_{\rm cell}(I)\leftarrow
              \min\{1,\widehat g_I+\operatorname{rad}_I+a_{i,h}\}\).
        \ENDFOR
        \STATE
        \(\underline M_i^g\leftarrow
          \max_{I\in\mathcal C_i(h)}\mathrm{LCB}(I)\).
        \STATE
        \(\overline M_i^g\leftarrow
          \max_{I\in\mathcal C_i(h)}U_{\rm cell}(I)\).
        \STATE Choose
        \(I_i^L\in\arg\max_{I\in\mathcal C_i(h)}\mathrm{LCB}(I)\)
        using fixed tie-breaking; set \(z_i\leftarrow c_{I_i^L}\).
        \STATE
        \(\xi_i^g\leftarrow
          \min\{1,\overline M_i^g-\underline M_i^g\}\).
    \ENDFOR

    \IF{there exists \(i\) such that
         \(\underline M_i^g>\max_{j\ne i}\overline M_j^g\)}
        \STATE
        \(\ell_i\leftarrow\max\{0,\underline M_i^g/q_w\}\),
        \(U_i\leftarrow\min\{1,\overline M_i^g/q_w\}\),
        \(\Xi_i\leftarrow\min\{1,\xi_i^g/q_w\}\).
        \STATE Build \(\mathsf{Acct}\) from
               \(t,\delta_{\rm cert},\mathcal S_{\rm cert}\).
        \RETURN \textsc{Certified}
        \((i,z_i,\ell_i,U_i,\Xi_i,\mathsf{Acct})\).
    \ENDIF

    \FOR{each family \(i\)}
        \STATE
        \(\mathcal S_i\leftarrow
          \{I\in\mathcal C_i(h):
          U_{\rm cell}(I)\ge\underline M_i^g\}\).
        \STATE Set \(\mathcal C_i(h+1)\) to all dyadic children of
               cells in \(\mathcal S_i\), each with fresh estimator state.
    \ENDFOR
    \STATE \(h\leftarrow h+1\).
\ENDWHILE
\end{algorithmic}
\end{algorithm}
```

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

The returned quantities satisfy

\[
\ell_i
\le
f_i(z_i)
\le
f_i^\star
\le
U_i,
\qquad
0\le f_i^\star-f_i(z_i)\le\Xi_i.
\]

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

- [Upper theorem](theory/UPPER_THEOREM.md)
- [Upper proof outline](theory/UPPER_PROOF.md)
- [Lower theorem](theory/LOWER_THEOREM.md)
- [Lower proof outline](theory/LOWER_PROOF.md)
- [Delayed execution + GADU composition](theory/DELAYED_GADU.md)
- [Mathematical review checklist](MATH_REVIEW.md)
