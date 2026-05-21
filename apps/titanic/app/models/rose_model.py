from sklearn.tree import DecisionTreeClassifier


class RoseModel:
    """생존 예측용 결정 트리 모델 (secom models 레이어와 동일 역할)."""

    def __init__(self) -> None:
        self.model = DecisionTreeClassifier(random_state=42)

    def get_model_name(self) -> str:
        return type(self.model).__name__
