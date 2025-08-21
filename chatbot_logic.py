import json
from sentence_transformers import SentenceTransformer, util

# Load dataset
with open("dataset.json", "r") as f:
    data = json.load(f)["questions"]

# Extract questions and answers
corpus = [item["q"] for item in data]
answers = [item["a"] for item in data]

# Load sentence transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Precompute embeddings for all dataset questions
corpus_embeddings = model.encode(corpus, convert_to_tensor=True)

def get_bot_response(user_input):
    """
    Returns the most relevant answer from the dataset for the user's input.
    Uses semantic similarity via sentence embeddings.
    """
    # Encode the user's input
    user_embedding = model.encode(user_input, convert_to_tensor=True)

    # Compute cosine similarity between input and all dataset questions
    similarities = util.cos_sim(user_embedding, corpus_embeddings)[0]

    # Find the best match
    max_score = similarities.max().item()
    max_index = similarities.argmax().item()

    # Threshold to decide if a match is confident enough
    if max_score > 0.6:  # you can tweak this threshold
        return answers[max_index]
    else:
        return "Sorry, I didn't understand that. Please rephrase or contact admin."

# Example usage
if __name__ == "__main__":
    print("College Chatbot (type 'exit' to quit)")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        response = get_bot_response(user_input)
        print("Bot:", response)
