# Notion 이미지 자동화 더미 사용 파일

아래 순서대로 복붙해서 쓰면 됩니다.
python scripts/notion_local_images.py \
  --post "_posts/ai/llm/2026-03-17-lora.md" \
  --notion-dir "assets/notion/LoRA (Low-Rank Adaption of Large Language Models)" \
  --verbose
---

## 1) 현재 글에 바로 적용 (네 경로 기준)

### 1-1. 미리보기 (파일 수정 안 함)

```powershell
python scripts/notion_local_images.py `
  --post "_posts/ai/llm/2026-03-01-openclaw-setting.md" `
  --notion-dir "assets/notion/ExportBlock-0c12b87e-c312-4968-861e-8da87b41dde1-Part-1" `
  --dry-run `
  --verbose
```

### 1-2. 실제 적용 (복사 + 링크 치환)

```powershell
python scripts/notion_local_images.py `
  --post "_posts/ai/llm/2026-03-01-openclaw-setting.md" `
  --notion-dir "assets/notion/ExportBlock-0c12b87e-c312-4968-861e-8da87b41dde1-Part-1" `
  --verbose
```

### 1-3. 로컬 확인

```powershell
bundle exec jekyll serve --livereload
```

브라우저: `http://localhost:4000`

---

## 2) 새 글 작성 때 템플릿

`POST_PATH`와 `NOTION_DIR`만 바꿔서 쓰면 됩니다.

```powershell
$POST_PATH="_posts/ai/llm/YYYY-MM-DD-your-post-slug.md"
$NOTION_DIR="assets/notion/ExportBlock-xxxx"

# 1) 미리보기
python scripts/notion_local_images.py --post $POST_PATH --notion-dir $NOTION_DIR --dry-run --verbose

# 2) 실제 적용
python scripts/notion_local_images.py --post $POST_PATH --notion-dir $NOTION_DIR --verbose
```

---

## 3) npm 명령으로 실행 (선택)

```powershell
npm run notion:local-images -- 
  --post "_posts/ai/llm/2026-03-17-lora.md" 
  --notion-dir "assets/notion/LoRA (Low-Rank Adaption of Large Language Models)"
```

python scripts/notion_local_images.py \
  --post "_posts/ai/llm/2026-03-17-lora.md" \
  --notion-dir "assets/notion/LoRA (Low-Rank Adaption of Large Language Models)" \
  --verbose

---

## 4) 결과가 어떻게 바뀌는지 예시

### 변경 전

```md
![image.png](image.png)
![image.png](image%201.png)
```

### 변경 후

```md
![image.png](/assets/images/posts/openclaw-setting/image.png)
![image.png](/assets/images/posts/openclaw-setting/image-1.png)
```

---

## 5) 되돌리기

스크립트는 기본으로 백업 파일을 만듭니다.

- 백업 파일: `<post>.md.bak`
- 예: `_posts/ai/llm/2026-03-01-openclaw-setting.md.bak`

복구가 필요하면 `.bak` 내용을 원본으로 되돌리면 됩니다.
