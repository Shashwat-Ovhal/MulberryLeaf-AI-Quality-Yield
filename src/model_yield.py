import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

class YieldModel:
    def __init__(self):
        # We expect input features: [Avg_Quality_Score, Temperature, Humidity]
        self.model = Pipeline([
            ('scaler', StandardScaler()),
            ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
        ])
        
    def train(self, X, y):
        """
        Trains the regression model.
        Args:
            X: Feature matrix (pandas DataFrame or numpy array)
            y: Target vector
        """
        self.model.fit(X, y)
        
    def predict(self, X):
        return self.model.predict(X)
        
    def save(self, path):
        joblib.dump(self.model, path)
        
    @staticmethod
    def load(path):
        loaded = YieldModel()
        loaded.model = joblib.load(path)
        return loaded
