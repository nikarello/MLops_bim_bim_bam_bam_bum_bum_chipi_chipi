import os  # Добавить эту строку
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

# Загрузка данных
data_path = "data/test_data.txt"
data = pd.read_csv(data_path)

# Предполагаем, что в данных есть 'features' и 'target'
X = data[['feature1', 'feature2']]
y = data['target']

# Разделение данных на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Обучение модели
model = LogisticRegression()
model.fit(X_train, y_train)

# Оценка модели
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy}")

# Проверяем, существует ли папка models/, если нет - создаем
model_dir = "models"
os.makedirs(model_dir, exist_ok=True)

# Сохранение модели
model_path = os.path.join(model_dir, "model.pkl")
joblib.dump(model, model_path)
