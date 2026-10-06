# lococaeco 블로그 · Blog Studio

이 저장소의 Jekyll 블로그를 브라우저에서 편하게 작성하는 로컬 편집기입니다.
시각 편집, Markdown, 이미지 붙여넣기, 자동 저장, 이전 버전 복원을 지원합니다.

Python 3.10 이상을 설치한 뒤 Linux/macOS에서는 아래 명령을 실행하세요.

```sh
./blog-studio.sh
```

Windows에서는 `blog-studio.cmd`를 더블클릭하세요. 첫 실행에 필요한 환경을 준비하고 브라우저를 엽니다.
글 작성 후 **발행 준비**에서 파일 저장, Git 커밋, GitHub 전송 중 선택합니다.
시작 방법과 복구·게시 안내는 [Blog Studio 사용 설명서](tools/blog-studio/README.md)를 확인하세요.

## 블로그 미리보기와 점검

블로그 자체를 실행하려면 Ruby 3.2 이상과 Bundler를 설치하고 다음을 실행합니다.
Blog Studio로 글만 작성할 때는 Ruby가 필요하지 않습니다.

```sh
bundle install
bundle exec jekyll serve
```

미리보기는 `http://127.0.0.1:4000`에서 열립니다. 게시 전 점검은 아래와 같습니다.

```sh
JEKYLL_ENV=production bundle exec jekyll build
python3 scripts/check_site.py --site _site
```

검사기는 제목·설명·대표 URL·구조화 데이터, 내부 링크와 이미지, 사이트맵·RSS·검색 목록,
비공개 글과 Blog Studio 임시 저장 데이터의 공개 여부, 검색엔진 소유권 인증 파일을 확인합니다.
GitHub에 변경을 올리면 **Blog checks**에서도 같은 검사를 실행합니다.
이 워크플로는 검사만 수행하며 기존 GitHub Pages 배포 설정을 변경하지 않습니다.

검색 결과와 빈 카테고리는 `noindex` 처리하고 사이트맵에서 제외합니다.
빈 카테고리에 공개 글이 추가되면 자동으로 색인 허용과 사이트맵 포함 상태로 돌아옵니다.
페이지 주소와 기존 Google·Naver·Bing 인증 파일은 유지합니다.
게시글의 `description`, `teaser`, `teaser_alt`, `last_modified_at`을 설정하면 검색·공유 정보에 반영됩니다.
`mathjax: false`로 해당 글의 수식 라이브러리를 끌 수 있으며 댓글은 버튼을 눌렀을 때 불러옵니다.

Google Search Console의 **소유권 확인**과 **검색 색인 생성**은 별도 단계입니다.
이 점검이 통과해도 Google 색인을 보장하지 않습니다. 배포 후 URL 접두어 속성
`https://lococaeco.github.io/`에서 기존 HTML 인증과 `sitemap.xml`을 확인하고,
대표 글의 URL 검사에서 표시되는 구체적인 사유를 확인하세요.
