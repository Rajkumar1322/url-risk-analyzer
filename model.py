from sklearn.ensemble import RandomForestClassifier

# Sample training data
X = [
    [1, 0, 0, 0, 0],  # safe
    [0, 1, 1, 1, 1],  # phishing
    [0, 1, 0, 1, 1],
    [1, 0, 0, 0, 1]
]

y = [0, 1, 1, 0]

model = RandomForestClassifier()
model.fit(X, y)

def predict(features):
    result = model.predict([features])[0]
    prob = model.predict_proba([features])[0][1]
    return result, prob