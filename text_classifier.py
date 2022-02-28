from typing import Any, Callable, Dict, List, Tuple

from special_k import SerializableModel


class TextClassifier(SerializableModel):
    def __init__(
            self,
            vectorizer: Callable[[str], str],
            classifier: Any,
            classes: List[str],
            validation_data: Dict[str, Any],
    ):
        super().__init__()
        # A function that vectorizes text, e.g. tf-idf
        self.vectorizer = vectorizer
        # Classifier is an sklearn model that classifies preprocessed text.
        self.classifier = classifier
        self.classes = classes
        # Validation data maps example input data to expected outputs
        self.validation_data = validation_data

    @property
    def _name(self) -> str:
        """(Required) Return the name of the model"""
        return "World's ok-est text classfier"

    @property
    def custom_serialization(self) -> Dict[str, Tuple[str]]:
        """(Required) Describe how this model should be serialized
        
        Return a mapping of model attributes to tuples containing the serializer for that attribute
        and the name of the file to serialize that attribute to.
        """
        return {
            # Serialize the vectorizer attribute using pickle, and write the result to `vectorizer.pkl`.
            "vectorizer": ("pickle", "vectorizer.pkl"),
            # Serialize the classifier attribute using the keras serializer, and write the result to `classifier.h5`.
            "classifier": ("jlib", "classifier.jlib"),
            # Serialize validation data with JSON and write the result to `validation_data.json`.
            "validation_data": ("json", "validation_data.json"),
        }

    def validate_model(self) -> None:
        """"(Required) Validate that the model is working properly"""
        for input_datum, expected_output in self.validation_data.items():
            prediction = self.predict(input_datum)
            if prediction != expected_output:
                raise AssertionError("Model prediction did not match expected output")

    def predict(self, text: str) -> str:
        """(Required) Use inputs of your choice to make a prediction"""
        preprocessed_text = self.vectorizer.transform([text])
        prediction = self.classifier.predict(preprocessed_text)[0]
        label = self.classes[prediction]
        return label
