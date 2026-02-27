---
title: "PPO 알고리즘 핵심 정리"
excerpt: "Proximal Policy Optimization의 핵심 아이디어와 구현 포인트를 정리한다."

categories:
  - AI
  - Reinforcement Learning
tags:
  - RL
  - PPO
  - Policy Gradient

feature: true
toc: true
last_modified_at: 2026-02-28
---

## PPO란?

**Proximal Policy Optimization (PPO)**은 OpenAI에서 제안한 policy gradient 계열 알고리즘으로, TRPO의 복잡한 constraint를 간단한 clipping으로 대체하여 구현이 쉬우면서도 안정적인 학습을 가능하게 한다.

## 핵심 아이디어: Clipped Surrogate Objective

기존 policy gradient의 문제는 한 번의 업데이트에서 정책이 너무 크게 변할 수 있다는 것이다. PPO는 이를 **clipping**으로 해결한다.

$$L^{CLIP}(\theta) = \hat{\mathbb{E}}_t \left[ \min \left( r_t(\theta) \hat{A}_t, \; \text{clip}(r_t(\theta), 1 - \epsilon, 1 + \epsilon) \hat{A}_t \right) \right]$$

여기서 $r_t(\theta) = \frac{\pi_\theta(a_t \mid s_t)}{\pi_{\theta_{old}}(a_t \mid s_t)}$ 는 probability ratio이고, $\epsilon$은 보통 0.2를 사용한다.

## Clipping의 직관

- $\hat{A}_t > 0$ (좋은 행동): ratio가 $1 + \epsilon$을 넘으면 더 이상 보상하지 않음
- $\hat{A}_t < 0$ (나쁜 행동): ratio가 $1 - \epsilon$ 아래로 내려가면 더 이상 벌하지 않음

이렇게 하면 정책이 급격하게 변하는 것을 방지하면서도, 좋은 방향으로의 점진적 개선은 허용한다.

## PyTorch 구현 핵심

```python
def ppo_loss(old_log_probs, new_log_probs, advantages, epsilon=0.2):
    ratio = torch.exp(new_log_probs - old_log_probs)
    clipped_ratio = torch.clamp(ratio, 1 - epsilon, 1 + epsilon)
    loss = -torch.min(ratio * advantages, clipped_ratio * advantages).mean()
    return loss
```

## TRPO vs PPO 비교

| 항목 | TRPO | PPO |
|------|------|-----|
| Constraint | KL divergence | Clipping |
| 구현 난이도 | 높음 (conjugate gradient) | 낮음 |
| 성능 | 안정적 | 안정적 + 빠름 |
| 실무 사용 | 드묾 | 매우 많음 |

## 마무리

PPO는 구현의 단순함과 성능의 안정성 덕분에 RL 연구와 실무에서 가장 널리 사용되는 알고리즘 중 하나다. RLHF에서 LLM을 fine-tuning할 때도 PPO가 핵심적으로 사용된다.
