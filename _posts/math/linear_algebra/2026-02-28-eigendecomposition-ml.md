---
title: "고유값 분해와 머신러닝에서의 활용"
excerpt: "Eigendecomposition의 수학적 정의와 ML에서 어떻게 활용되는지 정리한다."

categories:
  - Math
  - Linear Algebra
tags:
  - Linear Algebra
  - Eigenvalue
  - PCA

toc: true
last_modified_at: 2026-02-28
---

## 고유값과 고유벡터

정방행렬 $A$에 대해 다음을 만족하는 스칼라 $\lambda$와 벡터 $\mathbf{v}$를 각각 **고유값(eigenvalue)**과 **고유벡터(eigenvector)**라 한다:

$$A\mathbf{v} = \lambda\mathbf{v}$$

직관적으로, 행렬 $A$를 곱해도 **방향이 변하지 않고 크기만 $\lambda$배 변하는** 벡터가 고유벡터이다.

## 고유값 분해 (Eigendecomposition)

$n \times n$ 행렬 $A$가 $n$개의 선형 독립인 고유벡터를 가지면:

$$A = V \Lambda V^{-1}$$

- $V$: 고유벡터를 열로 나열한 행렬
- $\Lambda$: 고유값을 대각에 나열한 대각행렬

**대칭 행렬**의 경우 $V$가 직교 행렬이므로:

$$A = V \Lambda V^T$$

## ML에서의 활용

### 1. PCA (주성분 분석)

데이터의 공분산 행렬 $C = \frac{1}{n}X^TX$에 대해 고유값 분해를 수행하면:
- **고유벡터** = 데이터의 주성분 (분산이 최대인 방향)
- **고유값** = 해당 방향의 분산 크기

고유값이 큰 순서대로 $k$개의 고유벡터만 선택하면 **차원 축소**가 된다.

### 2. Spectral Clustering

그래프의 Laplacian 행렬의 고유벡터를 이용해 클러스터링을 수행한다.

### 3. 학습 안정성 분석

Hessian 행렬의 고유값 분포를 통해 loss landscape의 곡률을 분석할 수 있다:
- 고유값이 모두 양수 → 극소점
- 음의 고유값 존재 → 안장점(saddle point)

## NumPy로 계산

```python
import numpy as np

A = np.array([[4, 2], [1, 3]])
eigenvalues, eigenvectors = np.linalg.eig(A)

print(f"고유값: {eigenvalues}")        # [5. 2.]
print(f"고유벡터:\n{eigenvectors}")     # 각 열이 고유벡터
```

## SVD와의 관계

**특이값 분해 (SVD)**: $A = U \Sigma V^T$

- $A^TA$의 고유값 분해 → $V$와 $\Sigma^2$를 얻음
- $AA^T$의 고유값 분해 → $U$와 $\Sigma^2$를 얻음

SVD는 직사각 행렬에도 적용 가능하므로, 실무에서는 고유값 분해보다 SVD가 더 자주 사용된다.
