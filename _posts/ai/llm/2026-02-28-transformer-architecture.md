---
title: "Transformer 아키텍처 핵심 정리"
excerpt: "Attention Is All You Need 이후 모든 LLM의 기반이 된 Transformer 구조를 정리한다."

categories:
  - AI
  - LLM
tags:
  - Transformer
  - Attention
  - LLM

feature: true
toc: true
last_modified_at: 2026-02-28
---

## Transformer란?

2017년 Google이 "Attention Is All You Need" 논문에서 제안한 아키텍처로, RNN/LSTM 없이 **Self-Attention만으로** 시퀀스를 처리한다. 현재 GPT, BERT, LLaMA 등 모든 LLM의 기반이다.

## Self-Attention 메커니즘

입력 시퀀스의 각 토큰이 다른 모든 토큰과의 관계를 동시에 계산한다.

$$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$$

- **Q (Query)**: "나는 어떤 정보를 찾고 있는가"
- **K (Key)**: "나는 어떤 정보를 가지고 있는가"
- **V (Value)**: "실제 전달할 정보"

$\sqrt{d_k}$로 나누는 이유: 차원이 클수록 내적 값이 커져서 softmax가 극단적으로 치우치는 것을 방지한다.

## Multi-Head Attention

하나의 attention보다 여러 개의 "head"에서 서로 다른 관점으로 attention을 수행한다.

$$\text{MultiHead}(Q, K, V) = \text{Concat}(\text{head}_1, \dots, \text{head}_h)W^O$$

각 head는 서로 다른 projection matrix를 사용하므로, 문법적 관계, 의미적 관계 등 다양한 패턴을 동시에 포착할 수 있다.

## Positional Encoding

Self-Attention은 순서 정보가 없으므로, 위치 정보를 별도로 주입한다.

$$PE_{(pos, 2i)} = \sin\left(\frac{pos}{10000^{2i/d_{model}}}\right)$$

$$PE_{(pos, 2i+1)} = \cos\left(\frac{pos}{10000^{2i/d_{model}}}\right)$$

## Encoder-Decoder vs Decoder-Only

| 구조 | 대표 모델 | 용도 |
|------|-----------|------|
| Encoder-Only | BERT | 분류, NLU |
| Decoder-Only | GPT, LLaMA | 생성, 범용 |
| Encoder-Decoder | T5, BART | 번역, 요약 |

현재 LLM의 대세는 **Decoder-Only** 구조이다.

## 마무리

Transformer는 병렬 처리 가능성과 long-range dependency 포착 능력 덕분에 NLP를 넘어 Vision, Audio, RL 등 거의 모든 분야로 확장되었다.
