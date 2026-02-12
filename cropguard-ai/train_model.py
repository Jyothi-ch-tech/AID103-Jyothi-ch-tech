"""
CropGuard AI - Model Training Script
Train a crop disease classification model using your dataset
"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os
import sys

# ============ CONFIGURATION ============
# Update these based on your dataset
IMG_SIZE = 224
BATCH_SIZE = 32
EPOCHS = 30
DATASET_PATH = "dataset"  # Change this to your dataset path

# Disease classes - will be auto-detected from folder names
# But you can manually specify them here if needed
CLASSES = None  # Set to None for auto-detection

# ============ SETUP ============
print("=" * 60)
print("CropGuard AI - Model Training")
print("=" * 60)

# Check if dataset exists
if not os.path.exists(DATASET_PATH):
    print(f"\n❌ ERROR: Dataset not found at '{DATASET_PATH}'")
    print("\nPlease create a dataset with this structure:")
    print("dataset/")
    print("  ├── train/")
    print("  │   ├── Healthy/")
    print("  │   ├── Disease1/")
    print("  │   └── Disease2/")
    print("  └── validation/")
    print("      ├── Healthy/")
    print("      ├── Disease1/")
    print("      └── Disease2/")
    sys.exit(1)

# ============ DATA PREPARATION ============
print("\n📁 Preparing data...")

# Data augmentation for training (helps prevent overfitting)
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=30,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    vertical_flip=True,
    fill_mode='nearest'
)

# Only rescaling for validation (no augmentation)
val_datagen = ImageDataGenerator(rescale=1./255)

# Load training data
train_generator = train_datagen.flow_from_directory(
    os.path.join(DATASET_PATH, 'train'),
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    shuffle=True
)

# Load validation data
validation_generator = val_datagen.flow_from_directory(
    os.path.join(DATASET_PATH, 'validation'),
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    shuffle=False
)

# Get number of classes and class names
num_classes = len(train_generator.class_indices)
class_names = list(train_generator.class_indices.keys())

print(f"\n✅ Dataset loaded successfully!")
print(f"   - Number of classes: {num_classes}")
print(f"   - Classes: {', '.join(class_names)}")
print(f"   - Training samples: {train_generator.samples}")
print(f"   - Validation samples: {validation_generator.samples}")

# ============ MODEL CREATION ============
print("\n🏗️  Building model...")

# Use MobileNetV2 as base (lightweight and accurate)
base_model = keras.applications.MobileNetV2(
    input_shape=(IMG_SIZE, IMG_SIZE, 3),
    include_top=False,
    weights='imagenet'  # Use pre-trained weights
)

# Freeze base model initially
base_model.trainable = False

# Build complete model
model = keras.Sequential([
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dropout(0.3),
    layers.Dense(256, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(num_classes, activation='softmax')
])

# Compile model
model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=0.001),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

print("\n📊 Model architecture:")
model.summary()

# ============ TRAINING ============
print("\n🚀 Starting training...")
print(f"   - Epochs: {EPOCHS}")
print(f"   - Batch size: {BATCH_SIZE}")
print(f"   - Image size: {IMG_SIZE}x{IMG_SIZE}")

# Callbacks for better training
callbacks = [
    # Stop if validation loss doesn't improve
    keras.callbacks.EarlyStopping(
        monitor='val_loss',
        patience=5,
        restore_best_weights=True,
        verbose=1
    ),
    # Reduce learning rate if stuck
    keras.callbacks.ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.5,
        patience=3,
        min_lr=1e-7,
        verbose=1
    ),
    # Save best model during training
    keras.callbacks.ModelCheckpoint(
        'model/best_model_checkpoint.h5',
        monitor='val_accuracy',
        save_best_only=True,
        verbose=1
    )
]

# Create model directory
os.makedirs('model', exist_ok=True)

# Train the model
history = model.fit(
    train_generator,
    epochs=EPOCHS,
    validation_data=validation_generator,
    callbacks=callbacks,
    verbose=1
)

# ============ FINE-TUNING (Optional but recommended) ============
print("\n🔧 Fine-tuning model...")

# Unfreeze the base model
base_model.trainable = True

# Recompile with lower learning rate
model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=1e-5),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# Train for a few more epochs
fine_tune_epochs = 10
print(f"   - Fine-tuning for {fine_tune_epochs} more epochs...")

history_fine = model.fit(
    train_generator,
    epochs=fine_tune_epochs,
    validation_data=validation_generator,
    callbacks=callbacks,
    verbose=1
)

# ============ SAVE MODEL ============
print("\n💾 Saving model...")

# Save final model
model.save('model/crop_disease_model.h5')
print("   ✅ Model saved to: model/crop_disease_model.h5")

# Save class names for reference
with open('model/class_names.txt', 'w') as f:
    for class_name in class_names:
        f.write(f"{class_name}\n")
print("   ✅ Class names saved to: model/class_names.txt")

# ============ EVALUATION ============
print("\n📈 Evaluating model...")

# Evaluate on validation set
val_loss, val_accuracy = model.evaluate(validation_generator)
print(f"\n   Final Validation Accuracy: {val_accuracy*100:.2f}%")
print(f"   Final Validation Loss: {val_loss:.4f}")

# Test on test set if available
if os.path.exists(os.path.join(DATASET_PATH, 'test')):
    print("\n🧪 Testing on test set...")
    test_datagen = ImageDataGenerator(rescale=1./255)
    test_generator = test_datagen.flow_from_directory(
        os.path.join(DATASET_PATH, 'test'),
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        shuffle=False
    )
    
    test_loss, test_accuracy = model.evaluate(test_generator)
    print(f"\n   Test Accuracy: {test_accuracy*100:.2f}%")
    print(f"   Test Loss: {test_loss:.4f}")

# ============ INSTRUCTIONS ============
print("\n" + "=" * 60)
print("✅ TRAINING COMPLETE!")
print("=" * 60)
print("\nNext steps:")
print("1. Check model/crop_disease_model.h5 - this is your trained model")
print("2. Update CLASSES in backend/services/ai_service.py:")
print(f"   CLASSES = {class_names}")
print("3. Restart your backend server")
print("4. Test with real images!")
print("\nModel location: model/crop_disease_model.h5")
print("=" * 60)
