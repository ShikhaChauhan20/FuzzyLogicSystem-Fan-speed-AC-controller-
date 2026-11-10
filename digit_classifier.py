import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.datasets import load_digits
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler

print("=== Task 1: Dataset Inspection ===")
digits = load_digits()

print(f"Original image shape: {digits.images.shape}")
print(f"Feature matrix shape (X): {digits.data.shape}")
print(f"Total number of samples: {digits.data.shape[0]}")
print(f"Feature dimensions per sample: {digits.data.shape[1]}")

unique, counts = np.unique(digits.target, return_counts=True)
print("\nClass distribution (Digit: Count):")
for digit, count in zip(unique, counts):
  print(f"  Digit {digit}: {count} samples")

X = digits.data
y = digits.target

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(
    f"\n=== Task 2: Train-Test Split ===\nTraining samples:"
    f" {X_train.shape[0]}, Testing samples: {X_test.shape[0]}"
)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
print(
    "=== Task 3: Standardization ===\nFeatures standardized using"
    " training-fitted StandardScaler."
)

k_values = [3, 5, 7, 9, 11]
results = {}

print("\n=== Tasks 4 & 5: Model Evaluation across k values ===")
for k in k_values:
  knn = KNeighborsClassifier(n_neighbors=k)
  knn.fit(X_train_scaled, y_train)
  y_pred = knn.predict(X_test_scaled)

  acc = accuracy_score(y_test, y_pred)
  prec = precision_score(y_test, y_pred, average="macro", zero_division=0)
  rec = recall_score(y_test, y_pred, average="macro", zero_division=0)
  f1 = f1_score(y_test, y_pred, average="macro", zero_division=0)

  results[k] = {
      "model": knn,
      "accuracy": acc,
      "precision": prec,
      "recall": rec,
      "f1": f1,
      "predictions": y_pred,
  }
  print(
      f"k = {k:2d} | Accuracy: {acc:.4f} | Precision: {prec:.4f} | Recall:"
      f" {rec:.4f} | Macro F1: {f1:.4f}"
  )

best_k = max(results, key=lambda k: results[k]["accuracy"])
print(
    f"\n>>> Optimal k identified: {best_k} with Accuracy:"
    f" {results[best_k]['accuracy']:.4f}"
)

print(f"\n=== Task 6: Confusion Matrix for Best k = {best_k} ===")
best_preds = results[best_k]["predictions"]
cm = confusion_matrix(y_test, best_preds)

plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", cbar=True)
plt.title(f"Confusion Matrix for k-NN (k = {best_k})")
plt.xlabel("Predicted Label")
plt.ylabel("True Label")
plt.tight_layout()
plt.show()

print(
    "=== Task 8: Generating Accuracy vs. k Graph (Close plot window to"
    " continue) ==="
)
accuracies = [results[k]["accuracy"] for k in k_values]

plt.figure(figsize=(8, 5))
plt.plot(
    k_values,
    accuracies,
    marker="o",
    linestyle="-",
    color="b",
    linewidth=2,
    markersize=8,
)
plt.title("Effect of k Value on k-NN Test Accuracy")
plt.xlabel("Value of k")
plt.ylabel("Test Accuracy")
plt.xticks(k_values)
plt.grid(True, linestyle="--", alpha=0.6)
plt.tight_layout()
plt.show()

print(
    "\n=== Task 9: Performance Comparison (Standardized vs. Non-Standardized)"
    " ==="
)
unscaled_accuracies = []
for k in k_values:
  knn_raw = KNeighborsClassifier(n_neighbors=k)
  knn_raw.fit(X_train, y_train)
  y_pred_raw = knn_raw.predict(X_test)
  unscaled_accuracies.append(accuracy_score(y_test, y_pred_raw))

print(f"{'k Value':<10} | {'Standardized Acc':<18} | {'Non-Standardized Acc'}")
print("-" * 52)
for k, scaled_acc, raw_acc in zip(k_values, accuracies, unscaled_accuracies):
  print(f"{k:<10} | {scaled_acc:<18.4f} | {raw_acc:.4f}")

print(
    "\n=== Task 10: Visualizing 5 Test Predictions (Close plot window to"
    " finish) ==="
)
fig, axes = plt.subplots(1, 5, figsize=(12, 3))
sample_indices = np.random.choice(len(y_test), 5, replace=False)

for i, idx in enumerate(sample_indices):
  img = X_test[idx].reshape(8, 8)
  true_label = y_test[idx]
  pred_label = best_preds[idx]

  axes[i].imshow(img, cmap="gray")
  axes[i].axis("off")
  color = "green" if true_label == pred_label else "red"
  axes[i].set_title(
      f"True: {true_label}\nPred: {pred_label}", color=color, fontsize=10
  )

plt.suptitle(
    f"Sample Digit Predictions using Optimal k = {best_k}", fontsize=12
)
plt.tight_layout()
plt.show()