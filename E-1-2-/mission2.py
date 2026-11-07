import json
import os
import sys

# 1. 개별 퀴즈를 담당하는 Quiz 클래스
class Quiz:
    def __init__(self, question, choices, answer):
        self.question = question
        self.choices = choices
        self.answer = answer

    def to_dict(self):
        """데이터 저장을 위해 딕셔너리 형태로 변환"""
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer
        }

    @classmethod
    def from_dict(cls, data):
        """불러온 딕셔너리 데이터로 Quiz 객체 생성"""
        return cls(data["question"], data["choices"], data["answer"])


# 2. 게임 전체 흐름을 관리하는 QuizGame 클래스
class QuizGame:
    def __init__(self):
        self.file_name = "state.json"
        self.quizzes = []
        self.best_score = 0
        self.load_data()

    def load_data(self):
        """JSON 파일에서 데이터를 불러오거나, 없으면 기본 퀴즈 세팅"""
        # 필수 요구사항: 기본 퀴즈 5개 이상 세팅
        default_quizzes = [
            Quiz("파이썬(Python)의 창시자는 누구일까요?", ["귀도 반 로섬", "리누스 토발즈", "빌 게이츠", "스티브 잡스"], 1),
            Quiz("마블 시네마틱 유니버스에서 타노스가 모은 인피니티 스톤의 개수는?", ["4개", "5개", "6개", "7개"], 3),
            Quiz("대한민국의 수도는 어디일까요?", ["부산", "인천", "서울", "대구"], 3),
            Quiz("태양계에서 지구는 태양으로부터 몇 번째 행성일까요?", ["첫 번째", "두 번째", "세 번째", "네 번째"], 3),
            Quiz("영화 '기생충'의 감독은 누구일까요?", ["박찬욱", "봉준호", "이창동", "김기덕"], 2)
        ]

        if not os.path.exists(self.file_name):
            self.quizzes = default_quizzes
            return

        try:
            with open(self.file_name, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.quizzes = [Quiz.from_dict(q) for q in data.get("quizzes", [])]
                self.best_score = data.get("best_score", 0)
                if not self.quizzes:
                    self.quizzes = default_quizzes
        except Exception:
            print("\n⚠️ 데이터 파일이 손상되었습니다. 기본 퀴즈로 복구합니다.")
            self.quizzes = default_quizzes
            self.best_score = 0

    def save_data(self):
        """현재 퀴즈 목록과 최고 점수를 JSON 파일에 UTF-8로 저장"""
        try:
            with open(self.file_name, "w", encoding="utf-8") as f:
                data = {
                    "quizzes": [q.to_dict() for q in self.quizzes],
                    "best_score": self.best_score
                }
                json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"\n⚠️ 데이터 저장 중 오류가 발생했습니다: {e}")

    def get_valid_input(self, prompt, valid_range=None):
        """요구사항 충족: 공백 제거, 숫자 예외 처리, 비정상 종료 방지"""
        while True:
            try:
                user_input = input(prompt).strip()
                if not user_input:
                    print("⚠️ 빈 입력입니다. 다시 입력해주세요.")
                    continue
                
                value = int(user_input)
                if valid_range and value not in valid_range:
                    print(f"⚠️ 잘못된 입력입니다. {valid_range[0]}~{valid_range[-1]} 사이의 숫자를 입력해주세요.")
                    continue
                return value
            
            except ValueError:
                print("⚠️ 잘못된 입력입니다. 숫자로 입력해주세요.")
            except (KeyboardInterrupt, EOFError):
                print("\n\n프로그램을 안전하게 종료합니다. 데이터가 저장되었습니다.")
                self.save_data()
                sys.exit(0)

    def play_quiz(self):
        """1. 퀴즈 풀기 기능"""
        if not self.quizzes:
            print("\n등록된 퀴즈가 없습니다.")
            return

        print(f"\n📝 퀴즈를 시작합니다! (총 {len(self.quizzes)}문제)")
        score = 0

        try:
            for i, quiz in enumerate(self.quizzes, 1):
                print("-" * 40)
                print(f"[{i}번 문제] {quiz.question}")
                for j, choice in enumerate(quiz.choices, 1):
                    print(f"  {j}. {choice}")
                
                answer = self.get_valid_input("\n정답 입력 (1-4): ", range(1, 5))
                if answer == quiz.answer:
                    print("✅ 정답입니다!")
                    score += 1
                else:
                    print(f"❌ 틀렸습니다! 정답은 {quiz.answer}번입니다.")
            
            print("=" * 40)
            score_percent = int(score / len(self.quizzes) * 100)
            print(f"🏆 결과: {len(self.quizzes)}문제 중 {score}문제 정답! ({score_percent}점)")
            
            if score > self.best_score:
                print("🎉 새로운 최고 점수입니다!")
                self.best_score = score
                self.save_data()
            print("=" * 40)
        
        except (KeyboardInterrupt, EOFError):
            print("\n\n퀴즈 풀기가 중단되었습니다. 메인 메뉴로 돌아갑니다.")
            self.save_data()

    def add_quiz(self):
        """2. 퀴즈 추가 기능"""
        print("\n📌 새로운 퀴즈를 추가합니다.")
        try:
            while True:
                question = input("문제를 입력하세요: ").strip()
                if question:
                    break
                print("⚠️ 문제는 비워둘 수 없습니다.")
            
            choices = []
            for i in range(1, 5):
                while True:
                    choice = input(f"선택지 {i}: ").strip()
                    if choice:
                        choices.append(choice)
                        break
                    print("⚠️ 선택지는 비워둘 수 없습니다.")
            
            answer = self.get_valid_input("정답 번호 (1-4): ", range(1, 5))
            
            new_quiz = Quiz(question, choices, answer)
            self.quizzes.append(new_quiz)
            self.save_data()
            print("\n✅ 퀴즈가 추가되고 저장되었습니다!")
            
        except (KeyboardInterrupt, EOFError):
            print("\n\n퀴즈 추가가 취소되었습니다.")
            self.save_data()

    def show_list(self):
        """3. 퀴즈 목록 보기 기능"""
        print(f"\n📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")
        print("-" * 40)
        for i, quiz in enumerate(self.quizzes, 1):
            print(f"[{i}] {quiz.question}")
        print("-" * 40)

    def show_score(self):
        """4. 점수 확인 기능"""
        print(f"\n🏆 최고 정답 수: {self.best_score}개")

    def run(self):
        """메인 메뉴 실행 흐름"""
        print("📂 퀴즈 게임 데이터를 준비했습니다.")
        while True:
            print("\n" + "=" * 40)
            print("        🎯 나만의 퀴즈 게임 🎯")
            print("=" * 40)
            print("1. 퀴즈 풀기")
            print("2. 퀴즈 추가")
            print("3. 퀴즈 목록")
            print("4. 점수 확인")
            print("5. 종료")
            print("=" * 40)
            
            choice = self.get_valid_input("선택: ", range(1, 6))
            
            if choice == 1:
                self.play_quiz()
            elif choice == 2:
                self.add_quiz()
            elif choice == 3:
                self.show_list()
            elif choice == 4:
                self.show_score()
            elif choice == 5:
                print("\n게임을 종료합니다. 데이터가 안전하게 저장되었습니다.")
                self.save_data()
                break

if __name__ == "__main__":
    game = QuizGame()
    game.run()