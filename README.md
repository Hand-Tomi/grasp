# grasp

Claude Code용 스킬입니다. (An agent skill for Claude Code. Documentation is in Korean.)

긴 코드 변경(diff, PR, 브랜치, 커밋)이나 긴 리포트·문서를 빠르고 정확하게 이해하도록 안내하는 스킬입니다.

Claude가 대상을 끝까지 대신 읽고, 이 순서로 보여 줍니다.

1. **지도**: 한 화면 분량의 요지, 할 일, 확인하지 못한 것
2. **덩어리별 설명**: 중요한 순서(🔴 🟡 ⚪)로 하나씩
3. **확인**: 판단에 필요한 질문과, 직접 열어 볼 코드 위치

설명을 그대로 믿지 않도록, 주장마다 근거 수준(실행해서 확인 / 코드에서 확인 / 추정 / 미확인 등)을 붙이고 얕게 읽은 부분을 밝힙니다.

## 모드

| 모드 | 하는 일 |
| --- | --- |
| `quick` | 지도만 보여 줍니다 |
| 기본 | 지도 → 덩어리별 설명 → 확인 |
| `deep` | 다이어그램과 표가 들어간 설명 페이지를 브라우저로 엽니다 |
| `quiz` | 짧게 설명하고 질문을 낸 뒤, 답에 맞춰 짚어 줍니다 |

## 설치

```sh
git clone https://github.com/Hand-Tomi/grasp.git
mkdir -p ~/.claude/skills
cp -R grasp/skills/grasp ~/.claude/skills/
```

Claude Code에서 "이 PR 뭐가 바뀐 거야", "이 리포트 정리해서 이해시켜줘", "quiz me on this diff" 같이 요청하면 쓰입니다.

## 요구 사항

- `deep` 모드: Python 3 (표준 라이브러리만 사용)
- `deep` 모드 다이어그램 검사: Chrome, Chromium 또는 Edge (없으면 검사만 건너뜁니다)
- `deep` 모드 페이지는 열 때 jsDelivr CDN에서 [Mermaid](https://mermaid.js.org/) 11.17.2를 불러옵니다. 오프라인이면 다이어그램이 소스 텍스트로 보입니다. 페이지의 CSP가 외부 전송을 막으므로 페이지 내용은 밖으로 나가지 않습니다.

## 근거

각 규칙의 연구 근거와 한계는 [`skills/grasp/references/evidence.md`](skills/grasp/references/evidence.md)에 있습니다. 이 스킬 전체의 효과는 아직 검증하지 않았습니다.

## 라이선스

[MIT](LICENSE)
