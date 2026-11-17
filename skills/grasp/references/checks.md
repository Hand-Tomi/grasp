# 기계적 확인 (코드)

🟡 ⚪ 판정에 붙일 기계적 확인 명령을 고를 때 읽는다. 리포트에는 해당하지 않는다.

원칙: **판정이 틀렸을 때 실제로 실패하는 명령만 준다.** 실패할 수 없는 확인은 확인했다는 느낌만 준다. 명령마다 **무엇을 잡지 못하는지**도 함께 적는다.

`<범위>`는 `main...feature/x` 같은 비교 범위, `<base>` `<head>`는 실제 비교할 두 커밋이다. 3점 비교의 `<base>`에는 `git merge-base main feature/x` 결과를 쓴다.

## 파일을 옮기기만 했다

```bash
git diff -M100% --name-status <범위> -- <경로>
```

모든 줄이 `R100`으로 시작해야 한다. `M`, `A`, `D`나 `R100`이 아닌 `R`이 있으면 내용도 바뀐 것이다.

잡지 못하는 것: 옮긴 파일 안의 식별자 이름 변경은 "내용 변경"으로 나오므로, 이름 변경까지 함께 했다면 아래 명령을 쓴다.

## 식별자 이름만 바꿨다

`Order`를 `Checkout`으로 바꾼 경우, 검토하는 저장소에서 실행한다 (Python 3.9 이상과 Git 필요):

```bash
python3 <이 스킬 폴더>/scripts/check_rename.py <범위> Order Checkout -- <경로>
```

**`PASS`가 나오고 종료 코드가 0이어야** 지정한 치환 외의 텍스트 변경이 없는 것이다. 도구는 3점 범위의 공통 조상과 head를 비교한다. 바뀐 파일마다 이전 파일의 독립된 `Order`를 `Checkout`으로 치환한 결과와 새 파일 **전체**를 비교한다. 공백·줄 순서 변경과 파일 추가·삭제·이동·모드 변경도 통과시키지 않는다. 여러 이름을 함께 바꿨거나 포맷도 바꿨으면 이 검사로 확인하지 못했다고 밝히고, 실제 언어의 파서 등으로 별도 확인하지 않은 덩어리는 🟡로 둔다.

삭제 토큰과 추가 토큰을 각각 `grep -v`로 지우는 검사는 쓰지 않는다. 대응하는 새 이름이 없어도 `return Order;` → `return;` 같은 로직 삭제를 통과시킬 수 있다.

이 명령이 통과해도 아래는 따로 본다. 하나라도 해당하면 ⚪가 아니다. Git 오류도 통과로 보지 않는다.

```bash
git diff <범위> -- <경로> | grep -E '^[-+].*["'"'"'](Order|Checkout)["'"'"']'      # 문자열 안의 이름 (직렬화 키, DB 값, 로그)
git diff <범위> -- <경로> | grep -E '^[-+][[:space:]]*export[[:space:]].*(Order|Checkout)'   # 밖에서 쓰는 이름 (공개 API)
git grep -n -w Checkout <base> -- <경로>                                       # 새 이름이 원래 있던 이름과 겹치는지
git diff --numstat <범위> -- <경로> | grep '^-'                                 # 바이너리 파일 변경
```

**범위도 확인한다.** 위 명령들은 `<경로>` 안만 보므로, "이 폴더 안에서만 바꿨다"는 판정 자체가 틀렸으면 잡지 못한다. 그래서 옛 이름이 남은 곳(`git grep -n -w Order <head> -- <넓은 경로>`)과 범위 밖의 변경(`git diff <범위> -- . ':(exclude)<경로>' | grep -E '^[-+].*(Order|Checkout)'`)도 본다. 둘 다 출력이 없어야 한다.

잡지 못하는 것: 언어별 의미. 문자열·주석 속 같은 철자도 치환하며, 공개 API, 이름 충돌, 동적 접근이나 다른 호출부와의 호환성은 증명하지 못한다. 같은 단어가 다른 의미로 쓰인 곳도 구분하지 못한다. 텍스트 치환이 맞는지와 그 변경이 동작에 영향을 주는지는 따로 판단한다.

주의: `sort | uniq -u`로 지운 줄과 더한 줄을 맞춰 보는 방법은 쓰지 않는다. 같은 줄이 여러 번 있거나 줄의 순서가 바뀌면 변경을 놓친다.

## 포맷만 바꿨다

프로젝트의 포매터를 기준 버전에 돌려서 결과가 새 버전과 같은지 본다.

```bash
git show <base>:<파일> | <포매터의 표준 입력 모드> | diff - <(git show <head>:<파일>)
```

예: `prettier --stdin-filepath <파일>`, `black -q -`, `gofmt`. **아무것도 출력되지 않아야** 포맷 변경뿐이다.

`git diff -w`는 들여쓰기가 의미를 갖는 언어에서 동작 변경(문장이 `if` 밖으로 나가는 것 등)을 숨기므로 쓰지 않는다. 다른 언어에서도 포매터 비교가 더 정확하다.

잡지 못하는 것: 포매터 버전이나 설정이 이번 diff에서 함께 바뀐 경우(그 변경까지 "포맷"으로 보인다), 포매터가 건드리지 않는 파일. 파일마다 돌려야 한다.

## 주석·문서만 바꿨다

문서 파일(`.md`, `.rst`, `.txt`)이 아닌 바뀐 파일마다, 언어의 파서로 주석을 지운 결과를 비교한다. 줄 모양을 보는 `grep`은 주석과 코드를 구분하지 못하므로 쓰지 않는다.

```bash
git diff --name-only <범위> | grep -vE '\.(md|rst|txt)$'      # 아래 비교를 돌릴 파일 목록

# TypeScript/JavaScript (typescript 패키지가 필요하다. 아래 "남의 저장소" 참고)
strip_ts() { node -e '
const ts = require("typescript"); let s = "";
process.stdin.on("data", d => s += d).on("end", () => {
  const f = ts.createSourceFile("x." + process.argv[1], s, ts.ScriptTarget.Latest, false);
  console.log(ts.createPrinter({ removeComments: true }).printFile(f));
});' "$1"; }

# Python (표준 라이브러리만 쓰고, 코드를 실행하지 않고 파싱만 한다): docstring은 빈 문자열로 바꿔 비교한다
strip_py() { python3 -c '
import ast, sys
t = ast.parse(sys.stdin.read())
for n in ast.walk(t):
    b = getattr(n, "body", None)
    if isinstance(n, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)) and b and isinstance(b[0], ast.Expr) and isinstance(b[0].value, ast.Constant) and isinstance(b[0].value.value, str):
        b[0].value.value = ""
print(ast.dump(t, indent=1))'; }

# 파일마다 (strip_ts ts / tsx / js 또는 strip_py)
set -o pipefail
git show <base>:<파일> | strip_py > /tmp/old.txt && git show <head>:<파일> | strip_py > /tmp/new.txt && diff /tmp/old.txt /tmp/new.txt && echo 같음
```

파일마다 **마지막에 `같음`만 나와야** 주석·문서만 바뀐 것이다. 차이가 출력되거나, 오류가 나거나, `같음`이 나오지 않으면 통과가 아니다. 파서를 불러오지 못하면 양쪽이 모두 빈 출력이 되어 `diff`만으로는 "같다"고 나오므로, 출력이 없는 것을 통과로 보지 않는다. 새로 생기거나 지워진 파일은 `git show`가 실패해 통과하지 않는다 (그런 파일은 주석만 바뀐 것이 아니다). 들여쓰기, 정규식이나 문자열 안의 `//`, 포맷 변경은 올바르게 처리된다 (포맷만 바뀐 것도 `같음`이다).

**남의 저장소(내려받은 코드)에서는** 그 저장소의 `node_modules`에 있는 typescript를 불러오는 것 자체가 그 저장소의 코드를 실행하는 것이다. 그래서:
- Python은 그대로 쓴다 (`ast`는 파싱만 한다).
- TypeScript/JavaScript는 **네가 따로 설치해 둔 typescript가 있을 때만**, 저장소 밖의 폴더에서 `git -C <저장소> show ...`로 읽고 `NODE_PATH=<설치한 폴더>/node_modules`를 붙여 실행한다. 저장소 안에서 실행하면 저장소의 `node_modules`가 먼저 불린다.
- 그런 도구가 없으면 기계적 확인을 쓰지 않는다. 그 덩어리는 ⚪가 아니라 🟡로 두고, `git diff -U0 <범위> -- <파일들>`을 **직접 읽을 목록**으로 준다 (확인 명령이 아니라 읽기 목록이라고 밝힌다).

잡지 못하는 것: Python docstring의 내용 변경(`__doc__`로 읽는 코드가 있으면 동작이 바뀐다), 문서 생성기나 타입 검사기가 읽는 주석(JSDoc 타입, `# type:`, `// @ts-ignore`, `eslint-disable`), 문서 파일 안의 예제 코드나 설정.

## 생성 코드다

```bash
<생성 명령> && git diff --exit-code -- <생성 경로> && test -z "$(git status --porcelain -- <생성 경로>)"
```

종료 코드가 0이어야 생성 결과와 같다. `git diff`는 새로 생긴 파일을 보지 못하므로 `git status --porcelain`도 함께 본다.

**생성기의 입력(스키마, IDL, 설정)이 같은 diff에서 바뀌었는지 반드시 밝힌다.** 입력이 바뀌었으면 생성 코드는 입력과 완벽히 일치하면서도 API 변경을 담고 있을 수 있다. 그때는 ⚪가 아니라 입력 변경을 🔴나 🟡로 다룬다.

잡지 못하는 것: 생성기 버전 차이, 생성 결과를 손으로 고친 뒤 생성기 입력도 맞춰 고친 경우. 생성 명령을 실제로 알 때만 주고, 명령을 적는다 ("다시 생성해 비교함"이라고만 쓰지 않는다). 사용자 자신의 저장소이고 실행해도 될 때만 네가 직접 돌려 "실행해서 확인"으로 표시한다.

## 로직을 다시 썼고 동작은 같다고 판단했다

옛 코드와 새 코드를 같은 입력으로 돌려 결과를 비교하는 차등 테스트가 가장 직접적이다. 사용자 저장소에서 돌려도 될 때만 쓴다.

```bash
git worktree add /tmp/old <base>   # 옛 코드를 따로 꺼내 둔다
# 옛 함수와 새 함수를 각각 실제 모듈에서 import해 같은 입력 목록(경계값 포함)을 넣고 결과를 비교하는 짧은 스크립트
```

잡지 못하는 것: 넣지 않은 입력, 부수 효과(로그, 시간, 전역 상태). 함수를 손으로 복사해 비교하면 복사본을 시험한 것이 되므로 반드시 실제 모듈을 import한다.

## 지운 테스트가 다른 곳에서 여전히 다뤄진다고 판단했다

```bash
git show <c> -- <테스트 경로> | grep -E '^-[[:space:]]*(test|it|describe)\('     # 지운 테스트 이름
git grep -n '<지운 테스트가 확인하던 구체적인 단언>' <c> -- <테스트 경로>           # 남은 테스트에서 같은 단언 찾기
```

지운 테스트마다, 그것이 확인하던 **구체적인 단언**(기대값, 에러 종류)이 남은 테스트에 있어야 한다.

잡지 못하는 것: 같은 단언이 다른 입력이나 다른 설정으로 쓰인 경우(문자열은 같지만 다른 것을 시험한다). 찾은 줄을 열어 입력이 같은지 확인한다.

## 무작위로 고른 한 곳

네가 고른 확인 위치는 네 맹점을 공유한다. 무작위로 고른 위치는 그렇지 않다.

```bash
git diff -U0 <범위> -- <경로> | grep '^@@' | awk 'BEGIN{srand()} {a[NR]=$0} END{print a[int(rand()*NR)+1]}'
```

실행할 때마다 다른 곳이 나온다. 한 곳만 보면, 덩어리 안에 문제가 한 곳만 있을 때 그것을 볼 확률은 1/(변경 묶음 수)다. 그래서 이것은 보조 수단이고, 변경 묶음 수를 함께 알려 준다.
