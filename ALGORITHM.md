# VS-Certify-Delayed — каноническая процедура

Это текущая исполнимая версия variance-sensitive certification backend.

Ниже сначала дан **сам алгоритм целиком**, а уже после — короткое объяснение его блоков. Цель: чтобы процедуру можно было проверить построчно, не восстанавливая её из теорем и proof outline.

## Inputs / output

**Inputs**

- families (i=1,ldots,K) with domains (X_i=[0,1]^{d_i});
- known latent Lipschitz constants (L_i);
- fixed attribution window (w\in\mathbb Z_{\ge0});
- common known (q_w=F(w)>0);
- total certification risk (delta_{\rm cert});
- predeclared hard calendar cutoff (B).

Choose per-family risks (delta_i>0) such that

```text
sum_i delta_i <= delta_cert.
```

For dyadic depth (h),

```text
rho_h      = 2^(-h-1)
L_i^g      = q_w L_i
a_{i,h}    = min{1, L_i^g rho_h}
n_r        = 2^(r+1)
```

and for every possible level-(h) cell (I) of family (i) and checkpoint (r),

```text
eta_{i,h,I,r}
=
36 delta_i /
[pi^4 * 2^(d_i h) * (h+1)^2 * (r+1)^2].
```

For (n>=2) finalized designated samples,

```text
rad(n,V,eta)
=
sqrt(2 V log(6/eta)/n)
+
7 log(6/eta)/(3(n-1)).
```

**Output**

Either

```text
CERTIFIED(i, z_i, ell_i, U_i, Xi_i, accounting)
```

or

```text
NOT_CERTIFIED.
```

## Canonical pseudocode

LaTeX version used for the manuscript:

```latex
\begin{algorithm}[t]
\caption{\textsc{VS-Certify-Delayed}}
\label{alg:vs-certify-delayed}
\begin{algorithmic}[1]
\REQUIRE Families \(i=1,\ldots,K\), domains \(X_i=[0,1]^{d_i}\),
         Lipschitz bounds \(L_i\), common known \(q_w>0\),
         window \(w\in\mathbb Z_{\ge0}\),
         risks \((\delta_i)_i\) with
         \(\sum_i\delta_i\le\delta_{\rm cert}\),
         hard calendar cutoff \(B\).
\ENSURE \textsc{Certified}\((i,z_i,\ell_i,U_i,\Xi_i,\mathcal A)\)
        or \textsc{Not-Certified}.

\STATE \(t\leftarrow0\), \(h\leftarrow0\);
       \(\mathcal S_{\rm cert}\leftarrow\varnothing\).
\FOR{each family \(i\)}
    \STATE \(\mathcal A_i\leftarrow\{X_i\}\) and
           \(L_i^g\leftarrow q_w L_i\).
\ENDFOR

\WHILE{true}
    \STATE Set \(\rho_h\leftarrow2^{-h-1}\) and
           \(a_{i,h}\leftarrow\min\{1,L_i^g\rho_h\}\) for every \(i\).
    \STATE \(r\leftarrow0\).

    \WHILE{some active cell is not statistically resolved}
        \STATE \(n_r\leftarrow2^{r+1}\).

        \FOR{unresolved active centers in a fixed round-robin order}
            \WHILE{the designated count of center \(c_I\) is below \(n_r\)}
                \IF{another deployment would make \(t>B\)}
                    \RETURN \textsc{Not-Certified}.
                \ENDIF
                \STATE Deploy \((i,c_I)\) as a designated source;
                       tag source round \(t+1\) as certification-owned.
                \STATE Add the source round to \(\mathcal S_{\rm cert}\);
                       \(t\leftarrow t+1\).
            \ENDWHILE
        \ENDFOR

        \STATE Freeze the active sets for the flush.
        \FOR{\(u=1,\ldots,w\)}
            \IF{another deployment would make \(t>B\)}
                \RETURN \textsc{Not-Certified}.
            \ENDIF
            \STATE Deploy the center of the first active cell under a fixed
                   deterministic order as a filler action.
            \STATE Tag this source round as certification-owned, exclude its
                   feedback from designated estimators, and set \(t\leftarrow t+1\).
        \ENDFOR

        \STATE For every designated source generated before this flush, finalize
               \[
               B_s^{(w)}=\mathbf 1\{Z_s=1,\ D_s\le w\}.
               \]
        \STATE Recompute designated empirical means, sample variances, and
               \[
               r_n=
               \sqrt{\frac{2V_n\log(6/\eta_{i,h,I,r})}{n}}
               +
               \frac{7\log(6/\eta_{i,h,I,r})}{3(n-1)}.
               \]
        \STATE Mark cell \(I\) resolved when \(r_n\le a_{i,h}/8\).
        \STATE \(r\leftarrow r+1\).
    \ENDWHILE

    \FOR{each family \(i\)}
        \FOR{each active cell \(I\) with center \(c_I\)}
            \STATE
            \(\mathrm{LCB}(I)\leftarrow
              \max\{0,\widehat g(c_I)-r_I\}\).
            \STATE
            \(U_{\rm cell}(I)\leftarrow
              \min\{1,\widehat g(c_I)+r_I+a_{i,h}\}\).
        \ENDFOR
        \STATE
        \(L_i^g\leftarrow\max_{I\in\mathcal A_i}\mathrm{LCB}(I)\).
        \STATE
        \(U_i^g\leftarrow\max_{I\in\mathcal A_i}U_{\rm cell}(I)\).
        \STATE Choose
        \(I_i^L\in\arg\max_{I\in\mathcal A_i}\mathrm{LCB}(I)\),
        set \(z_i\leftarrow c_{I_i^L}\), and
        \(\xi_i^g\leftarrow\min\{1,U_i^g-L_i^g\}\).
    \ENDFOR

    \IF{there exists \(i\) with
         \(L_i^g>\max_{j\ne i}U_j^g\)}
        \STATE
        \(\ell_i\leftarrow\max\{0,L_i^g/q_w\}\),
        \(U_i\leftarrow\min\{1,U_i^g/q_w\}\),
        \(\Xi_i\leftarrow\min\{1,\xi_i^g/q_w\}\).
        \RETURN \textsc{Certified}
        \((i,z_i,\ell_i,U_i,\Xi_i,\mathcal A)\),
        where \(\mathcal A\) contains \(t\), the failure budget,
        and \(\mathcal S_{\rm cert}\).
    \ENDIF

    \FOR{each family \(i\)}
        \STATE Remove every active cell \(I\) satisfying
               \(U_{\rm cell}(I)<L_i^g\).
        \STATE Split every surviving cell into its dyadic children.
    \ENDFOR
    \STATE \(h\leftarrow h+1\).
\ENDWHILE
\end{algorithmic}
\end{algorithm}
```

## Что происходит в одном цикле

Если убрать техническую нотацию, один refinement cycle выглядит так:

```text
designated sampling
→ w legal filler rounds
→ finalize matured designated outcomes
→ empirical-Bernstein update
→ Lipschitz cell bounds
→ family-separation test
→ prune
→ split survivors
→ next level
```

То есть алгоритм не содержит неопределенного шага «подождать feedback».

После последнего designated source checkpoint он делает ровно (w) допустимых deployments. После этого все designated sources текущего checkpoint уже имеют возраст не меньше (w), поэтому для них можно вычислить

```text
B_s^(w) = 1{Z_s=1 and D_s<=w}.
```

До этого момента отсутствие события не кодируется как zero.

## Почему pruning безопасен

Для активной cell (I) с center (c_I),

```text
LCB(I) <= g_i(c_I)
```

и Lipschitz property дает

```text
sup_{x in I} g_i(x) <= U_cell(I).
```

Поэтому если

```text
U_cell(I) < L_i^g,
```

cell уже не может содержать maximizer своей family и может быть удалена.

На simultaneous confidence event cell с настоящим maximizer не удаляется.

## Почему family certification корректна

Для каждой family строятся

```text
L_i^g <= g_i^* <= U_i^g.
```

Если

```text
L_i^g > max_{j != i} U_j^g,
```

то

```text
g_i^* > g_j^*
```

для любого (j\ne i).

Поскольку

```text
g_i = q_w f_i
```

и один и тот же (q_w>0) используется для всех families, ordering сохраняется и в latent problem.

## Delayed execution и accounting

Filler feedback не используется в designated certification estimator.

Все source rounds certification phase — и designated, и filler — остаются source-tagged. Если после `NOT_CERTIFIED` запускается clean fallback, эти source rounds и их поздние arrivals не используются как fresh fallback data.

Если:

- (D) — число designated source pulls;
- (C_h) — число synchronized checkpoints на уровне (h);

то до hard-cutoff truncation

```text
T_cal = D + w * sum_h C_h.
```

## Что именно является текущим claim

Этот алгоритм — executable certification backend при фиксированном общем известном (q_w>0).

Он не означает автоматически, что:

- backend всегда лучше Hoeffding;
- checkpoint schedule оптимален;
- (q_w^{-1}) сам по себе является новой закономерностью;
- текущие GADU Theorem 1/8 или Theorem 9 автоматически заменяются;
- доказана end-to-end superiority на реальных данных.

## Связанная математика

- [Upper theorem](theory/UPPER_THEOREM.md)
- [Upper proof outline](theory/UPPER_PROOF.md)
- [Lower theorem](theory/LOWER_THEOREM.md)
- [Lower proof outline](theory/LOWER_PROOF.md)
- [Delayed execution + GADU composition](theory/DELAYED_GADU.md)
- [Mathematical review checklist](MATH_REVIEW.md)
