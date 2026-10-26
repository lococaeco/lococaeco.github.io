# Blog Studio

`lococaeco.github.io`의 글을 브라우저에서 작성하는 로컬 편집기입니다. 제목과
카테고리를 고르고, 이미지를 붙여넣고, 글을 확인한 뒤 저장하거나 GitHub로
전송할 수 있습니다. 기존 Jekyll 블로그와 Markdown 파일을 그대로 사용합니다.

## 실행 파일 하나로 시작하기

Python을 설치하지 않아도 실행할 수 있는 데스크톱 버전을 제공합니다.

| 운영체제 | 실행 파일 | 사용 방법 |
| --- | --- | --- |
| Windows 10/11, 64비트 | `BlogStudio.exe` | 더블클릭 |
| Ubuntu 22.04 이상, x86_64 | `BlogStudio-linux-x86_64` | 속성에서 실행 권한을 허용한 뒤 더블클릭 |

Ubuntu용은 Python과 Tcl/Tk를 포함한 **단일 실행 파일**입니다. AppImage나 FUSE
설치가 필요하지 않습니다. ARM 컴퓨터와 macOS용 파일은 제공하지 않습니다.

1. [GitHub Actions](https://github.com/lococaeco/lococaeco.github.io/actions)에서
   **Blog Studio desktop builds**의 성공한 실행을 엽니다.
2. 아래 **Artifacts**에서 운영체제에 맞는 파일을 내려받고 ZIP을 풉니다.
   GitHub 로그인이 필요하며 빌드 결과는 30일 동안 보관됩니다.
3. 위 표의 실행 파일 하나를 원하는 폴더로 옮겨 실행합니다. 함께 있는 SHA-256과
   빌드 정보 파일은 검증용이며 실행에 필요하지 않습니다.
4. 시작 창에서 `_config.yml`과 `_posts`가 있는 **블로그 폴더**를 선택하고
   **작성 시작**을 누릅니다. 기본 브라우저에 편집기가 열립니다.
5. 다음 실행부터는 선택한 폴더와 포트를 기억합니다. 종료 전 편집 화면에
   **모든 변경 저장됨**이 표시되는지 확인한 뒤 시작 창에서 종료하세요.

실행 파일에는 편집기만 들어 있고 개인 글·초안·GitHub 인증은 들어 있지 않습니다.
블로그 폴더는 별도로 필요합니다. 다른 컴퓨터에서는 먼저 블로그 저장소를 복제한
뒤 그 폴더를 선택하세요. 글과 초안은 선택한 폴더의 기존 `_posts`와
`.blog-studio`에 저장되므로 실행 파일을 교체하거나 이동해도 지워지지 않습니다.

**GitHub 전송에는 Git 설치와 해당 컴퓨터의 GitHub 인증이 여전히 필요합니다.**
Git이 없어도 작성·임시저장·파일 저장은 사용할 수 있습니다. GitHub CLI를
사용한다면 로그인 후 `gh auth setup-git --hostname github.com`으로 연결합니다.
실행 파일이 다른 컴퓨터의 로그인까지 가져오지는 않습니다.

Windows 실행 파일에는 유료 코드 서명이 적용되어 있지 않아 SmartScreen 경고가
나타날 수 있습니다. 본인 저장소의 성공한 빌드 결과인지 확인하세요.

같은 블로그를 여러 앱에서 동시에 열면 두 번째 앱은 시작을 막습니다. 사용 중인
포트가 다른 프로그램에 점유돼 있으면 별도 포트로 열고 시작 창에 알려줍니다.
이 경우 이전 포트의 브라우저 복구 기록과 새 편집 화면의 기록이 다를 수 있지만,
서버에 저장된 초안은 그대로 유지됩니다.

최근 폴더와 실행 로그는 Ubuntu의 `~/.config/blog-studio/`, Windows의
`%LOCALAPPDATA%\Blog Studio\`에 저장합니다. `XDG_CONFIG_HOME`을 설정했다면
Ubuntu에서는 해당 폴더를 사용합니다. 서버는 이 컴퓨터의 `127.0.0.1`에서만 열립니다.

## 소스 코드로 시작하기

Python **3.10 이상**이 필요합니다. Git 커밋과 GitHub 전송에는 Git도 필요합니다.
Node.js, Ruby, Jekyll을 설치하지 않아도 편집기는 실행됩니다.

이 절의 Python 설치 안내는 `.sh`/`.cmd`로 소스 코드를 실행하는 경우에만 해당합니다.
위의 데스크톱 실행 파일에는 Python이 포함되어 있습니다.

**Linux / macOS** — 저장소에서 실행합니다.

```sh
./blog-studio.sh
```

**Windows** — 저장소의 `blog-studio.cmd`를 더블클릭합니다. Python이 없다면
[python.org](https://www.python.org/downloads/)에서 설치하고 다시 실행하세요.

또는 운영체제에 맞는 Python 명령으로 직접 실행할 수 있습니다.

```sh
python3 tools/blog-studio/start.py
```

첫 실행에는 `.blog-studio/venv`에 전용 Python 환경과 PyYAML을 설치합니다.
설치할 때만 인터넷 연결이 필요하며, 컴퓨터의 기존 Python 패키지는 변경하지
않습니다. 이후 브라우저에서 `http://127.0.0.1:4310`이 열립니다. 실행 중인
터미널은 열어 두고, 종료할 때 `Ctrl+C`를 누르세요.

브라우저가 열리지 않으면 위 주소에 직접 접속합니다. 이미 포트를 사용 중이면
`./blog-studio.sh --port 4311`로 실행하세요. `--no-browser`는 브라우저 자동 열기를,
`--setup-only`는 최초 환경 준비까지만 실행하도록 설정합니다. 다른 위치에서도
실행 파일의 전체 경로를 사용하면 동일하게 동작합니다.

## 글 한 편 올리기

홈 화면의 **이어서 쓰기**에서 최근 초안을 바로 열 수 있습니다. 왼쪽 위
**Blog Studio**를 누르면 현재 내용을 저장한 뒤 홈으로 돌아갑니다.
글 설정은 필요할 때 여는 패널이며, 닫기 버튼이나 `Esc`로 편집에 돌아갑니다.

1. **새 글 쓰기**를 누릅니다. 빈 글, 논문 리뷰, 개발 노트, 오늘 배운 것
   템플릿을 선택할 수 있습니다.
2. 제목과 본문을 작성합니다. **시각 편집**에서는 도구 모음으로 서식을 적용하고,
   **Markdown**에서는 원문을 편집합니다.
3. 이미지를 본문에 붙여넣거나 끌어 놓습니다. **이미지** 버튼으로 여러 장을
   선택할 수도 있습니다. PNG, JPEG, GIF, WebP, AVIF를 한 장당 12MB까지 받습니다.
4. **글 설정**에서 카테고리, 태그, 날짜, 주소 이름, 대표 이미지, 공개 여부 등을
   정합니다. 새 글의 주소 이름은 비워두면 제목에서 자동 생성됩니다.
5. **발행 준비**에서 대상 파일과 경고를 확인하고 원하는 저장 방식을 선택합니다.

| 선택 | 실행되는 작업 |
| --- | --- |
| 파일로 저장 | `_posts`와 글에 사용하는 새 이미지를 저장 |
| 저장 + Git 커밋 | 파일 저장 후 이 글과 이미지의 변경을 로컬 Git 커밋으로 기록 |
| 저장 + GitHub 전송 | 파일 저장과 커밋 후 `origin`의 현재 브랜치로 push |

자동 저장과 `Ctrl/⌘+S`는 **로컬 초안 저장**입니다. 발행 준비에서 확인하기 전에는
블로그 원본 파일을 바꾸거나 GitHub로 전송하지 않습니다. `published: false`인
기존 글은 공개 설정을 직접 바꾸기 전까지 비공개 상태를 유지합니다.

GitHub 전송 완료 후 사이트에 반영되기까지 시간이 걸릴 수 있습니다.
[GitHub Pages 설정](https://github.com/lococaeco/lococaeco.github.io/settings/pages)과
[Actions](https://github.com/lococaeco/lococaeco.github.io/actions)에서 실제 빌드와
게시 상태를 확인하세요. 편집기는 Pages 설정이나 배포 워크플로를 변경하지 않습니다.

## 기존 글, 가져오기, 복구

- 왼쪽 목록에서 제목이나 태그로 검색해 기존 글을 엽니다. 기존 글은 원문 보존을
  위해 Markdown 모드로 시작하며, 제목을 바꿔도 파일 경로와 주소를 유지합니다.
  기존 글의 날짜·주소 이름·카테고리 이동은 이 편집기에서 지원하지 않습니다.
- **Markdown 가져오기**로 UTF-8 `.md` 파일을 새 초안으로 불러옵니다. YAML
  front matter도 읽습니다. Notion에서 내보낸 Markdown도 사용할 수 있지만,
  ZIP 파일이나 함께 내보낸 이미지 폴더를 자동으로 가져오지는 않습니다.
  이미지는 별도로 첨부하세요. 가져올 파일은 4MB 이하입니다.
- **내려받기**는 현재 초안을 YAML front matter를 포함한 Markdown 파일로
  내보냅니다. 별도 이미지 ZIP은 포함하지 않습니다.
- **기록**에서 최근 50회 저장 내용을 확인하고 복원합니다. 복원도 새 기록으로
  남으며, 원본 파일을 바로 덮어쓰지 않습니다.
- **작성 중**은 로컬에 임시저장한 초안과 기존 글의 수정본을 모아둔 목록입니다.
  각 글 오른쪽 **삭제** 버튼으로 글을 열지 않고 삭제할 수 있습니다.
  글 설정의 **이 초안 삭제** 버튼도 동일하게 동작합니다. `_posts`의 원본 글은
  삭제하지 않으며, 저장 이력과 업로드 이미지는 복구 자료로 남습니다.

다른 탭이나 외부 편집기에서 파일이 바뀌면 저장을 막고 충돌을 알립니다.
먼저 현재 내용을 **내려받기**로 보관하세요. 외부에서 변경된 원본을 다시 읽으려면
현재 초안을 삭제한 뒤 원본 글을 열고 보관한 내용을 반영하면 됩니다.

## 단축키

| 단축키 | 기능 |
| --- | --- |
| `Ctrl/⌘ + S` | 지금 초안 저장 |
| `Ctrl/⌘ + Shift + F` | 집중 모드 |
| `/` | 검색창으로 이동 |
| `N` | 새 글 작성 |

검색과 새 글 단축키는 입력란에서 글을 쓰는 동안 동작하지 않습니다.

## 알아두면 좋은 점

Markdown 편집 영역이 좁으면 **편집 / 미리보기** 탭으로 전환해 본문을 넓게
보여줍니다. 넓은 화면에서는 원문과 미리보기를 나란히 표시합니다.

편집 미리보기는 실제 Jekyll 사이트 전체를 실행하는 화면이 아닙니다. 편집기에서
수식은 KaTeX로 표시하며, 실제 사이트의 MathJax, Liquid, 테마와 결과가 다를 수
있습니다. 수식·Liquid·복잡한 HTML을 포함한 글은 Markdown 모드를 권장합니다.
시각 편집으로 전환하면 일부 Markdown 표현이나 서식이 정규화될 수 있습니다.

본문만 수정하면 기존 YAML 설정의 원문을 유지합니다. 제목·태그 등 설정을
수정하면 YAML을 다시 작성하므로 주석이나 따옴표 모양은 바뀔 수 있습니다.
편집기에 없는 설정 키와 중첩 설정 값은 보존합니다. 기존 `sitemap: false` 같은
편집기 밖의 설정도 유지하므로 필요하면 원본 파일에서 별도로 수정하세요.

카테고리는 현재 블로그에 등록된 11개 중에서 선택합니다. 예를 들어 메뉴의
`Deep Learning`은 기존 카테고리 페이지에 맞는 `Deep-Learning` 값으로 저장됩니다.
표시명, 폴더 이름, 실제 카테고리 값은 서로 달라도 기존 페이지와 연결을 유지합니다.

도구의 목차·댓글·수식 설정은 글의 YAML에 저장됩니다. 실제 표시 여부는 블로그
테마가 그 설정을 사용하는지에 달려 있습니다. 새 글 날짜는 한국 시간으로
생성됩니다. Jekyll이 미래 날짜의 글을 제외할 수 있어 발행 전 검사에서 미래
날짜의 글 저장을 막습니다. 예약 발행 서비스는 제공하지 않습니다.

편집기와 수식·글꼴 파일은 저장소에 포함되어 있어 오프라인으로 사용할 수
있습니다. 외부 URL의 이미지와 GitHub 전송에는 인터넷이 필요합니다. GitHub 인증은
컴퓨터에 설정된 Git 인증을 사용하며 브라우저에 개인 액세스 토큰을 입력하지
않습니다. 첫 전송 전에는 터미널에서 해당 저장소의 Git 인증과 `user.name`,
`user.email` 설정을 준비하세요.

다른 작업이 스테이징되어 있으면 커밋·전송을 중단합니다. 원격에 새 변경이 있거나
이 글과 무관한 미전송 커밋이 있으면 GitHub 전송을 중단합니다. 터미널에서 기존
작업을 확인하고 동기화한 뒤 다시 시도하세요. 전송만 실패한 경우 로컬 파일과
커밋은 남으므로 같은 글에서 전송을 다시 시도할 수 있습니다.

## 로컬 파일과 유지보수

| 경로 | 내용 |
| --- | --- |
| `.blog-studio/drafts/<id>.json` | 자동 저장 초안 |
| `.blog-studio/history/<id>/` | 최근 50회 저장 기록 |
| `.blog-studio/uploads/<id>/` | 초안에 첨부한 원본 이미지 |
| `.blog-studio/backups/<id>/` | 기존 글을 변경하기 직전의 Markdown 백업 |
| `.blog-studio/venv/` | 실행에 사용하는 Python 환경 |
| `_posts/<카테고리>/<날짜>-<주소>.md` | 발행 준비에서 저장한 글 |
| `assets/images/posts/studio-<id>/` | 저장한 글에 사용하는 이미지 |

`.blog-studio`는 Git과 Jekyll 게시 대상에서 제외됩니다. 컴퓨터를 옮길 때 초안과
기록을 유지하려면 이 폴더도 따로 백업하세요. 이력 50회 제한 외에는 업로드와
백업 파일을 자동 정리하지 않습니다. `tools`와 실행 파일도 Jekyll에서 제외됩니다.

서버는 `127.0.0.1`에서만 실행됩니다. 다른 웹사이트의 API 호출과 임의 파일 경로
접근을 막고, HTML 정화와 CSP를 적용합니다. TOAST UI Editor 3.2.2와 별도
DOMPurify 3.4.16을 사용합니다. 의존성 업데이트 시 수식과 기존 Markdown 보존을
다시 검증해야 합니다. 원본 배포 주소, 버전, 라이선스와 파일 해시는
[vendor 안내](static/vendor/README.md)와 [manifest](static/vendor/manifest.json)에 있습니다.

Ubuntu/Debian에서 소스 실행용 `venv` 생성 오류가 나면
`sudo apt install python3-venv` 후 다시 실행하세요. 데스크톱 실행 파일에는
이 과정이 필요하지 않습니다.

## 실행 파일 직접 빌드하기

Windows 파일은 Windows에서, Ubuntu 파일은 Ubuntu 22.04에서 각각 빌드합니다.
더 새로운 Linux에서 만든 파일은 더 오래된 Ubuntu에서 실행되지 않을 수 있습니다.
빌드용 Python 3.12에 Tk가 포함되어 있어야 합니다. Ubuntu 개발 환경에서는
`python3-tk`가 필요하며, 사용자가 내려받는 실행 파일에는 Tk도 들어 있습니다.

```sh
python -m pip install -r tools/blog-studio/requirements-build.txt
python tools/blog-studio/build_desktop.py
python tools/blog-studio/tests/package_smoke.py tools/blog-studio/dist/BlogStudio.exe
```

마지막 명령은 Windows용입니다. Ubuntu에서는 실행 파일 이름을
`BlogStudio-linux-x86_64`로 바꿉니다. 화면이 없는 CI 환경에서는 `xvfb-run -a`를
앞에 붙입니다. `dist/`와 `.build/`는 Git·블로그 게시 대상에 포함되지 않습니다.

**Blog Studio desktop builds** 워크플로는 두 운영체제에서 백엔드·런처 검사 후
실제 실행 파일을 빌드하고 다시 실행해 검사합니다. 패키지 검사는 Python과 Git을
찾을 수 없도록 PATH를 비운 상태에서 GUI, 편집기 리소스, 한글·공백 경로,
글과 초안 저장, 종료 후 재실행 복구를 검증합니다. 모든 검사는 임시 블로그만
사용합니다. Windows 개인 PC의 보안 정책·화면 배율까지 보장하는 검사는 아닙니다.

## 개발용 검사

백엔드 검증은 전용 환경 준비 후 아래 명령으로 실행할 수 있습니다.

```sh
.blog-studio/venv/bin/python -m unittest discover -s tools/blog-studio/tests -v
```

Windows에서는 Python 경로를 `.blog-studio\venv\Scripts\python.exe`로 바꿉니다.

브라우저 회귀 검증은 개발 시 선택적으로 실행합니다. 일반 글 작성에는
Playwright 설치가 필요하지 않습니다. 전용 환경에 설치한 뒤 실행하세요.

```sh
.blog-studio/venv/bin/python -m pip install playwright
.blog-studio/venv/bin/python tools/blog-studio/tests/browser_smoke.py
```

테스트는 `PATH`에서 찾은 `google-chrome` 또는 `chromium`을 사용합니다. 별도
브라우저 경로는 `STUDIO_BROWSER` 환경 변수로 지정할 수 있습니다.

```sh
STUDIO_BROWSER=/path/to/chromium .blog-studio/venv/bin/python tools/blog-studio/tests/browser_smoke.py
```

사용할 브라우저가 없다면 Playwright의 Chromium을 설치한 뒤 테스트를 실행합니다.

```sh
.blog-studio/venv/bin/python -m playwright install chromium
.blog-studio/venv/bin/python tools/blog-studio/tests/browser_smoke.py
```

브라우저 검증은 실제 Chromium에서 글 작성·이미지·파일 저장, 기존 글 보존,
오프라인 복구·내려받기, Markdown 가져오기·미리보기 정화, 좁은 화면과 글 전환을
확인합니다. 테스트는 임시 블로그 저장소만 사용하므로 실제 블로그 원본을
수정하거나 실제 GitHub 원격 저장소로 전송하지 않습니다.
