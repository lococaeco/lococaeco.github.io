---
title: "[Ep_0: Introduction] 대 LLM 시대의 필수 언어 Markdown에 대하여 알아보기"
excerpt: "Introduction"

categories:
  - Dev
  - Markdown
tags:
  - Markdown
  - Writing
  - Blog

toc: true
last_modified_at: 2026-05-25
published: true
sitemap: true
---

# MARKDOWN 연습

이 글은 블로그 글을 더욱 잘 작성하기 위해 Markdown 문법을 하나씩 실험해보며 연습해 나아가는 공간입니다.

## 1. 제목

Markdown에서는 `#`의 개수로 제목의 깊이를 표현합니다.

```markdown
# H1 제목
## H2 제목
### H3 제목
#### H4 제목
```

실제 블로그 글에서는 글 제목이 이미 front matter의 `title`에 들어가므로, 본문에서는 보통 `##`부터 사용하는 편이 깔끔합니다.

## 2. 문장 강조

문장에서 중요한 부분은 **굵게**, *기울임*, `인라인 코드`로 강조할 수 있습니다.

- `**굵게**`: 핵심 키워드를 강조할 때 사용합니다.
- `*기울임*`: 용어, 짧은 뉘앙스, 보충 표현에 사용합니다.
- `` `인라인 코드` ``: 명령어, 파일명, 변수명처럼 정확히 적어야 하는 텍스트에 사용합니다.


## 3. 목록
순서가 중요하지 않은 내용은 불릿 목록으로 씁니다. **-** 와 스페이스바 한번이면 됩니다.
- 글의 주제 정하기
- 목차 잡기
- 예시 코드 넣기
- 최종 문장 다듬기

순서가 중요한 내용은 번호 목록이 좋습니다.

1. 초안 작성
2. 로컬에서 미리보기
3. 오탈자 수정
4. 발행 여부 확인

## 4. 체크리스트

작업 진행 상태를 기록할 때는 체크리스트를 사용할 수 있습니다. 당연하게도 대괄호와 영어 x를 사용하시면 됩니다.

- [x] 파일 만들기
- [x] front matter 작성하기
- [ ] 로컬 빌드 확인하기

## 5. 인용문

인용문은 `>`로 시작합니다.

> 좋은 글은 한 번에 완성되기보다, 여러 번 읽고 고치면서 점점 선명해진다.

> 일단 유명해져라, 그러면 X를 싸도 박수를 쳐줄 것이다.

인용문은 외부 문장뿐 아니라 스스로 기억하고 싶은 메모를 강조할 때도 유용합니다. 

## 6. 링크와 이미지

링크는 `[텍스트](URL)` 형식으로 작성합니다.

``` markdown
[GitHub Pages 공식 문서](https://docs.github.com/pages (괄호)
```

[GitHub Pages 공식 문서](https://docs.github.com/pages)

이미지는 링크 앞에 `!`를 붙입니다.

```markdown
![샘플 이미지](/assets/images/samples/image1.jpg)
```

![메타몽입니다.](../../../assets/images/posts/2026-05-25-markdown-practice/1779647762310.png)

## 7. 표

간단한 비교는 표로 정리하면 읽기 쉽습니다.

``` markdown
| 1 | 2 | 3 |
|:-|:-:|-:|
| 왼쪽 정렬 | 중앙 정렬 | 오른쪽 정렬 |
| 이런 | 식으로 | 하시면 |
| 간단한 | 표는 | 금방 만들죠 |

```
| 1 | 2 | 3 |
|:-|:-:|-:|
| 왼쪽 정렬 | 중앙 정렬 | 오른쪽 정렬 |
| 이런 | 식으로 | 하시면 |
| 간단한 | 표는 | 금방 만들죠 |


## 8. 코드 블록

코드 블록은 백틱 세 개로 감싸고, 언어 이름을 함께 적으면 문법 강조가 적용됩니다.

``` markdown

 [```python
  def greet(name: str) -> str:
      return f"Hello, {name}!"


  print(greet("Markdown"))
  ```]
대괄호는 빼야 합니다!
```

```python
def greet(name: str) -> str:
    return f"Hello, {name}!"


print(greet("Markdown"))
```

터미널 명령어는 `bash`로 표시합니다.

```bash
bundle exec jekyll serve
```

## 9. 수식

이 블로그는 `mathjax: true`가 기본값이므로 수식도 사용할 수 있습니다.

인라인 수식은 `$a^2 + b^2 = c^2$`처럼 작성합니다.

블록 수식은 아래처럼 사용합니다.

``` markdown
$$
\text{softmax}(x_i) = \frac{e^{x_i}}{\sum_j e^{x_j}}
$$
```

$$
\text{softmax}(x_i) = \frac{e^{x_i}}{\sum_j e^{x_j}}
$$


## 마무리

이 정도만 해도 Markdown 글을 쓰는건 크게 어렵지 않습니다. 하지만, 많이 불편하긴 하죠. 따라서, 어떻게 최적화가 되어야지
Markdown을 사용하면서도 편하게 포스팅을 할 수 있는지는 다음 에피소드에 포스팅하겠습니다.