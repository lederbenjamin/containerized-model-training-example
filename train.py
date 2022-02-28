import argparse
import logging

from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from special_k import save_model_to_tarball

from text_classifier import TextClassifier

logger = logging.getLogger("train.py")
logging.basicConfig(level=logging.INFO)


def main(model_serialization_path):
    ## Load our training data - two classes from the 20Newsgroups dataset
    CATEGORIES_TO_LOAD = (
        "rec.sport.baseball",
        "rec.sport.hockey",
    )

    logger.info("Loading data...")
    # The subset on which to train
    train_data = fetch_20newsgroups(subset="train", categories=CATEGORIES_TO_LOAD)
    X_train = train_data.data
    y_train = train_data.target
    class_names = train_data.target_names

    # The subset on which to make sure our model prediction hasn't changed
    test_data = fetch_20newsgroups(subset="test", categories=CATEGORIES_TO_LOAD)
    X_test = test_data.data[:10]

    logger.info("Done loading data, vectorizing...")
    # Let's define our preprocessing, and fit the preprocessor
    vectorizer = TfidfVectorizer()
    vectorized_train_data = vectorizer.fit_transform(X_train)

    logger.info("Training model...")
    # Train the model on preprocessed data
    classifier = LogisticRegression()
    classifier.fit(vectorized_train_data, y_train)

    logger.info("Generating validation data...")
    # Generate a list of our model predictions, so we know what it did at train times
    model_predictions = classifier.predict(vectorizer.transform(X_test))
    model_labels = [class_names[prediction] for prediction in model_predictions]
    model_validation_data = {text: label for text, label in zip(X_test, model_labels)}

    logger.info("Serializing Model...")
    # Create our serializable model, and dump it to file
    serializable_model = TextClassifier(
        vectorizer, classifier, class_names, model_validation_data
    )
    save_model_to_tarball(
        serializable_model,
        tarball_path=model_serialization_path,
        gpg_home_dir="./gnupg",
        signing_key_fingerprint="BB5A 3DD0 C7C7 FD8D FE63  A7DF 6ED0 3CAD 6BBE 4D54",
        passphrase="thisisapassphrase",
    )
    logger.info("Done.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Train a sports classifier on the 20 Newsgroups dataset."
    )
    parser.add_argument(
        "--model-serialization-path",
        dest="model_serialization_path",
        help="The path at which to serialize the trained model",
        default="text_classifier.tar.gz",
    )
    args = parser.parse_args()
    main(args.model_serialization_path)
