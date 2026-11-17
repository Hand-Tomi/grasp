# grasp 규칙의 연구 근거

## 먼저 알아 둘 한계

- **원리는 연구로 뒷받침되지만 이 스킬 자체는 검증되지 않았다.** 이 스킬을 썼을 때 이해 시간이 줄어든다는 것은 아직 측정한 적이 없다.
- **학습 연구는 대부분 학생이 짧은 교재를 배우고 곧바로 시험을 보는 상황이다.** 숙련된 개발자가 AI 출력을 읽고 판단하는 상황에 옮긴 것은 유추다. 아래에서 "유추"로 표시했다. 특히 Mayer의 원리들은 초보 학습자에게서 효과가 크고, 사전지식이 많을수록 줄어든다.
- **코드 리뷰 연구와 AI 의존 연구는 상황이 가깝다.** "직접"으로 표시했다.
- **가장 가까운 연구는 경고에 가깝다.** 전문 개발자 29명이 LLM이 만든 리뷰를 받고 코드를 리뷰한 실험에서, 리뷰어는 LLM이 짚은 곳에 집중했고, 경미한 문제는 더 찾았지만 심각한 문제는 더 찾지 못했으며, 시간도 줄지 않았고 확신도 높아지지 않았다 (Tufano 외 2025). 평균 시간은 오히려 늘었다(직접 리뷰 약 42분, LLM 리뷰 약 56분, 심어 둔 문제를 모두 알려 준 리뷰 약 57분. 차이는 유의하지 않음). 저자들은 시간이 늘어난 이유를 **주어진 코멘트를 읽고 이해하고 다시 확인하는 데 드는 시간**으로 보았고, "코드를 이해하게 돕지 않는다"는 설명은 확신이 높아지지 않은 결과에 대한 것이었다. 대상은 diff가 아니라 75~528줄짜리 독립 프로그램이었다(과제 6개를 Java와 Python으로 각각 구현한 12개, 심어 둔 문제 48개). 심어 둔 문제는 주로 유지보수성 문제였다(Java 78%, Python 64%). LLM 조건이 준 것은 코드 설명이 아니라 문제를 짚는 리뷰 코멘트였고, 리뷰어들은 그 코멘트 대부분을 타당하다고 보았다. 그래서 설명을 주는 grasp에 이 결과가 그대로 옮겨진다고 볼 수는 없지만, "AI가 짚은 곳에 주의가 몰린다"는 점은 grasp의 등급에도 해당한다. grasp는 바로 그런 읽기와 확인 거리(볼 곳, 판정, 질문)를 더하므로 시간이 늘 수 있다. 그래서 시간을 공동 주 지표로 둔다. 이 스킬의 목표인 "더 빠르고 정확한 이해"는 이 결과를 넘어서야 의미가 있고, 아직 그것을 보여 준 적이 없다.

## 규칙별 근거

### 지도를 먼저 준다 (유추, 효과 크기는 조건에 따라 다름)

주제를 모르면 거의 해석할 수 없는 글에서는 주제를 먼저 알려 주는 것이 이해와 기억을 크게 바꿨다. 하지만 일반적인 글에서 "선행 조직자"의 효과는 작다(메타분석에서 작지만 대체로 양의 효과. 이전의 서술적 리뷰들은 일관되지 않다고 보았다). 효과는 읽는 사람이 그 주제의 틀을 갖고 있지 않을 때 크다. 숙련자에게 지도의 주된 가치는 이해보다 **어디부터 볼지 고르는 것**이다. 그래서 이 스킬은 지도를 "이해를 크게 높이는 장치"가 아니라 **세부를 어디에 끼워 넣을지 알려 주는 짧은 안내**로 쓴다.

- Bransford, J. D., & Johnson, M. K. (1972). Contextual prerequisites for understanding. *Journal of Verbal Learning and Verbal Behavior*.
- Luiten, J., Ames, W., & Ackerson, G. (1980). A meta-analysis of the effects of advance organizers on learning and retention. *American Educational Research Journal*.

### 한 번에 4개 이하 (유추)

외부 도움 없이 머릿속에 동시에 붙잡는 덩어리는 대략 4개다. 화면에 목록이 있으면 그 한계가 그대로 적용되지는 않고, 숙련자는 더 큰 덩어리로 묶어 기억한다. 그래서 이 규칙의 실제 목적은 **우선순위를 강제하는 것**이고, 🔴 항목이 묻힐 때는 예외를 둔다.

- Cowan, N. (2001). The magical number 4 in short-term memory: A reconsideration of mental storage capacity. *Behavioral and Brain Sciences*.

### 새 용어를 먼저 소개한다, 목적과 무관한 내용은 뺀다, 중요한 곳을 표시한다, 그림과 설명을 붙여 둔다 (유추)

Mayer의 멀티미디어 학습 원리 중 사전 훈련, 일관성, 신호, 공간 근접 원리에 해당한다. 모두 초보 학습자에게서 효과가 크고, 사전지식이 많을수록 줄어든다. 그래서 용어집 밑줄 같은 신호는 화면당 처음 한 번만 준다.

한 덩어리씩 멈추는 규칙은 분절 원리(Mayer & Chandler 2001)에서 왔지만, 그 연구는 흘러가 버리는 내레이션 애니메이션을 끊어 준 것이다. 글은 이미 읽는 사람이 속도를 정할 수 있으므로, 이 스킬에서 멈추는 이유는 **사용자가 자기 목적에 맞는 덩어리를 고르게 하는 것**이다.

- Mayer, R. E. (2009). *Multimedia Learning* (2nd ed.). Cambridge University Press.
- Mayer, R. E., & Chandler, P. (2001). When learning is just a click away: Does simple user interaction foster deeper understanding of multimedia messages? *Journal of Educational Psychology*.

### 같은 사실을 한 번만 보여 준다, 이미 아는 것은 설명하지 않는다 (유추)

같은 정보를 그 자체로 완결된 여러 형태로 반복하면 이해에 도움이 안 되고 오히려 방해가 된다(중복 효과). 서로 보완하는 글과 그림은 여기에 해당하지 않는다(멀티미디어 원리). 그래서 규칙은 "글이나 그림 중 하나만"이 아니라 "같은 내용을 두 번 전부 말하지 않기"다.

초보자에게 도움 되는 안내가 숙련자에게는 학습을 방해한다(전문성 역전 효과). 기본 모드에서 사용자가 이미 아는 것을 설명하지 않고, 덩어리를 사용자가 고르게 하는 근거다.

- Kalyuga, S., Chandler, P., & Sweller, J. (1998). Levels of expertise and instructional design. *Human Factors*.
- Kalyuga, S., Ayres, P., Chandler, P., & Sweller, J. (2003). The expertise reversal effect. *Educational Psychologist*.

### 관계는 그림으로 보여 준다, 장식용 그림은 넣지 않는다 (유추)

그림은 관련된 정보를 한자리에 모아 주어서, 글에서는 찾고 추론해야 하는 관계를 바로 읽게 해 준다. 다만 그 장점을 살리도록 그린 그림만 그렇다. 반대로 흥미롭지만 핵심과 무관한 글이나 그림을 끼워 넣으면 학습이 나빠졌고, 앞쪽에 둘수록 더 나빴다.

- Larkin, J. H., & Simon, H. A. (1987). Why a diagram is (sometimes) worth ten thousand words. *Cognitive Science*.
- Harp, S. F., & Mayer, R. E. (1998). How seductive details do their damage: A theory of cognitive interest in science learning. *Journal of Educational Psychology*.

### 추상적인 설명에 구체적인 예를 붙인다, 여러 경우를 나란히 비교한다 (유추)

예시를 함께 공부한 쪽이 개념을 새 상황에 더 잘 적용했다. 예시를 정의 앞에 두든 뒤에 두든 차이는 작았다. 여러 경우를 나란히 놓고 비교하게 하면 무엇이 결과를 가르는지 더 잘 알아본다. deep 모드의 값 추적 표에 대조 사례(쿠폰 없는 주문, 부분 환불 등)를 함께 넣는 근거다.

- Rawson, K. A., Thomas, R. C., & Jacoby, L. L. (2015). The power of examples: Illustrative examples enhance conceptual learning of declarative concepts. *Educational Psychology Review*.
- Alfieri, L., Nokes-Malach, T. J., & Schunn, C. D. (2013). Learning through case comparisons: A meta-analytic review. *Educational Psychologist*.

### 확인 질문: 기억이 아니라 오해를 찾기 위해 (유추)

사람은 원리를 설명할 수 있다고 믿는 정도가 실제로 설명할 수 있는 정도보다 훨씬 크고, 직접 설명해 보게 하면 그 차이가 드러난다. 글을 읽은 직후 "이해했다"는 판단은 실제 이해와 약하게만 맞는다(Dunlosky & Lipko 2007). 매끄럽게 설명하는 강사의 강의는 배웠다는 느낌을 높였지만 실제 학습은 높이지 않았다(Carpenter 2013. 후속 연구는 엇갈린다: Carpenter 외 2020과 Toftness 외 2018은 같은 결과를 냈고, Wilford 외 2020은 실제 학습도 높아진 결과를 보고했다). 매끄러운 글을 쓰는 AI가 설명할 때 같은 착각이 생길 수 있다. 이 스킬이 질문하는 주된 이유가 이것이고, 페이지가 "이해했어요" 대신 "다 봤어요"라고 쓰는 이유도 같다.

연습 시험이 기억을 늘린다는 결과(시험 효과)는 이 스킬의 목적과는 조건이 다르다. Roediger & Karpicke(2006)에서 그 효과는 **며칠 뒤 시험에서** 나타났고, 5분 뒤 시험에서는 다시 읽기가 더 나았다. 메타분석 전체로는 시험이 다시 읽기보다 뚜렷이 나았고(Rowland 2014, g≈0.50), 짧은 지연에서도 양의 효과가 보고되지만 지연이 길수록 커진다는 것이 일반적인 정리다(지연별 수치는 원문 미확인). 요소들이 서로 얽힌 복잡한 내용에서는 효과가 줄어든다는 주장이 있지만(van Gog & Sweller 2015), 이 주장은 논쟁 중이고 여러 메타분석은 다양한 자료에서 시험 효과를 확인했다. 이 스킬은 대개 지금 판단하기 위한 것이므로 기억 효과를 기대하지 않고, 질문 수를 판단이 걸린 곳으로 제한한다.

설명 전에 질문하는 것(사전 질문)은 틀리더라도 이후 학습을 돕지만, 주로 **질문한 그 정보에 한해서** 돕는다. 질문한 정보에 대한 효과는 비교적 꾸준하고, **질문하지 않은 정보**에 대한 효과는 결과가 엇갈린다(Pan & Carpenter 2023, 검토자 인용, 원문 미확인). 그리고 비용이 있을 수 있다. 질문하지 않은 내용에서 주의가 멀어지는 것이다. grasp는 대개 🔴에만 질문하므로(quiz 모드는 사용자가 고른 🟡에도), 이것이 질문하지 않은 덩어리에서 주의를 더 떼어 낼 수 있다. 검증 계획에 질문 유무에 따른 🟡 결함 발견률 비교를 넣은 이유다. 코드 리뷰에서는 아무도 묻지 않은 위험이 중요할 수 있으므로, deep 모드는 질문으로 설명을 가리지 않고 주의 사항과 볼 곳을 언제나 보여 준다.

확인 질문 뒤에는 답의 핵심 1~3개를 보여 주고 사용자가 핵심마다 "내 답에 있음 / 없음 / 이 핵심이 틀렸다고 봄"을 고르게 한다. 스스로 채점할 때 사람은 자기 답을 후하게 보는데, 답을 핵심(idea unit) 단위로 나눠 비교하게 하면 과신이 줄었다(Dunlosky 외 2011). 다만 그 연구의 핵심은 정답에서 나온 것이었고, 여기의 핵심은 **틀릴 수 있는 AI의 분석**이다. 그래서 이 적용은 느슨한 유추이고, AI의 핵심을 정답처럼 받아들이게 만들 위험이 있다. 세 번째 선택지("틀렸다고 봄")와, 그 선택을 받으면 grasp가 원문을 다시 확인하는 규칙이 그 위험에 대한 대책이다. 이 체크는 아무것도 열거나 접지 않는다.

확인 질문을 "본 내용을 새 경우에 적용하게" 만드는 데도 근거가 있다. 글을 다시 말하게 하는 질문보다 추론을 요구하는 질문에서 이해 판단이 실제 이해와 더 잘 맞았고, 추론 질문이 나올 것을 미리 아는 것만으로도 판단이 정확해졌다 (Wiley, Griffin & Thiede 2005, Thiede, Wiley & Griffin 2011. 검토자 인용, 원문 미확인). 새 경우는 "가정:"으로 시작한다. 꾸며 낸 상황을 사실처럼 쓰면 나중에 그 출처를 잊고 사실로 기억할 수 있기 때문이다 (출처 감시 연구: Johnson, Hashtroudi & Lindsay 1993. 검토자 인용, 원문 미확인). 한 번의 짧은 세션에서 이 효과가 얼마나 클지는 알 수 없으므로, 이것은 예측된 효과가 아니라 유추에서 나온 예방책이다.

- Wiley, J., Griffin, T. D., & Thiede, K. W. (2005). Putting the comprehension in metacomprehension. *Journal of General Psychology*.
- Thiede, K. W., Wiley, J., & Griffin, T. D. (2011). Test expectancy affects metacomprehension accuracy. *British Journal of Educational Psychology*.
- Johnson, M. K., Hashtroudi, S., & Lindsay, D. S. (1993). Source monitoring. *Psychological Bulletin*.
- Pan, S. C., & Carpenter, S. K. (2023). Prequestioning and pretesting effects: A review of empirical research, theoretical perspectives, and implications for educational practice. *Educational Psychology Review*. (검토자 인용, 원문 미확인)
- Rozenblit, L., & Keil, F. (2002). The misunderstood limits of folk science: An illusion of explanatory depth. *Cognitive Science*.
- Dunlosky, J., & Lipko, A. R. (2007). Metacomprehension: A brief history and how to improve its accuracy. *Current Directions in Psychological Science*.
- Carpenter, S. K., Wilford, M. M., Kornell, N., & Mullaney, K. M. (2013). Appearances can be deceiving: Instructor fluency increases perceptions of learning without increasing actual learning. *Psychonomic Bulletin & Review*.
- Toftness, A. R., Carpenter, S. K., Geller, J., Lauber, S., Johnson, M., & Armstrong, P. I. (2018). Instructor fluency leads to higher confidence in learning, but not better learning. *Metacognition and Learning*.
- Wilford, M. M. 외 (2020). Lecturer fluency can impact students' judgments of learning and actual learning performance. *Applied Cognitive Psychology*.
- Carpenter, S. K., Northern, P. E., Tauber, S. K., & Toftness, A. R. (2020). Effects of lecture fluency and instructor experience on students' judgments of learning, test scores, and evaluations of instructors. *Journal of Experimental Psychology: Applied*.
- Dunlosky, J., Hartwig, M. K., Rawson, K. A., & Lipko, A. R. (2011). Improving college students' evaluation of text learning using idea-unit standards. *Quarterly Journal of Experimental Psychology*.
- Roediger, H. L., & Karpicke, J. D. (2006). Test-enhanced learning: Taking memory tests improves long-term retention. *Psychological Science*.
- Dunlosky, J., Rawson, K. A., Marsh, E. J., Nathan, M. J., & Willingham, D. T. (2013). Improving students' learning with effective learning techniques. *Psychological Science in the Public Interest*.
- van Gog, T., & Sweller, J. (2015). Not new, but nearly forgotten: The testing effect decreases or even disappears as the complexity of learning materials increases. *Educational Psychology Review*. 반론: Karpicke, J. D., & Aue, W. R. (2015). 같은 학술지.
- Rowland, C. A. (2014). The effect of testing versus restudy on retention: A meta-analytic review of the testing effect. *Psychological Bulletin*.
- Adesope, O. O., Trevisan, D. A., & Sundararajan, N. (2017). Rethinking the use of tests: A meta-analysis of practice testing. *Review of Educational Research*.
- Richland, L. E., Kornell, N., & Kao, S. L. (2009). The pretesting effect: Do unsuccessful retrieval attempts enhance learning? *Journal of Experimental Psychology: Applied*.

### quiz 모드: 묻고, 답에 맞춰 짚어 준다 (유추)

**기대할 수 있는 것과 없는 것.** quiz 모드는 답을 받고, 갈린 가정을 짚고, 후속 질문을 하나 낸다. 사용자의 풀이를 단계마다 따라가며 짚어 주지는 않는다. 그래서 튜터링 연구의 분류로는 **답 단위로 채점하는 시스템에 후속 한 번을 더한 것**에 가깝다. 그런 시스템의 효과는 튜터링이 없는 조건보다 d ≈ 0.31로, 단계마다 짚어 주는 튜터(d ≈ 0.76)나 사람 튜터(d ≈ 0.79)보다 훨씬 작았다 (VanLehn 2011). 대화형 튜터 AutoTutor의 이득은 같은 시간 글을 읽은 조건보다 약 0.3~0.8 표준편차로 정리된다 (Graesser 2016. 그 정리는 0.3을 Nye, Graesser & Hu 2014로, 0.8을 Graesser 외 2008로 인용하지만, Nye 외 2014 자체는 약 0.8을 보고하므로 0.3의 출처는 확인되지 않았다. 범위로 읽는다). 그리고 튜터링 대화가 같은 내용을 읽는 것보다 나았던 것은 **내용이 학습자 수준보다 어려울 때**였고, 수준에 맞는 내용에서는 읽기와 뚜렷한 차이가 없었다 (VanLehn, Graesser 외 2007). 그 내용의 사전지식이 충분한 사용자라면 뒤쪽 조건에 가깝다 (경력이 길어도 그 코드나 분야를 모르면 앞쪽일 수 있다). 또 이 연구들은 기간, 대상, 과제가 제각각이라 (예: VanLehn 외 2007의 한 실험에서 튜터링은 약 60분), 질문 8개 이하의 한 세션에 기대할 효과를 정해 주지 않는다. 따라서 이 숫자들은 **기대 효과가 아니다.** 이 모드의 근거는 "직접 답해 보면 읽기만 할 때 숨어 있던 오해가 드러난다"는 개연성이고, 그 효과의 크기는 모른다.

**왜 묻는가.** 입문 프로그래밍 수강생에게 자기가 제출한 프로그램에 대해 질문하자, 첫 연습(질문 3개)과 둘째 연습(질문 2개)에서 약 3분의 1이 질문 중 하나 이상을 틀렸다 (셋째 연습의 약 절반은 표본이 작고 자기 선택 편향이 커서 저자들도 탐색적으로 다뤘다). 테스트를 통과한 프로그램을 낸 학생도 그랬다. 초록은 질문의 정답 여부가 프로그램 제출 성공보다 이후 성과와 더 강하게 관련됐다고 쓰지만, 본문에서 그 관련은 한 연습에서만 유의했고 다른 연습에서는 아니었다(작은 표본). 이후 성과는 시험 점수가 아니라 다음 연습들의 점수 비율이었다 (Lehtinen, Lukkarinen & Haaranen 2021). "코드가 돌아간다"와 "코드를 이해한다"가 다를 수 있다는 것을 보여 주는, 이 모드에 가장 가까운 결과다. 하지만 대상이 초보 학습자였고, 정답 여부는 이전 프로그래밍 수강 경력(r ≈ .43)과 이전 프로그래밍 시간(r ≈ .37)과도 상관이 있었으며, 개입의 효과를 시험한 연구가 아니다. 활동을 수동, 능동, 구성, 상호작용으로 나누고 뒤로 갈수록 학습이 깊다고 보는 틀(ICAP, Chi & Wylie 2014)에서, 튜터가 묻고 채점하는 활동이 "구성"이 되는지는 학습자가 무엇을 만들어 내느냐에 달려 있다. 짚어 준 줄에서 문장을 찾아 옮기는 답은 "능동"에 가깝고, 그 줄로 새 경우를 추론하는 답이 "구성"에 가깝다. 이 틀은 가설로 제시된 것이다. "남에게 설명" 목적의 이유 설명 질문은 스스로 설명하게 하는 개입에 해당하며, 그 메타분석의 효과는 중간 크기였다 (Bisra 외 2018, 64개 보고서의 69개 효과 크기, g = 0.55). 스스로 설명하게 한 조건은 같은 내용의 설명을 대신 받은 조건보다도 나았다(g = .35, 설명 없는 대조군과의 차이보다는 작음). 그리고 설명을 요청하면 받을 수 있게 하자 성과가 낮아졌고, 저자들은 스스로 설명하려는 노력이 줄었기 때문이라고 해석했다 (Schworm & Renkl 2006, Bisra 외 2018에서 재인용). quiz 모드가 "답 알려줘"를 진행 안내에 넣지 않고 힌트 끝에서만 알리는 이유다. 승인 판단이 목적이면 배우는 것보다 시간이 중요하므로 안내에서 미리 알린다 (판단). 이것은 Bastani 외 2025에서 해가 컸던 "제한 없는 답" 조건에 가까운 쪽을 고른 절충이다. 그래서 목적이 "남에게 설명"이면 이유는 설명에 쓰지 않고 질문으로 남기고, 사용자가 볼 곳을 열어 볼 수 있으면 "질문부터"를 권한다. 그 코드를 모르는 사용자에게 설명 없이 이유를 물으면 전문성 역전 효과의 반대쪽, 즉 안내가 부족해서 생기는 부담이 생긴다. 다른 질문 종류에는 이 숫자를 옮기지 않는다. 덧붙여, g = .35는 효과 크기 6개(약 570명)에 기댄 값이다. 또 스스로 설명하는 조건이 시간을 더 쓴 연구에서 효과가 컸고(g ≈ .72, 시간이 비슷하면 g ≈ .41, 차이는 유의하지 않음), 저자들은 시간을 통제하지 않아 효율이 과장됐을 수 있다고 경고했다. 검증 계획에 같은 시간 읽기 조건을 둔 이유다. 프롬프트 형식별 차이(질문형, 명령형, 빈칸, 선택형)는 사후 검정에서 유의하지 않았으므로, "서술형으로 묻는다"는 규칙은 이 메타분석이 받치지 않는다. 선택형 프롬프트만 따로 보면 g = .24로 0과 다르지 않았고(효과 크기 2개), 저자들은 강한 단서가 스스로 설명을 약하게 할 수 있다고 보았다. 약한 방향 근거일 뿐이다. 서술형은 답에서 갈린 가정이 보여서 고른 판단이다.

**답이 볼 곳의 줄에 기대게 한다.** 떠올린 것은 틀린 내용이라도 반복해서 떠올리면 강화될 수 있다. 질문의 답이 grasp의 설명만으로 나오면, 설명이 틀렸을 때 문답이 그 틀린 내용을 두 번 연습시킨다. 이것이 이 스킬이 막으려는 자동화 편향이다. 그래서 🔴 질문의 답은 설명에 없고 볼 곳의 줄을 열어야 알 수 있는 사실에 기대게 한다. 이것은 검증 비용을 낮추는 장치(Vasconcelos 2023)라기보다, 줄을 직접 확인하도록 강제하는 장치에 가깝다 (인지 강제 장치, Buçinca 2021). 그런 장치는 과의존을 줄였지만 사용자들이 가장 싫어했으므로, 건너뛰기 비율이 높을 수 있다. 또 질문이 답이 있는 줄을 짚어 주므로, 그 줄을 연 사용자에게는 오해를 찾는 질문이라기보다 **확인을 강제하는 장치**가 된다. 이 경우 맞힌 답은 원래 생각이 맞았다는 뜻이 아니라 줄을 읽었다는 뜻일 수 있다. 원래 생각은 줄을 열기 전의 답("질문부터")이나 확신 표시에서 더 잘 드러난다. 이 규칙은 판단이고, 효과는 재지 않았다.

**질문부터.** 숙련자에게는 설명이 중복이 되어 오히려 비용이 된다 (전문성 역전 효과, 위 절). 첫 단계만 풀게 해서 수준을 빠르게 재고 그에 맞춰 안내를 바꾸는 방법이 연구됐다 (Kalyuga & Sweller 2004, 2005). 그리고 AI의 설명을 보기 전에 자기 답을 먼저 정하면 과의존이 줄었다 (Buçinca 2021, 아래 절). "질문부터"는 이 둘을 빌린 선택 사항이다. 다만 "질문부터"도 주의(grasp의 위험 판단)를 먼저 보여 주므로, 사용자가 AI의 판단을 전혀 보지 않고 답하는 Buçinca의 조건과는 다르다.

**힌트 하나, 그다음 답.** 튀르키예의 한 고등학교에서 약 1,000명이 수학 수업 네 번(90분씩)에 참여한 현장 실험에서, 제한 없는 GPT-4를 연습에 쓴 학생은 연습 문제는 48% 더 잘 풀었지만 이후 AI 없이 본 시험에서 대조군보다 17% 낮았다. 교사가 쓴 정답 풀이와 흔한 실수를 받고 정답 대신 단계적 힌트를 주도록 만든 버전은 연습 성적이 127% 높았고 시험 성적은 대조군과 비슷했다 (Bastani 외 2025). 이 버전은 여러 안전장치를 함께 넣은 것이라 힌트만의 효과를 가른 것은 아니고, 시험 성적에서 대조군과 유의한 차이가 검출되지 않았다. 해가 없다고 증명된 것도, 시험 성적을 높인 것도 아니라는 점에 주의한다. quiz 모드가 "모르겠어"에 힌트 하나를 먼저 주되, 사용자가 "답 알려줘"라고 하면 바로 주는 것은 이 결과와 사용자의 시간 사이의 절충이다. 다만 그 튜터의 힌트는 알려진 정답에 기대 있었고, grasp에는 따로 정해진 정답이 없다. grasp의 분석이 곧 정답 역할을 하므로, 힌트가 틀린 방향을 가리킬 위험이 있다 (아래 한계).

**피드백은 갈린 가정과 근거.** 컴퓨터 기반 학습의 메타분석에서, 설명을 붙인 피드백(효과 0.49)이 정답만 알려 주는 피드백(0.32)이나 맞음/틀림만 알려 주는 피드백(0.05)보다 컸고, 고차원 학습에서 특히 그랬다 (Van der Kleij, Feskens & Eggen 2015). 판정에 갈린 가정과 근거 줄을 붙이는 근거다. 피드백 개입은 평균적으로 성과를 높였지만 (d ≈ 0.41), 3분의 1 이상에서는 오히려 낮췄다. 저자들은 주의를 과제에서 자기 자신으로 돌리는 피드백이 효과를 낮춘다고 설명했다 (Kluger & DeNisi 1996, 수치는 2차 자료로 확인). 피드백 연구를 모은 리뷰에서도 칭찬은 효과가 가장 낮은 피드백에 속했고, 과제와 그 개선 방법에 대한 정보가 가장 컸다 (Hattie & Timperley 2007). 칭찬이나 위로를 붙이지 않는 이유다.

**확신을 묻는다.** 확신 없이 맞힌 답에 피드백을 주면 그 답의 기억이 크게 늘었다 (Butler, Karpicke & Roediger 2008). "반반", "찍음"으로 맞힌 답에 이유를 더하는 근거다. 같은 이유로, 확신한 답에 대한 **틀린** 교정도 강하게 받아들여질 수 있다. grasp의 판정이 틀렸다면 확신했던 맞는 답이 가장 크게 덮어써질 수 있으므로, 확신한 답을 틀림으로 판정할 때는 인용한 줄을 직접 확인하라고 권한다. 다만 틀린 교정이 확신한 답을 특히 더 덮어쓰는지는 위 연구들이 시험하지 않았다 (판단). 높은 확신으로 틀린 답은 피드백 직후에 오히려 더 잘 고쳐졌다 (과잉 교정 효과, Butterfield & Metcalfe 2001. 원문이 아니라 인용한 문헌으로 확인). 일주일 뒤에도 과잉 교정은 유지됐다 (Butler, Fazio & Marsh 2011). 다만 정답을 잊은 경우에는 높은 확신의 오답이 낮은 확신의 오답보다 **다시 나타나기 쉬웠다** (Butler, Fazio & Marsh 2011). 그래서 과잉 교정 효과 자체는 "확신한 오답에 후속 질문을 더 낸다"는 규칙을 받치지 않는다(오히려 쉽게 고쳐진다는 뜻이다). Butler 외 2011의 재발 결과는 확신했던 오답을 마무리 맨 위에 두고 "다시 풀 질문"으로 남기는 근거다. 그들은 정답을 다시 떠올릴 기회를 더 주라고 권했고, 같은 세션의 후속 질문 하나가 그 재발을 얼마나 막는지는 확인되지 않았다. 🟡에서 확신했던 오답에만 후속 질문을 내는 규칙은 판단이다. 두 연구 모두 일반 상식 문제였다. "확신한 생각은 스스로 다시 확인하지 않기 쉽다"는 것은 연구가 아니라 판단이다.

**질문하지 않은 것.** 단어 목록 실험에서는 일부를 떠올리는 연습이 같은 범주의 연습하지 않은 항목을 떠올리기 어렵게 만들었다 (인출 유도 망각, Anderson, Bjork & Bjork 1994). 반대로 서로 이어진 글에서는 일부를 시험한 것이 하루 뒤 시험하지 않은 부분의 기억도 도왔다 (Chan, McDermott & Roediger 2006). 코드 설명은 이어진 글에 가깝지만, 한 덩어리의 한 면만 묻는 것이 같은 덩어리의 다른 주의를 덜 떠올리게 할 가능성은 남는다. 위의 사전 질문 절과 같은 종류의 위험이다. 그래서 위험은 질문과 상관없이 주의에 결과까지 쓰고, 검증 계획에서 질문하지 않은 주의 사항의 기억과 반영을 따로 잰다.

**선택지를 줄 때.** 객관식에서 읽은 그럴듯한 오답은 나중에 정답처럼 떠올려질 수 있었고 (Roediger & Marsh 2005), 피드백을 주면 그 부작용이 줄었다 (Butler & Roediger 2008). 선택지를 원할 때만 주고, 판정에서 오답을 하나하나 바로잡는 이유다.

**설명 직후에 맞힌 것.** 학습 중의 수행은 오래가는 학습의 지표로 믿을 수 없고, 사람들은 그 수행을 학습으로 착각한다 (Soderstrom & Bjork 2015). 마무리가 "바로잡음" 대신 "설명 뒤 맞힘"이라고 쓰고, 이해가 굳었다는 뜻이 아니라고 밝히는 이유다.

**한계.**
- 위 연구는 대부분 학생이 교과 내용이나 상식을 배우는 상황이다 (피드백 메타분석은 더 넓은 과제를 포함한다). 숙련 개발자가 AI 출력을 판단하기 전에 오해를 찾는 상황에 옮긴 것은 유추다.
- 이 모드에서는 **튜터가 틀릴 수 있다.** 위의 연구에서 정답은 미리 정해져 있었지만, 여기서는 grasp의 분석이 정답 역할을 한다. grasp가 틀린 판정을 확신 있게 내리면 사용자의 맞는 이해를 틀린 것으로 "교정"할 수 있고, 설명이 틀리면 문답이 그 틀린 설명을 연습시킬 수 있다. 판정 전에 근거 줄을 다시 읽고, 사용자가 줄을 다르게 읽으면 설명부터 의심하고, 판정마다 위치를 주고, 확인하지 못한 것을 묻지 않고, 판정 보류를 허용하는 규칙이 그 대책이다. 이 위험이 실제로 얼마나 큰지는 재지 않았다.
- 시험 효과의 기억 이득은 주로 며칠 뒤에 나타난다 (위 "확인 질문" 절). 지금 판단하기 위한 문답에서 기대하는 것은 기억이 아니라 **오해를 드러내는 것**이다.
- 질문은 시간을 쓴다. 문답이 기본 모드보다 결정을 더 정확하게 만드는지, 그 시간이 값어치가 있는지는 측정하지 않았다 (검증 계획).

- VanLehn, K. (2011). The relative effectiveness of human tutoring, intelligent tutoring systems, and other tutoring systems. *Educational Psychologist*.
- VanLehn, K., Graesser, A. C., Jackson, G. T., Jordan, P., Olney, A., & Rosé, C. P. (2007). When are tutorial dialogues more effective than reading? *Cognitive Science*.
- Nye, B. D., Graesser, A. C., & Hu, X. (2014). AutoTutor and family: A review of 17 years of natural language tutoring. *International Journal of Artificial Intelligence in Education*.
- Graesser, A. C. (2016). Conversations with AutoTutor help students learn. *International Journal of Artificial Intelligence in Education*.
- Lehtinen, T., Lukkarinen, A., & Haaranen, L. (2021). Students struggle to explain their own program code. *ITiCSE*.
- Chi, M. T. H., & Wylie, R. (2014). The ICAP framework: Linking cognitive engagement to active learning outcomes. *Educational Psychologist*.
- Bisra, K., Liu, Q., Nesbit, J. C., Salimi, F., & Winne, P. H. (2018). Inducing self-explanation: A meta-analysis. *Educational Psychology Review*.
- Schworm, S., & Renkl, A. (2006). Computer-supported example-based learning: When instructional explanations reduce self-explanations. *Computers & Education*. (Bisra 외 2018에서 재인용, 원문 미확인)
- Kalyuga, S., & Sweller, J. (2004). Measuring knowledge to optimize cognitive load factors during instruction. *Journal of Educational Psychology*.
- Kalyuga, S., & Sweller, J. (2005). Rapid dynamic assessment of expertise to improve the efficiency of adaptive e-learning. *Educational Technology Research and Development*.
- Bastani, H., Bastani, O., Sungu, A., Ge, H., Kabakcı, Ö., & Mariman, R. (2025). Generative AI without guardrails can harm learning: Evidence from high school mathematics. *PNAS*.
- Van der Kleij, F. M., Feskens, R. C. W., & Eggen, T. J. H. M. (2015). Effects of feedback in a computer-based learning environment on students' learning outcomes: A meta-analysis. *Review of Educational Research*.
- Kluger, A. N., & DeNisi, A. (1996). The effects of feedback interventions on performance: A historical review, a meta-analysis, and a preliminary feedback intervention theory. *Psychological Bulletin*.
- Butler, A. C., Karpicke, J. D., & Roediger, H. L. (2008). Correcting a metacognitive error: Feedback increases retention of low-confidence correct responses. *Journal of Experimental Psychology: Learning, Memory, and Cognition*.
- Butterfield, B., & Metcalfe, J. (2001). Errors committed with high confidence are hypercorrected. *Journal of Experimental Psychology: Learning, Memory, and Cognition*.
- Butler, A. C., Fazio, L. K., & Marsh, E. J. (2011). The hypercorrection effect persists over a week, but high-confidence errors return. *Psychonomic Bulletin & Review*.
- Anderson, M. C., Bjork, R. A., & Bjork, E. L. (1994). Remembering can cause forgetting: Retrieval dynamics in long-term memory. *Journal of Experimental Psychology: Learning, Memory, and Cognition*.
- Chan, J. C. K., McDermott, K. B., & Roediger, H. L. (2006). Retrieval-induced facilitation: Initially nontested material can benefit from prior testing of related material. *Journal of Experimental Psychology: General*.
- Hattie, J., & Timperley, H. (2007). The power of feedback. *Review of Educational Research*.
- Roediger, H. L., & Marsh, E. J. (2005). The positive and negative consequences of multiple-choice testing. *Journal of Experimental Psychology: Learning, Memory, and Cognition*.
- Butler, A. C., & Roediger, H. L. (2008). Feedback enhances the positive effects and reduces the negative effects of multiple-choice testing. *Memory & Cognition*.
- Soderstrom, N. C., & Bjork, R. A. (2015). Learning versus performance: An integrative review. *Perspectives on Psychological Science*.

### AI의 설명과 분류를 그대로 믿지 않게 한다 (직접, 단 조건이 다름)

이 스킬은 AI가 AI의 출력을 설명하는 구조라서, 설명 자체를 과하게 믿게 될 위험이 있다.

아래 인간-AI 연구는 상황이 가깝지만 조건이 다르다. Bansal 2021과 Buçinca 2021은 일반 참가자(크라우드 워커)가 코드가 아닌 과제를 했고, Vasconcelos 2023은 미로 과제였다. 숙련 개발자의 코드 리뷰에 그대로 옮겨진다는 보장은 없다.

- 자동화된 보조 도구가 불완전하면 사람은 도구가 표시하지 않은 문제를 더 자주 놓치고(누락 오류) 도구의 틀린 판단을 따르기도 한다(실행 오류). 이 편향은 초보자와 숙련자 모두에게서 나타났고 단순한 훈련이나 지시로 막아지지 않았다 (Parasuraman & Manzey 2010).
- 진단 보조 도구의 신뢰도가 대략 0.7보다 낮으면 도구가 없을 때보다 성과가 나빠질 수 있다 (Wickens & Dixon 2007. 엄격한 경계가 아니라 대략적인 기준이다). 단서를 주면 예상한 대상은 더 잘 찾지만 예상하지 못한 대상에서는 주의가 멀어졌다 (Yeh 외 1999).
- 이 스킬의 등급 매기기와 순서 정하기가 바로 그런 보조 도구이자 단서다. **따라서 이 스킬의 순효과는 등급이 얼마나 정확한가에 달려 있고, 그 정확도는 아직 모른다.** Fregnan 2022가 보여 준 순서 효과도 양날이다. 네가 낮게 매긴 결함은 뒤에 놓이고 "건너뛰어도 됨"이 붙어서, 혼자 리뷰할 때보다 덜 발견될 수 있다.
- 그래서 지도에 **얕게 읽은 것**을 펼친 채로 밝히고, 🟡 ⚪를 지시가 아니라 "grasp 판단"으로 표시하고, 판정마다 그것이 틀렸다면 드러날 **한 곳**을 붙인다. 🟡에도 붙이는 이유는, 등급·순서·질문이 모두 🔴를 가리키면 🟡 안의 문제는 혼자 볼 때보다 덜 발견될 수 있기 때문이다 (Yeh 외 1999, Tufano 외 2025, Fregnan 2022). 여기에 "AI가 만든 코드의 버그는 요청한 핵심 로직 안에 있기 쉽다"는 판단이 더해지지만, 그 판단은 연구로 확인하지 않았다 (아래 판단 목록).
- 보조 도구가 **자기 신뢰도를 알려 주면** 사람들의 의존이 실제 신뢰도에 더 잘 맞춰졌다 McGuirl & Sarter 2006은 사례마다 달라지는 확신 정보를, Wang, Jamieson & Hollands 2009는 도구 전체의 신뢰도 수준을 미리 알려 준 경우를 다뤘다 (둘 다 검토자 인용, 원문 미확인). grasp가 지금 덩어리 목록 위에 쓰는 문장("얼마나 정확한지는 아직 측정되지 않았습니다")에는 숫자가 없으므로 두 연구 어느 쪽의 조건에도 해당하지 않고, 금방 무시될 수 있다. 그래서 지금의 문장은 정직하게 밝히기 위한 **판단**이다. 검증 계획의 첫 단계로 놓침 비율을 재면, 그 숫자를 보여 주는 것은 Wang 외 2009의 조건에 가까워진다. 또 사람은 도구가 말한 정확도보다 직접 본 정확도에 더 크게 반응했다 (Yin, Wortman Vaughan & Wallach 2019. 검토자 인용, 원문 미확인). 페이지의 "grasp가 앞서 틀렸던 것"이 그 역할을 일부 한다.
- 훈련 중에 자동화의 실패를 직접 겪은 사람은 이후 덜 맹신했다 (Bahner 외 2008. 원문이 아니라 인용한 문헌으로 확인). 그래서 대화 중 네가 틀렸던 것이 드러나면 숨기지 않고 페이지 맨 위의 "grasp가 앞서 틀렸던 것"에 남긴다.

- AI가 설명을 붙이면 사람들은 AI의 권고를 더 많이 받아들였고, **AI가 틀렸을 때도 그랬다** (Bansal 2021).
- AI의 답을 보기 전에 자기 답을 먼저 정하게 하는 "인지 강제 장치"는 과의존을 줄였다. 하지만 완전히 없애지는 못했고, **사용자들은 이 방식을 가장 싫어했으며**, 생각하기를 즐기는 사람에게서 효과가 컸다 (Buçinca 2021). 이 장치는 사용자가 AI의 판단을 **아직 보지 않았을 때만** 의미가 있다. 또 Buçinca의 장치는 사용자가 AI와 **같은 판단**을 먼저 내리게 한 것이지만, grasp는 "어떻게 동작해야 하나"라는 **기대**를 묻는다. 그래서 "바뀐 코드는 6천 원을 돌려준다" 같은 grasp의 사실 주장이 틀린 경우는 이 질문으로 막을 수 없고, 직접 확인할 위치와 "틀렸다고 봄" 표시가 그 역할을 한다. 그래서 deep 모드는 페이지를 열기 전에 채팅에서 기대나 기준을 묻는다. 페이지 안에서 물으면 지도, 제목, 주의 사항에서 답이 먼저 보인다. 싫어하는 사람이 많으므로 🔴 덩어리에만, 한 번에 묻고, 건너뛸 수 있게 한다.
- 설명이 AI의 답을 **검증하는 비용을 충분히 낮출 때** 과의존이 줄었다 (Vasconcelos 2023). `파일:줄` 같은 볼 곳을 짚어 주고 근거 수준을 붙이는 이유다. 페이지는 분석 결과를 "정답"이 아니라 "grasp의 분석"으로 표시한다.
- 같은 이유로 **근거 수준 표시 자체가 권위처럼 작동할 위험**이 있다. "코드에서 확인"은 grasp가 스스로 붙인 표시이지 제3자의 검증이 아니다. Bansal 2021의 결과대로라면 이런 표시는 틀린 주장의 수용도 높일 수 있다. 그래서 표시마다 직접 열어 볼 위치를 함께 주고, 검증 계획에서 일부러 틀린 설명에 "코드에서 확인" 표시를 붙여 시험한다.
- ⚪의 확인 위치는 판정을 잘 보여 주는 곳이 아니라 **판정이 틀렸다면 드러날 곳**이어야 한다. 실패할 수 없는 확인은 확인했다는 느낌만 주고 안주를 키운다 (Parasuraman & Manzey 2010의 논리). 가능하면 `checks.md`의 기계적 확인을 함께 준다.

- Parasuraman, R., & Manzey, D. H. (2010). Complacency and bias in human use of automation: An attentional integration. *Human Factors*.
- Wickens, C. D., & Dixon, S. R. (2007). The benefits of imperfect diagnostic automation: A synthesis of the literature. *Theoretical Issues in Ergonomics Science*.
- Yeh, M., Wickens, C. D., & Seagull, F. J. (1999). Target cuing in visual search: The effects of conformality and display location on the allocation of visual attention. *Human Factors*.
- McGuirl, J. M., & Sarter, N. B. (2006). Supporting trust calibration and the effective use of decision aids by presenting dynamic system confidence information. *Human Factors*.
- Wang, L., Jamieson, G. A., & Hollands, J. G. (2009). Trust and reliance on an automated combat identification system. *Human Factors*.
- Yin, M., Wortman Vaughan, J., & Wallach, H. (2019). Understanding the effect of accuracy on trust in machine learning models. *CHI*.
- Bahner, J. E., Hüper, A.-D., & Manzey, D. (2008). Misuse of automated decision aids: Complacency, automation bias and the impact of training experience. *International Journal of Human-Computer Studies*.
- Tufano, R., Martin-Lopez, A., Tayeb, A., Dabić, O., Haiduc, S., & Bavota, G. (2025). Deep learning-based code reviews: A paradigm shift or a double-edged sword? *ICSE*.
- Bansal, G., Wu, T., Zhou, J., Fok, R., Nushi, B., Kamar, E., Ribeiro, M. T., & Weld, D. (2021). Does the whole exceed its parts? The effect of AI explanations on complementary team performance. *CHI*.
- Buçinca, Z., Malaya, M. B., & Gajos, K. Z. (2021). To trust or to think: Cognitive forcing functions can reduce overreliance on AI in AI-assisted decision-making. *Proceedings of the ACM on Human-Computer Interaction (CSCW)*.
- Vasconcelos, H., Jörke, M., Grunde-McLaughlin, M., Gerstenberg, T., Bernstein, M. S., & Krishna, R. (2023). Explanations can reduce overreliance on AI systems during decision-making. *Proceedings of the ACM on Human-Computer Interaction (CSCW)*.

### 리뷰의 병목은 이해다 (직접)

Microsoft 개발자 연구에서 코드 리뷰의 핵심 어려움은 변경과 코드를 이해하는 일이었다. 이 스킬이 설명에 집중하는 이유다. 오픈소스 리뷰 코멘트 900개를 분석한 연구는 리뷰어의 정보 요구 일곱 가지를 찾았는데, 그중 "코드의 맥락"에 대한 요구 안에 바뀐 메서드와 변수가 어디서 쓰이는지가 들어 있다. 걷기의 "주의" 칸에 영향 범위(호출부)를 넣은 근거다.

- Bacchelli, A., & Bird, C. (2013). Expectations, outcomes, and challenges of modern code review. *ICSE*.
- Pascarella, L., Spadini, D., Palomba, F., Bruntink, M., & Bacchelli, A. (2018). Information needs in contemporary code review. *Proceedings of the ACM on Human-Computer Interaction (CSCW)*.

### 논리적 변경 단위로 묶는다 (직접)

여러 목적이 섞인 변경은 이해하기 어렵다. 변경을 독립된 부분으로 나눠 보여 주자 개발자 다수가 그 분할에 동의했고 이해에 도움이 된다고 답했다.

- Tao, Y., Dang, Y., Xie, T., Zhang, D., & Kim, S. (2012). How do software engineers understand code changes? An exploratory study in industry. *FSE*.
- Barnett, M., Bird, C., Brunet, J., & Lahiri, S. K. (2015). Helping developers help themselves: Automatic decomposition of code review changesets. *ICSE*.

### 중요한 순서로 배치한다 (직접)

리뷰에서 뒤에 나오는 파일은 코멘트를 덜 받고, 통제 실험에서도 결함이 있는 파일이 뒤에 놓이면 발견될 확률이 낮아졌다. 다만 결함 종류에 따라 효과가 달랐다.

- Fregnan, E., Braz, L., D'Ambros, M., Çalıklı, G., & Bacchelli, A. (2022). First come first served: The impact of file position on code review. *ESEC/FSE*.

### 한 덩어리에 200~400줄 이하 (직접, 단 근거가 약함)

Cisco에서 리뷰 2,500건을 분석한 결과 한 번의 리뷰에서 보는 양이 200~400줄을 넘으면 결함 발견률이 떨어졌고, 리뷰는 한 시간 안팎, 시간당 500줄 이하가 좋았다. 이 수치는 **리뷰 한 번(세션)** 기준이지 이해 단위 기준이 아니다. 이 스킬은 이것을 "한 번의 걷기에서 직접 읽게 하는 분량"의 상한으로 빌려 쓴다. 동료 평가 논문이 아니라 도구 회사의 보고서라는 점도 감안해야 한다. 리포트의 "40줄 안팎" 기준은 연구 근거가 없는 판단이다.

- SmartBear Software. Cisco 코드 리뷰 사례 연구 (*Best Kept Secrets of Peer Code Review*, 2006).

### 도메인 언어로 먼저 말하고 볼 곳을 짚어 준다 (직접, 단 서술 이론)

숙련된 개발자는 목적에 대한 가설을 세우고 그 증거가 되는 지점을 찾아가며 코드를 읽는다(Brooks). 낯선 코드를 읽는 프로그래머는 먼저 제어 흐름 중심의 모델을 만들고, 이해가 깊어지면서 도메인 의미와 연결한다(Pennington). 이 스킬은 사용자가 그 연결을 처음부터 갖고 시작하도록 도메인 언어로 먼저 말한다. 이 두 연구는 개입을 시험한 것이 아니라 이해 과정을 서술한 이론이다. 그리고 위험도 하나 있다. 도메인 수준의 이야기를 먼저 들으면 제어 흐름을 확인하지 않고 넘어가기 쉬운데, AI의 오류는 바로 거기 숨어 있을 수 있다. 그래서 "볼 곳"은 이야기가 아니라 실제 코드 줄을 가리킨다.

- Brooks, R. (1983). Towards a theory of the comprehension of computer programs. *International Journal of Man-Machine Studies*.
- Pennington, N. (1987). Stimulus structures and mental representations in expert comprehension of computer programs. *Cognitive Psychology*.

## 이 스킬을 검증하는 방법 (아직 하지 않음)

원리별 근거가 있어도 조합한 결과가 좋다는 보장은 없다. 검증하려면 이렇게 비교한다.

- **참가자**: 숙련된 개발자.
- **대상**: 결함을 일부러 심은 diff 여러 개와, 전문가가 정답 결정을 정해 둔 리포트 여러 개. 결함 일부는 🔴가 아니라 🟡나 ⚪ 덩어리 안에 둔다. 그리고 grasp의 설명 중 하나를 일부러 틀리게 만든다.
- **비교 조건**: 도움 없이 리뷰 / 일반적인 AI 요약을 보고 리뷰 / grasp로 리뷰. 현실의 대안은 "도움 없음"보다 "그냥 AI 요약"이므로 두 번째 조건이 중요하다. 여기에 안전장치를 하나씩 뺀 조건(질문 없음, 등급 없음, 얕게 읽은 것 표시 없음)을 더하면 각 장치의 효과를 나눠 볼 수 있다.
- **측정**: 걸린 시간, 결함 발견률(특히 🟡 ⚪ 안의 결함), **일부러 틀린 grasp 설명을 받아들인 비율**(과의존의 핵심 지표), 등급의 정확도(심은 결함 중 🔴에 들어간 비율), 사용자가 `볼 곳`과 확인 위치를 실제로 열었는지, 확신과 정확도의 일치, 리포트는 전문가 정답과 비교한 결정의 질.
- **비용도 잰다**: 질문에 쓴 시간, 건너뛰기 비율, 사용자 평가. 인지 강제 장치는 사용자가 가장 싫어하는 방식이었다(Buçinca 2021).
- **틀린 설명은 근거 수준별로 나눠 심는다.** 특히 "코드에서 확인" 표시가 붙은 틀린 설명을 얼마나 받아들이는지 따로 잰다.
- **"그냥 AI 요약" 조건에도 같은 수의 틀린 설명을 같은 종류의 위치에 심는다.** 그래야 틀린 설명 수용률의 비교가 의미를 갖는다. 참가자의 경력 기준과, 과제와 조건의 순서(역균형)를 미리 정한다.
- **예측 질문과 확인 질문은 따로 뺀다.** 둘은 작동 방식(먼저 자기 생각을 정하게 하기 / 본 뒤 새 경우에 적용하기)과 비용이 다르므로 "질문 없음" 하나로 묶지 않는다. 그리고 확인 질문이 제 역할을 하는지, 즉 **확인 질문을 틀린 사람이 실제로 틀린 결정(머지, 도입)을 더 많이 했는지**를 잰다. 그렇지 않으면 질문은 시간만 쓴다.
- **틀린 핵심(`points`)도 따로 심는다.** 사용자가 핵심마다 자기 답과 비교하는 곳은 AI의 분석을 정답처럼 받아들이기 가장 쉬운 곳이다. 틀린 핵심에 "내 답에 있음"이나 "없음"을 고른 비율과 "틀렸다고 봄"을 고른 비율을 잰다.
- **확인 위치가 제 역할을 하는지 잰다.** 🟡 ⚪ 안에 심은 결함이 grasp가 고른 "틀렸다면 드러날 곳"(`spot_check`)과 같은 곳이나 가까운 곳에 있었던 비율을 센다. 낮으면 "판정을 뒤집을 곳을 고른다"는 규칙이 실제로는 대표적인 곳을 고르고 있다는 뜻이다.
- **주 지표를 미리 정한다.** 결과를 본 뒤에 고르지 않는다. 후보: 🟡 ⚪ 안의 심각한 결함 발견률, 일부러 틀린 설명을 받아들인 비율, 걸린 시간. 각각 "그냥 AI 요약" 조건보다 나쁘지 않아야 하는 한계(비열등 한계)를 미리 정한다. 예: 심각한 결함 발견률은 5%p 이상 낮지 않을 것, 틀린 설명 수용률은 5%p 이상 높지 않을 것, 시간은 10% 이상 길지 않을 것. **🟡 ⚪ 안의 심각한 결함 발견률은 "도움 없음" 조건에 대해서도** 같은 한계를 둔다. AI 요약 조건 자체가 도움 없음보다 나쁠 수 있으므로(Tufano 외 2025, Yeh 외 1999), AI 요약과만 비교하면 도움 없음보다 나쁜 결과도 통과할 수 있다.
- **사용자 실험 전에 값싼 첫 단계**: 나중에 버그나 되돌림이 생긴 것으로 알려진 과거 diff에 grasp로 등급을 매겨, 문제가 된 줄이 어느 등급에 들어갔는지 본다. 기준선은 각 등급이 전체 줄에서 차지하는 비율이다. 실험 전에 정할 통과 기준의 예:
  - 문제 줄 중 ⚪에 들어간 비율이 ⚪의 줄 비율보다 낮고, 그 비율의 95% 신뢰 상한이 5%를 넘지 않는다. (⚪는 화면이 없고 "건너뛰어도 됨"이 붙으므로 가장 엄격하게 본다)
  - 문제 줄 중 🔴에 들어간 비율이 **🔴의 줄 비율보다 뚜렷이 높다** (예: 2배 이상). 모든 것을 🔴로 매기면 이 기준은 저절로 통과하므로 줄 비율 대비로 본다.
  - 🟡는 따로 보고한다.
  - 빠진 코드(만들어야 했는데 없는 마이그레이션, 테스트)는 "문제 줄"이 없으므로 diff 단위로 따로 센다.
  - 문제 줄은 diff 안에 몰려 있으므로 분석 단위는 diff로 하거나 diff 단위로 재표집(cluster bootstrap)한다.
  - ⚪ 안의 문제가 하나도 없을 때 95% 상한이 5% 아래가 되려면 독립된 관측이 약 60개 필요하다(3의 법칙). 문제는 diff 안에 몰려 있으므로 문제 60개가 아니라 **diff 약 60개**(또는 설계 효과를 반영한 유효 표본)로 잡는다.
  - ⚪는 grasp가 "끝까지 읽었다"고 한 자기 보고가 맞아야 안전하다. 도구 호출 기록과 대조해 그 보고를 감사한다.
  Wickens & Dixon의 약 0.7은 진단 적중률에 대한 값이라 이 지표에 그대로 옮길 수 없고, 방향만 참고한다. 모델이 공개 저장소에서 나중의 수정을 이미 봤을 수 있으므로, 비공개 저장소나 모델 학습 이후의 diff를 쓴다.
- **quiz 모드는 따로 비교한다.** 같은 대상에서 기본 모드, quiz 모드, 그리고 **quiz와 같은 시간 동안 기본 모드의 설명을 읽는 조건**을 비교한다. 마지막 조건이 없으면 문답의 효과와 더 오래 본 효과를 가를 수 없다. 결정의 정확도와 걸린 시간에 더해 두 가지를 잰다. 채점 기준(질문의 핵심)을 일부러 틀리게 만든 질문에서 **사용자가 맞는 답을 버린 비율**, 그리고 일부러 틀리게 만든 **설명**을 받아들인 비율이다. 문답은 떠올린 것을 강화하므로 틀린 설명의 수용이 기본 모드보다 높아질 수 있다. **설명 먼저와 질문부터를 비교하는 조건**도 둔다. 문항마다 걸린 시간과 건너뛰기 비율을 기록하고, 답이 짚어 준 줄을 인용하거나 바꿔 말한 것인지도 기록한다 (줄을 읽고 맞힌 것과 원래 알던 것을 가르기 위해).
- **시간은 공동 주 지표로 둔다.** 기준은 위의 비열등 한계 하나로 정한다(그냥 AI 요약보다 10% 넘게 길지 않을 것). 시간이 줄면 더 좋지만, 줄지 않았다고 실패로 보지는 않는다.
- **사용자 실험의 분석**: 참가자와 diff가 교차하므로 둘 다 무작위 효과로 넣는다. 필요한 참가자 수는 위의 비열등 한계와 예비 실험의 분산으로 미리 계산한다.

## 연구가 아니라 판단에서 나온 규칙

아래는 연구 근거 없이 정한 것이다. 써 보면서 고쳐야 한다.

- 주의 등급 🔴 🟡 ⚪ 의 구체적인 기준, 근거 수준 다섯 가지의 구분, 출처(근거 수준)와 근거의 튼튼함을 나누는 것
- 리포트에서 예측 대신 사용자의 기준을 먼저 적게 하는 것. 가까운 근거는 있다: 후보를 보기 전에 평가 기준을 먼저 정하게 하면 본 뒤에 기준을 바꿔 자기 선택을 정당화하는 일이 줄었다 (Uhlmann & Cohen 2005, 채용 판단 연구. 검토자 인용, 원문 미확인). 다만 영역이 달라 판단 목록에 둔다.
- 🟡 ⚪마다 "틀렸다면 드러날 곳"을 하나씩 붙이는 것과 그 고르는 기준, 무작위로 고른 한 곳을 덧붙이는 것(`references/checks.md`, 보조 수단) (무작위 표본은 분류기의 오류와 상관이 없다는 표본 추출의 논리이지, 시험된 학습 방법이 아니다)
- "요청한 로직(🟡) 안에 버그가 있기 쉽다"는 판단. AI가 만든 코드의 버그 분포에 대한 연구로 확인하지 않았다
- 지도를 한 화면(25줄 안팎)으로 제한하는 것, 덩어리당 질문 하나, 용어집 8개, 리포트 발췌 40줄
- 지도 뒤에 멈추고 사용자가 고르게 하는 것
- `quick`, 기본, `deep`, `quiz` 네 가지 모드
- 사용자가 말한 기준이 걸리는 덩어리를 🔴로 올리는 것, 기대와 분석의 차이를 한 줄(`gap`)로 쓰는 것, 분석에 대한 "확인했고 맞음 / 아직 확인 안 함 / 틀렸다고 봄" 선택, 직접 돌려 보는 명령(`repro`)
- 그림의 형태 구분, 그림 안에 덩어리 번호를 넣는 것, 세로 방향으로 그리는 것
- deep 모드에서 기대·기준 질문을 페이지를 열기 전에 채팅에서 묻는 것, 확인 질문은 페이지에서 하고 피드백은 채팅에서 하는 분담
- 그림을 덩어리당 0~3개로 정한 것
- quiz 모드의 세부: 질문 상한 8개, 힌트 한 번(후속 질문에는 없음), 후속 질문 하나, 확신 세 단계(확실 / 반반 / 찍음), 목적별 질문 종류, 설명 15줄 안팎과 위치 3곳, 🔴 질문의 답이 볼 곳의 줄에 기대게 하는 것, "질문부터" 선택, 다시 풀 질문(형태, 며칠 뒤라는 지연, 대상 목적), 🟡에서는 확신했던 오답에만 후속 질문을 내는 것, "확실"로 두 번 맞으면 질문부터를 권하는 것(Kalyuga의 빠른 평가는 설명 전에 재는 것이라 이 규칙을 직접 받치지 않는다), 서술형으로만 묻는 것, 이유 없는 답에 이유를 열린 질문으로 묻는 것, 질문마다 "판단 한 줄"을 쓰게 하는 것, "줄의 사실 없이" 맞힌 답을 따로 기록하는 것, 판정 10줄 안팎

## 확인 상태

위 문헌 중 Fregnan, Bacchelli & Bird, Barnett, Tao, SmartBear 보고서, Dunlosky 2013, Mayer & Chandler, Rawson, Richland, Larkin & Simon, Harp & Mayer, Roediger & Karpicke, Bansal, Buçinca, Vasconcelos, Carpenter, Pascarella, Parasuraman & Manzey, Dunlosky & Lipko, Dunlosky 외 2011, Wickens & Dixon, Yeh 외 1999, Wilford 외 2020, Carpenter 외 2020, Tufano 외 2025, Rowland 2014(전체 효과 크기만), Toftness 외 2018, Bisra 외 2018, Bastani 외 2025, Lehtinen 외 2021, Butler 외 2008, Butler 외 2011, Van der Kleij 외 2015, VanLehn 외 2007, Soderstrom & Bjork 2015, Anderson 외 1994, Chan 외 2006, Hattie & Timperley 2007, Roediger & Marsh 2005, Butler & Roediger 2008은 웹 검색으로 서지와 핵심 결과를 확인했다. VanLehn 2011, Nye 외 2014와 Graesser 2016, Kluger & DeNisi 1996, Chi & Wylie 2014, Kalyuga & Sweller 2004·2005는 초록과 2차 자료로 수치나 내용을 확인했다. Bahner 외 2008과 Butterfield & Metcalfe 2001은 인용한 문헌을 통해서만 확인했다. 나머지는 학습과학 검토자의 지적과 기억에 기댄 것이라 원문 대조가 필요하다.
