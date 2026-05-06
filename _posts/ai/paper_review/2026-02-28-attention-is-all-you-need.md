---
title: "[논문 리뷰] Attention Is All You Need"
excerpt: "Transformer를 처음 제안한 Vaswani et al. (2017) 논문을 리뷰한다."

categories:
  - AI
  - Paper-Review
tags:
  - Paper Review
  - Transformer
  - NLP

feature: true
toc: true
last_modified_at: 2026-02-28
published: false
sitemap: false
---

## 논문 정보

- **제목**: Attention Is All You Need
- **저자**: Vaswani, Shazeer, Parmar, Uszkoreit, Jones, Gomez, Kaiser, Polosukhin
- **학회**: NeurIPS 2017
- **핵심 기여**: RNN/CNN 없이 Self-Attention만으로 시퀀스 변환 모델 구축

## 동기 (Motivation)

기존 시퀀스 모델(RNN, LSTM)의 근본적 한계:

1. **순차적 계산** — 병렬화 불가, 학습 속도 느림
2. **Long-range dependency** — 거리가 먼 토큰 간 관계 포착 어려움
3. **메모리 병목** — hidden state에 모든 정보를 압축

저자들은 "attention만으로 충분하지 않을까?"라는 질문에서 출발했다.

## 핵심 구조

### Scaled Dot-Product Attention

$$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$$

### Multi-Head Attention

서로 다른 $h$개의 linear projection으로 Q, K, V를 변환한 뒤 각각 attention을 수행하고 결합한다. 논문에서는 $h=8$, $d_k = d_v = d_{model}/h = 64$를 사용했다.

### Feed-Forward Network

각 position마다 독립적으로 적용되는 2-layer MLP:

$$\text{FFN}(x) = \max(0, xW_1 + b_1)W_2 + b_2$$

### Positional Encoding

위치 정보를 sin/cos 함수로 인코딩하여 입력에 더한다.

## 실험 결과

WMT 2014 영-독 번역 태스크에서:

| 모델 | BLEU | 학습 비용 (FLOPs) |
|------|------|-------------------|
| GNMT + RL | 26.30 | $2.3 \times 10^{19}$ |
| Transformer (base) | 27.3 | $3.3 \times 10^{18}$ |
| Transformer (big) | **28.4** | $2.3 \times 10^{19}$ |

**더 적은 연산량으로 더 높은 성능**을 달성했다.

## 이 논문이 중요한 이유

이 논문 이후 NLP의 패러다임이 완전히 바뀌었다:

- **BERT** (2018): Encoder-only Transformer → NLU 혁명
- **GPT 시리즈** (2018~): Decoder-only Transformer → 생성 모델의 시작
- **LLaMA, Claude, GPT-4**: 현재 모든 LLM의 기반

인용 수 13만+ (2026년 기준). 딥러닝 역사에서 가장 영향력 있는 논문 중 하나다.

## 개인적 생각

이 논문의 가장 큰 통찰은 "recurrence를 제거하고 attention만 남겨도 된다"는 것이다. 이후 RL에서도 Decision Transformer처럼 시퀀스 모델링 관점에서 RL 문제를 푸는 접근이 등장했는데, 이는 이 논문의 직접적인 영향이다.
