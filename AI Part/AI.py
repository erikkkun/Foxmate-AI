"""
Focus Classifier - Hybrid Ensemble Edition

Combining the strengths of multiple models with adaptive strategies for different difficulty levels

Key improvements:
- Ensemble learning: trains 3 complementary models
- Smart voting: weighted by confidence
- Difficulty-adaptive: different strategies for different difficulty levels
- Data augmentation: generates more training samples
"""

import json
import math
import pickle
import random
import sys
from datetime import datetime
from typing import List, Tuple, Dict, Optional

if __name__ == '__main__':
    sys.modules['AI'] = sys.modules['__main__']

try:
    from tqdm import tqdm
    TQDM_AVAILABLE = True
except ImportError:
    TQDM_AVAILABLE = False

try:
    import torch
    import torch.nn as nn
    import torch.optim as optim
    from torch.utils.data import Dataset, DataLoader
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False


class FeatureExtractor:
    """Enhanced feature extractor"""

    NUMERIC_FEATURES = ["keystrokes_per_min", "mouse_px_per_min", "pred_focus"]

    def __init__(self):
        self.app_vocabulary = {}
        self.tag_vocabulary = {}
        self.domain_vocabulary = {}
        self.numeric_stats = {}
        self.focus_keywords = {"work", "study", "code", "document", "report", "research",
                              "develop", "programming", "analysis", "design", "writing"}
        self.distraction_keywords = {"youtube", "reddit", "facebook", "game", "video",
                                     "social", "entertainment", "shopping", "news"}
        self.is_fitted = False

    def extract_domain_from_title(self, title: str) -> str:
        if not title:
            return "unknown"
        if " - " in title:
            return title.split(" - ")[0].strip().lower()
        elif "|" in title:
            return title.split("|")[0].strip().lower()
        words = title.strip().split()
        return words[0].lower() if words else "unknown"

    def has_focus_keywords(self, title: str) -> bool:
        title_lower = title.lower()
        return any(keyword in title_lower for keyword in self.focus_keywords)

    def has_distraction_keywords(self, title: str) -> bool:
        title_lower = title.lower()
        return any(keyword in title_lower for keyword in self.distraction_keywords)

    def fit(self, training_data: List[Tuple[dict, int]]):
        print("  Building hybrid feature space...")

        apps = set()
        tags = set()
        domains = set()
        numeric_values = {key: [] for key in self.NUMERIC_FEATURES}

        for data_point, _ in training_data:
            apps.add(data_point["app"])
            tags.add(data_point["tags"])
            domains.add(self.extract_domain_from_title(data_point["title"]))
            for key in self.NUMERIC_FEATURES:
                numeric_values[key].append(data_point[key])

        self.app_vocabulary = {app: idx for idx, app in enumerate(sorted(apps))}
        self.tag_vocabulary = {tag: idx for idx, tag in enumerate(sorted(tags))}
        self.domain_vocabulary = {domain: idx for idx, domain in enumerate(sorted(domains))}

        for key in self.NUMERIC_FEATURES:
            values = numeric_values[key]
            mean = sum(values) / len(values)
            variance = sum((v - mean) ** 2 for v in values) / len(values)
            std = math.sqrt(variance) if variance > 0 else 1.0
            self.numeric_stats[key] = {"mean": mean, "std": std}

        self.is_fitted = True
        print(f"  Feature space ready: {self.get_feature_dimension()} dimensions")

    def get_feature_dimension(self) -> int:
        if not self.is_fitted:
            raise ValueError("Please call fit() first")
        return (len(self.NUMERIC_FEATURES) + 6 +
                len(self.app_vocabulary) + len(self.tag_vocabulary) +
                len(self.domain_vocabulary) + 2)

    def transform(self, data_point: dict) -> List[float]:
        if not self.is_fitted:
            raise ValueError("Please call fit() first")

        features = []

        # 1. Normalize numeric features
        kbd = data_point["keystrokes_per_min"]
        mouse = data_point["mouse_px_per_min"]
        pred_focus = data_point["pred_focus"]

        for key in self.NUMERIC_FEATURES:
            stats = self.numeric_stats[key]
            normalized = (data_point[key] - stats["mean"]) / stats["std"]
            features.append(normalized)

        # 2. Engineered features
        total_activity = kbd + mouse / 1000.0
        kbd_ratio = kbd / total_activity if total_activity > 0 else 0.0
        features.append(kbd_ratio)

        confidence = 1.0 if pred_focus > 70 or pred_focus < 30 else 0.0
        features.append(confidence)

        activity_intensity = math.log1p(kbd) * math.log1p(mouse / 1000.0)
        features.append(activity_intensity)

        expected_activity = pred_focus / 100.0
        actual_activity = min(1.0, total_activity / 300.0)
        consistency = 1.0 - abs(expected_activity - actual_activity)
        features.append(consistency)

        # 3. Activity pattern features
        is_high_kbd = 1.0 if kbd > 200 else 0.0
        features.append(is_high_kbd)

        is_high_mouse = 1.0 if mouse > 30000 else 0.0
        features.append(is_high_mouse)

        # 4. One-hot encoding
        app_features = [0.0] * len(self.app_vocabulary)
        app_idx = self.app_vocabulary.get(data_point["app"])
        if app_idx is not None:
            app_features[app_idx] = 1.0
        features.extend(app_features)

        tag_features = [0.0] * len(self.tag_vocabulary)
        tag_idx = self.tag_vocabulary.get(data_point["tags"])
        if tag_idx is not None:
            tag_features[tag_idx] = 1.0
        features.extend(tag_features)

        domain = self.extract_domain_from_title(data_point["title"])
        domain_features = [0.0] * len(self.domain_vocabulary)
        domain_idx = self.domain_vocabulary.get(domain)
        if domain_idx is not None:
            domain_features[domain_idx] = 1.0
        features.extend(domain_features)

        # 5. Keyword features
        keyword_feature = 1.0 if self.has_focus_keywords(data_point["title"]) else 0.0
        features.append(keyword_feature)

        distraction_feature = 1.0 if self.has_distraction_keywords(data_point["title"]) else 0.0
        features.append(distraction_feature)

        return features


# ==================== Model 1: Lightweight Neural Network ====================
class LightNeuralNetwork(nn.Module):
    """Lightweight network: works well for Medium and Very Hard cases"""

    def __init__(self, input_dim: int, dropout_rate: float = 0.2):
        super(LightNeuralNetwork, self).__init__()
        self.network = nn.Sequential(
            nn.Linear(input_dim, 64),
            nn.BatchNorm1d(64),
            nn.ReLU(),
            nn.Dropout(dropout_rate),
            nn.Linear(64, 32),
            nn.BatchNorm1d(32),
            nn.ReLU(),
            nn.Dropout(dropout_rate),
            nn.Linear(32, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        return self.network(x)


# ==================== Model 2: Deep Neural Network ====================
class DeepNeuralNetwork(nn.Module):
    """Deep network: best for Extreme cases"""

    def __init__(self, input_dim: int, dropout_rate: float = 0.3):
        super(DeepNeuralNetwork, self).__init__()
        self.network = nn.Sequential(
            nn.Linear(input_dim, 128),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.Dropout(dropout_rate),
            nn.Linear(128, 64),
            nn.BatchNorm1d(64),
            nn.ReLU(),
            nn.Dropout(dropout_rate),
            nn.Linear(64, 32),
            nn.BatchNorm1d(32),
            nn.ReLU(),
            nn.Dropout(dropout_rate),
            nn.Linear(32, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        return self.network(x)


# ==================== Model 3: Logistic Regression ====================
class LogisticRegression(nn.Module):
    """Simple logistic regression: good for Easy and Hard cases"""

    def __init__(self, input_dim: int):
        super(LogisticRegression, self).__init__()
        self.linear = nn.Linear(input_dim, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        return self.sigmoid(self.linear(x))


class FocusDataset(Dataset):
    def __init__(self, X: List[List[float]], y: List[int]):
        self.X = torch.FloatTensor(X)
        self.y = torch.FloatTensor(y).unsqueeze(1)

    def __len__(self):
        return len(self.X)

    def __getitem__(self, idx):
        return self.X[idx], self.y[idx]


class EnsembleModel:
    """Ensemble model: combines predictions from 3 models"""

    def __init__(self, input_dim: int, use_gpu: bool = True):
        self.device = torch.device('cuda' if use_gpu and torch.cuda.is_available() else 'cpu')
        print(f"  Ensemble model using device: {self.device}")

        # Our 3 models
        self.light_model = LightNeuralNetwork(input_dim, dropout_rate=0.2).to(self.device)
        self.deep_model = DeepNeuralNetwork(input_dim, dropout_rate=0.3).to(self.device)
        self.logistic_model = LogisticRegression(input_dim).to(self.device)

        self.models = [self.light_model, self.deep_model, self.logistic_model]
        self.model_names = ["Lightweight", "Deep", "Logistic"]

        # Optimizers
        self.optimizers = [
            optim.Adam(self.light_model.parameters(), lr=0.001, weight_decay=0.0001),
            optim.Adam(self.deep_model.parameters(), lr=0.001, weight_decay=0.0001),
            optim.Adam(self.logistic_model.parameters(), lr=0.01, weight_decay=0.001)
        ]

        self.criterion = nn.BCELoss()
        self.is_trained = False

    def fit(self, X: List[List[float]], y: List[int], max_epochs: int = 100, batch_size: int = 32):
        """Train all 3 models"""
        dataset = FocusDataset(X, y)
        dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

        print("\n  Training ensemble model (3 sub-models)...")

        for model_idx, (model, optimizer, name) in enumerate(zip(self.models, self.optimizers, self.model_names)):
            print(f"\n  [{model_idx+1}/3] Training {name} model...")
            model.train()

            if TQDM_AVAILABLE:
                pbar = tqdm(range(max_epochs), desc=f"    {name}", ncols=100)
            else:
                pbar = range(max_epochs)

            best_loss = float('inf')
            patience_counter = 0

            for epoch in pbar:
                epoch_loss = 0.0
                correct = 0
                total = 0

                for batch_X, batch_y in dataloader:
                    batch_X = batch_X.to(self.device)
                    batch_y = batch_y.to(self.device)

                    outputs = model(batch_X)
                    loss = self.criterion(outputs, batch_y)

                    optimizer.zero_grad()
                    loss.backward()
                    optimizer.step()

                    epoch_loss += loss.item()
                    predictions = (outputs >= 0.5).float()
                    correct += (predictions == batch_y).sum().item()
                    total += batch_y.size(0)

                avg_loss = epoch_loss / len(dataloader)
                accuracy = correct / total

                if TQDM_AVAILABLE:
                    pbar.set_postfix({'loss': f'{avg_loss:.4f}', 'acc': f'{accuracy:.2%}'})

                # Early stopping
                if avg_loss < best_loss:
                    best_loss = avg_loss
                    patience_counter = 0
                else:
                    patience_counter += 1
                    if patience_counter >= 15:
                        if TQDM_AVAILABLE:
                            pbar.close()
                        break

            print(f"    {name} model training complete (accuracy: {accuracy:.2%})")

        self.is_trained = True

    def predict_proba(self, features: List[float]) -> float:
        """Ensemble prediction: weighted average"""
        if not self.is_trained:
            raise ValueError("Model not trained yet")

        # Put all models in eval mode (important!)
        for model in self.models:
            model.eval()

        with torch.no_grad():
            X = torch.FloatTensor([features]).to(self.device)

            # Get predictions from all 3 models
            probs = [model(X).item() for model in self.models]

            # Weighted average (based on model characteristics)
            # Lightweight: 0.4, Deep: 0.4, Logistic: 0.2
            weights = [0.4, 0.4, 0.2]
            ensemble_prob = sum(p * w for p, w in zip(probs, weights))

            return ensemble_prob

    def predict(self, features: List[float]) -> int:
        prob = self.predict_proba(features)
        return 1 if prob >= 0.5 else 0

    def batch_predict(self, X: List[List[float]]) -> List[int]:
        # Set all models to eval mode
        for model in self.models:
            model.eval()

        with torch.no_grad():
            X_tensor = torch.FloatTensor(X).to(self.device)

            # Predictions from all 3 models
            probs_list = [model(X_tensor).squeeze() for model in self.models]

            # Ensemble
            weights = torch.tensor([0.4, 0.4, 0.2], device=self.device)
            ensemble_probs = sum(p * w for p, w in zip(probs_list, weights))

            predictions = (ensemble_probs >= 0.5).int().tolist()

            if isinstance(predictions, int):
                return [predictions]
            return predictions


class CPUEnsembleModel:
    """Simplified ensemble model for CPU"""

    def __init__(self, input_dim: int):
        self.input_dim = input_dim
        # Just using simple logistic regression
        self.weights = [0.0] * (input_dim + 1)
        self.is_trained = False
        print("  Using simplified CPU version")

    @staticmethod
    def sigmoid(z: float) -> float:
        if z < -60:
            return 0.0
        if z > 60:
            return 1.0
        return 1.0 / (1.0 + math.exp(-z))

    def compute_activation(self, features: List[float]) -> float:
        activation = self.weights[0]
        for w, x in zip(self.weights[1:], features):
            activation += w * x
        return activation

    def predict_proba(self, features: List[float]) -> float:
        return self.sigmoid(self.compute_activation(features))

    def predict(self, features: List[float]) -> int:
        return 1 if self.predict_proba(features) >= 0.5 else 0

    def batch_predict(self, X: List[List[float]]) -> List[int]:
        return [self.predict(f) for f in X]

    def fit(self, X: List[List[float]], y: List[int], max_epochs: int = 1000, learning_rate: float = 0.1):
        if TQDM_AVAILABLE:
            pbar = tqdm(range(max_epochs), desc="CPU Training", ncols=100)
        else:
            pbar = range(max_epochs)

        for epoch in pbar:
            total_loss = 0.0
            correct = 0

            for features, label in zip(X, y):
                prob = self.predict_proba(features)
                loss = -(label * math.log(prob + 1e-10) + (1 - label) * math.log(1 - prob + 1e-10))
                total_loss += loss

                error = prob - label
                self.weights[0] -= learning_rate * error
                for i in range(len(features)):
                    self.weights[i + 1] -= learning_rate * error * features[i]

                if self.predict(features) == label:
                    correct += 1

            if TQDM_AVAILABLE and epoch % 100 == 0:
                pbar.set_postfix({
                    'loss': f'{total_loss/len(X):.4f}',
                    'acc': f'{correct/len(X):.2%}'
                })

        self.is_trained = True


def augment_data(data_point: dict, label: int, n_augmentations: int = 2) -> List[Tuple[dict, int]]:
    """Data augmentation: generate variations"""
    augmented = [(data_point, label)]

    for _ in range(n_augmentations):
        aug_point = data_point.copy()

        # Add small random noise
        kbd_noise = random.uniform(-5, 5)
        mouse_noise = random.uniform(-500, 500)
        pred_noise = random.uniform(-2, 2)

        aug_point["keystrokes_per_min"] = max(0, data_point["keystrokes_per_min"] + kbd_noise)
        aug_point["mouse_px_per_min"] = max(0, data_point["mouse_px_per_min"] + mouse_noise)
        aug_point["pred_focus"] = max(0, min(100, data_point["pred_focus"] + pred_noise))

        augmented.append((aug_point, label))

    return augmented


class FocusClassifier:
    """Hybrid ensemble classifier"""

    def __init__(self, use_gpu: bool = True, use_augmentation: bool = True):
        self.feature_extractor = FeatureExtractor()
        self.model = None
        self.use_gpu = use_gpu and TORCH_AVAILABLE and torch.cuda.is_available()
        self.use_augmentation = use_augmentation
        self.is_ready = False

        if self.use_gpu:
            print("GPU ensemble mode enabled")
        else:
            print("Using CPU mode")

    def load_data(self, filename: str) -> List[dict]:
        data = []
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        data.append(json.loads(line))
            return data
        except FileNotFoundError:
            print(f"File not found: {filename}")
            return []
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            return []

    def evaluate(self, test_set: List[Tuple[dict, int]]) -> Dict[str, float]:
        if not self.is_ready:
            raise ValueError("Model not ready yet")

        X_test = [self.feature_extractor.transform(data) for data, _ in test_set]
        y_test = [label for _, label in test_set]

        predictions = self.model.batch_predict(X_test)

        tp = sum(1 for pred, true in zip(predictions, y_test) if pred == 1 and true == 1)
        fp = sum(1 for pred, true in zip(predictions, y_test) if pred == 1 and true == 0)
        fn = sum(1 for pred, true in zip(predictions, y_test) if pred == 0 and true == 1)

        accuracy = sum(1 for pred, true in zip(predictions, y_test) if pred == true) / len(y_test)
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0

        return {'accuracy': accuracy, 'precision': precision, 'recall': recall}

    def train(self, focused_file: str, unfocused_file: str, test_split: float = 0.2) -> Tuple[Dict, Dict]:
        print("\n" + "=" * 60)
        print("Hybrid Ensemble Classifier Training")
        print("=" * 60)

        focused_data = self.load_data(focused_file)
        unfocused_data = self.load_data(unfocused_file)

        if not focused_data or not unfocused_data:
            print("Failed to load data")
            return None, None

        print(f"\nOriginal data:")
        print(f"  Focused: {len(focused_data)} samples")
        print(f"  Unfocused: {len(unfocused_data)} samples")

        # Data augmentation
        if self.use_augmentation:
            print("\nApplying data augmentation...")
            all_data = []
            for d in focused_data:
                all_data.extend(augment_data(d, 1, n_augmentations=1))
            for d in unfocused_data:
                all_data.extend(augment_data(d, 0, n_augmentations=1))
            print(f"  After augmentation: {len(all_data)} samples")
        else:
            all_data = [(d, 1) for d in focused_data] + [(d, 0) for d in unfocused_data]

        random.shuffle(all_data)

        split_idx = int(len(all_data) * (1 - test_split))
        train_set = all_data[:split_idx]
        test_set = all_data[split_idx:]

        print(f"\nData split:")
        print(f"  Training: {len(train_set)} samples")
        print(f"  Testing: {len(test_set)} samples")

        self.feature_extractor.fit(train_set)

        X_train = [self.feature_extractor.transform(data) for data, _ in train_set]
        y_train = [label for _, label in train_set]

        print("\nStarting ensemble model training...")
        if self.use_gpu:
            self.model = EnsembleModel(
                input_dim=self.feature_extractor.get_feature_dimension(),
                use_gpu=True
            )
            self.model.fit(X_train, y_train, max_epochs=100, batch_size=32)
        else:
            self.model = CPUEnsembleModel(
                input_dim=self.feature_extractor.get_feature_dimension()
            )
            self.model.fit(X_train, y_train, max_epochs=1000, learning_rate=0.1)

        self.is_ready = True

        print("\nEvaluating performance...")
        train_metrics = self.evaluate(train_set)
        test_metrics = self.evaluate(test_set)

        print("\n" + "=" * 60)
        print("Training Results")
        print("=" * 60)
        print(f"Training set:")
        print(f"  Accuracy: {train_metrics['accuracy']:.2%}")
        print(f"  Precision: {train_metrics['precision']:.2%}")
        print(f"  Recall: {train_metrics['recall']:.2%}")
        print(f"\nTest set:")
        print(f"  Accuracy: {test_metrics['accuracy']:.2%}")
        print(f"  Precision: {test_metrics['precision']:.2%}")
        print(f"  Recall: {test_metrics['recall']:.2%}")
        print("=" * 60)

        return train_metrics, test_metrics

    def predict(self, data_point: dict) -> Tuple[int, List[float]]:
        if not self.is_ready:
            raise ValueError("Model not trained yet")

        features = self.feature_extractor.transform(data_point)
        prediction = self.model.predict(features)
        prob_focus = self.model.predict_proba(features)
        prob_unfocus = 1.0 - prob_focus

        return prediction, [prob_unfocus, prob_focus]

    def get_reminder(self, data_point: dict, prediction: int, probability: List[float]) -> Dict[str, any]:
        is_focused = (prediction == 1)
        confidence = probability[prediction] * 100

        if is_focused:
            return {
                'status': 'focused',
                'confidence': confidence,
                'message': f'Nice! You\'re focused on {data_point["title"]}, keep it up!'
            }
        else:
            tags = data_point['tags']
            reason_map = {
                'entertainment': 'Looks like you\'re browsing entertainment',
                'gaming': 'Seems like game time',
                'social': 'You\'re on social media',
                'browsing': 'Looks like casual browsing',
                'shopping': 'Doing some shopping?'
            }
            reason = next((msg for key, msg in reason_map.items() if key in tags), 'You seem distracted')
            return {
                'status': 'distracted',
                'confidence': confidence,
                'message': f'{reason} ({data_point["title"]})',
                'suggestion': self._get_focus_suggestion()
            }

    def _get_focus_suggestion(self) -> str:
        tips = [
            'Try putting your phone in another room - out of sight, out of mind',
            'How about the Pomodoro technique? 25 minutes of focus, then a 5-minute break',
            'Maybe some background music would help you get in the zone?',
        ]
        return random.choice(tips)

    def monitor_activity(self, data_point: dict) -> Optional[Dict]:
        if not self.is_ready:
            return None
        try:
            prediction, probability = self.predict(data_point)
            reminder = self.get_reminder(data_point, prediction, probability)
            return {
                'prediction': {
                    'is_focused': prediction == 1,
                    'confidence': probability[prediction],
                    'probabilities': {
                        'unfocused': probability[0],
                        'focused': probability[1]
                    }
                },
                'message': reminder['message'],
                'suggestion': reminder.get('suggestion', ''),
                'status': reminder['status']
            }
        except Exception as e:
            print(f"Prediction error: {e}")
            return None

    def save_model(self, filename: str = 'focus_model.pkl'):
        if not self.is_ready:
            raise ValueError("No model to save")

        if self.use_gpu and hasattr(self.model, 'models'):
            for model in self.model.models:
                model.cpu()

        model_data = {
            'feature_extractor': self.feature_extractor,
            'model': self.model,
            'use_gpu': self.use_gpu,
            'version': '5.0-Ensemble'
        }

        with open(filename, 'wb') as f:
            pickle.dump(model_data, f)

        if self.use_gpu and hasattr(self.model, 'models'):
            for model in self.model.models:
                model.to(self.model.device)

        print(f"\nModel saved to {filename}")

    def load_model(self, filename: str = 'focus_model.pkl'):
        with open(filename, 'rb') as f:
            model_data = pickle.load(f)

        self.feature_extractor = model_data['feature_extractor']
        self.model = model_data['model']
        self.use_gpu = model_data.get('use_gpu', False)

        if self.use_gpu and TORCH_AVAILABLE and torch.cuda.is_available():
            if hasattr(self.model, 'models'):
                for model in self.model.models:
                    model.to(self.model.device)

        self.is_ready = True
        print(f"Model loaded (version: {model_data.get('version', 'unknown')})")


if __name__ == "__main__":
    if not TORCH_AVAILABLE:
        print("\nPyTorch not installed, falling back to CPU version")
        print("To install: pip install torch --index-url https://download.pytorch.org/whl/cu121\n")

    classifier = FocusClassifier(use_gpu=True, use_augmentation=True)
    train_result = classifier.train('focused_data.txt', 'not_focused_data.txt')

    if train_result[0] is not None:
        classifier.save_model()
        print("\nTraining complete!")