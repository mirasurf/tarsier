# Trigger the download of the yolox model
# Ref: https://docs.unstructured.io/open-source/concepts/models
from unstructured_inference.models.base import get_model
from unstructured_inference.inference.layout import DocumentLayout

model = get_model("yolox")
DocumentLayout.from_file("testdata/embedded-images.pdf", detection_model=model)
print("unstructured models loaded!")

# preload NTLK data.
import nltk

nltk.download("punkt")
nltk.download("averaged_perceptron_tagger")
