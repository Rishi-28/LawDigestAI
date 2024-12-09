from transformers import T5Tokenizer, T5ForConditionalGeneration

from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch



def generate_catchphrases(input_text, model_path):
    """
    Generate a summary of important phrases from a given text using a fine-tuned T5 model.

    Args:
        input_text (str): The text to process.
        model_path (str): Path to the fine-tuned T5 model and tokenizer.

    Returns:
        list: List of important phrases summarizing the text.
    """
    # Load the fine-tuned model and tokenizer
    tokenizer = T5Tokenizer.from_pretrained(model_path)
    model = T5ForConditionalGeneration.from_pretrained(model_path)

    # Define the prompt
    PROMPT = "Generate an abstract list of important phrases that summarize the case document: "
    full_input_text = f"{PROMPT}{input_text}"

    # Tokenize the input
    input_ids = tokenizer(full_input_text, return_tensors="pt", truncation=True, max_length=512).input_ids

    # Generate prediction
    outputs = model.generate(
        input_ids,
        max_length=128,
        num_beams=4,
        early_stopping=True,
        no_repeat_ngram_size=2,
        temperature=0.7
    )

    # Decode the output and split into a list of phrases
    output_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    phrases_list = [phrase.strip() for phrase in output_text.split(',')]

    return phrases_list



# Function to classify a single text
def classify_citation(text, model_path):
    """
    Classifies the input text into one of the predefined categories.

    Args:
        text (str): The input text to classify.
        model_path (str): The path to the fine-tuned LegalBERT model.
        category_labels (list): List of category labels.

    Returns:
        str: The predicted category for the input text.
    """
    # Load the tokenizer and model
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForSequenceClassification.from_pretrained(model_path)
    category_labels = ["Referred to", "Cited", "Applied", "Followed"]

    # Tokenize the input text
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    outputs = model(**inputs)

    # Get predicted class index
    predicted_class = torch.argmax(outputs.logits, dim=1).item()

    # Return the predicted category
    return category_labels[predicted_class]
