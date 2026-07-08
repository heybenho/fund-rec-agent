from sentence_transformers import SentenceTransformer

model = SentenceTransformer("BAAI/bge-small-en-v1.5")

test_strings = [
    "An endowment to support graduate students in the School of Journalism.",
    "An endowment to support undergraduate students in the Haas School of Business",
    "A current-use fund to support Professor Dawn Song's research."
]

embeddings = model.encode(test_strings)

print(embeddings.shape)
print(embeddings[0][:5])