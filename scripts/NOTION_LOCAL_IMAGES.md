# Notion Export Image Automation (Local Assets)

This script moves image links like `![image.png](image.png)` from a Notion-exported post into stable Jekyll asset paths.

## What it does

1. Reads a post markdown file.
2. Finds local image links (markdown + `<img src>`).
3. Copies images from a Notion export folder to:
   - `assets/images/posts/<post-slug>/`
4. Rewrites links to:
   - `/assets/images/posts/<post-slug>/<image-file>`

## Command

```powershell
python scripts/notion_local_images.py `
  --post "_posts/ai/llm/2026-03-01-openclaw-setting.md" `
  --notion-dir "assets/notion/ExportBlock-0c12b87e-c312-4968-861e-8da87b41dde1-Part-1" `
  --verbose
```

## Preview only

```powershell
python scripts/notion_local_images.py `
  --post "_posts/ai/llm/2026-03-01-openclaw-setting.md" `
  --notion-dir "assets/notion/ExportBlock-0c12b87e-c312-4968-861e-8da87b41dde1-Part-1" `
  --dry-run
```

## Notes

- A backup is created by default: `<post>.md.bak`
- Remote URLs (`http://`, `https://`, `data:`), and root-relative paths (`/assets/...`) are left unchanged.
- You can override destination slug:
  - `--slug my-custom-slug`
