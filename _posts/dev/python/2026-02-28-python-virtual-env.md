---
title: "Python 가상환경 관리: conda vs venv"
excerpt: "ML 연구에서 Python 가상환경을 효율적으로 관리하는 방법을 비교한다."

categories:
  - Dev
  - Python
tags:
  - Python
  - conda
  - venv

toc: true
last_modified_at: 2026-02-28
---

## 왜 가상환경이 필요한가?

ML 연구에서 프로젝트마다 다른 버전의 PyTorch, CUDA, 라이브러리를 사용하는 것은 흔하다. 가상환경 없이 시스템 Python에 모든 것을 설치하면 **의존성 충돌**이 발생한다.

## venv (Python 내장)

```bash
# 생성
python -m venv myenv

# 활성화
source myenv/bin/activate  # Linux/Mac
myenv\Scripts\activate     # Windows

# 패키지 설치
pip install torch numpy

# 비활성화
deactivate
```

**장점**: Python 내장, 가볍고 빠름
**단점**: Python 버전 자체를 바꿀 수 없음, CUDA 관리 불가

## conda (Anaconda/Miniconda)

```bash
# 생성 (Python 버전 지정 가능)
conda create -n myenv python=3.11

# 활성화
conda activate myenv

# 패키지 설치 (CUDA 포함 가능)
conda install pytorch torchvision pytorch-cuda=12.1 -c pytorch -c nvidia

# 비활성화
conda deactivate
```

**장점**: Python 버전 관리, CUDA toolkit 포함 설치, 바이너리 패키지 관리
**단점**: 느림, 용량 큼, resolver 충돌 가능

## 비교 정리

| 항목 | venv | conda |
|------|------|-------|
| Python 버전 관리 | X | O |
| CUDA 관리 | X | O |
| 속도 | 빠름 | 느림 |
| 용량 | 작음 | 큼 |
| ML 연구 적합성 | 보통 | 높음 |

## 실전 팁

ML 연구에서는 **conda로 환경을 만들되, pip로 패키지를 설치**하는 하이브리드 방식이 가장 실용적이다:

```bash
conda create -n research python=3.11
conda activate research
conda install pytorch pytorch-cuda=12.1 -c pytorch -c nvidia
pip install transformers wandb einops
```

`conda`와 `pip`을 섞어 쓸 때는 **conda를 먼저, pip을 나중에** 설치하는 것이 충돌을 줄이는 핵심이다.
