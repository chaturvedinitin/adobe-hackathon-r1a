from sentence_transformers import SentenceTransformer

# This is a powerful and small model, perfect for this task.
model_name = 'all-MiniLM-L6-v2'
model = SentenceTransformer(model_name)

# Save the model to a local directory
model.save('models/all-MiniLM-L6-v2')

print(f"Model '{model_name}' downloaded and saved to 'models/' directory.")