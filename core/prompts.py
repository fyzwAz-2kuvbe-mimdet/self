"""단계별 Gemini 프롬프트 조립 — 매뉴얼 운영 원칙 기반."""

from core.manual_data import CONSULTANT_RULES, WEEK_DATA


def build_prompt(step: int, question_id: str, student_answer: str) -> str:
    week = WEEK_DATA[step]
    question_label = next(
        (q["label"] for q in week["questions"] if q["id"] == question_id),
        "학생의 답변"
    )
    context = (
        f"현재 {step}주차 — {week['title']} 세션.\n"
        f"주차 목표: {', '.join(week['goals'])}\n"
        f"질문: {question_label}\n"
        f"학생 답변: {student_answer}"
    )
    return f"{CONSULTANT_RULES}\n\n[현재 세션 컨텍스트]\n{context}"


def build_summary_prompt(step: int, all_answers: dict) -> str:
    week = WEEK_DATA[step]
    answers_text = "\n".join(
        f"Q({qid}): {ans}" for qid, ans in all_answers.items() if ans.strip()
    )
    context = (
        f"{step}주차 — {week['title']} 세션 전체 답변 요약 요청.\n\n"
        f"학생의 모든 답변:\n{answers_text}\n\n"
        f"이 학생이 이번 세션에서 보여준 점 한 가지와, 다음 주차에 주의깊게 관찰할 점 한 가지를 짧게 적어줘. "
        f"평가어 없이. 컨설턴트(어른)에게 보고하는 톤으로."
    )
    return f"{CONSULTANT_RULES}\n\n[세션 마무리 요약]\n{context}"
