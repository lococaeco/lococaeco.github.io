---
title: "Batch Normalization의 원리와 효과"
excerpt: "딥러닝 학습을 안정화시키는 핵심 기법인 Batch Normalization을 정리한다."

categories:
  - AI
  - Deep-Learning
tags:
  - Deep Learning
  - Optimization
  - BatchNorm

toc: true
last_modified_at: 2026-02-28
---

## Internal Covariate Shift 문제

딥러닝에서 각 레이어의 입력 분포가 학습 과정에서 계속 변한다. 이전 레이어의 파라미터가 업데이트되면 현재 레이어가 받는 입력의 분포도 바뀌기 때문이다. 이를 **Internal Covariate Shift**라 하고, Batch Normalization은 이 문제를 해결하기 위해 제안되었다.

## Batch Normalization 수식

미니배치 $\mathcal{B} = \{x_1, \dots, x_m\}$에 대해:

$$\hat{x}_i = \frac{x_i - \mu_\mathcal{B}}{\sqrt{\sigma^2_\mathcal{B} + \epsilon}}$$

$$y_i = \gamma \hat{x}_i + \beta$$

- $\mu_\mathcal{B}$, $\sigma^2_\mathcal{B}$: 미니배치의 평균과 분산
- $\gamma$, $\beta$: 학습 가능한 파라미터 (scale & shift)
- $\epsilon$: 수치 안정성을 위한 작은 값

$\gamma$와 $\beta$가 있는 이유: 단순 정규화만 하면 네트워크의 표현력이 제한되므로, 필요하면 원래 분포로 복원할 수 있게 한다.

## 왜 효과적인가?

1. **더 높은 learning rate 사용 가능** — 그래디언트 스케일이 안정적
2. **초기화에 덜 민감** — 입력이 정규화되므로
3. **정규화 효과** — 미니배치 통계를 사용하므로 약간의 노이즈가 생김

## 추론(Inference) 시 주의점

학습 시에는 미니배치 통계를 사용하지만, 추론 시에는 **학습 중 누적된 running mean/variance**를 사용한다.

```python
# PyTorch에서는 자동으로 처리
model.train()   # 미니배치 통계 사용
model.eval()    # running 통계 사용
```

## BatchNorm의 변형

| 이름 | 정규화 축 | 사용 분야 |
|------|-----------|-----------|
| Batch Norm | 배치 | CNN, MLP |
| Layer Norm | 피처 | Transformer, RNN |
| Instance Norm | 공간 | Style Transfer |
| Group Norm | 그룹 | 작은 배치 |

Transformer에서는 **Layer Normalization**이 표준이다. 배치 크기에 의존하지 않기 때문이다.