"""
CropGuard AI - Train Model with Plant Disease Dataset
Optimized for the downloaded Kaggle dataset
"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os
import sys

# Configuration
IMG_SIZE = 224
BATCH_SIZE = 32
EPOCHS = 20  # Reduced for faster training
DATASET_PATH = "New Plant Diseases Dataset(Augmented)/New Plant Diseases Dataset(Augmented)"

print("=" * 70)
print("CropGuard AI - Model Training")
print("=" * 70)

# Check GPU availability
gpus = tf.config.list_physical_devices('GPU')
if gpus:
    print(f"\n✅ GPU detected: {len(gpus)} GPU(s) available")
    print("   Training will be faster!")
else:
    print("\n⚠️  No GPU detected - training will use CPU")
    print("   This may take 1-2 hours")

# Data preparation
print("\n📁 Loading dataset...")

train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.15,
    zoom_range=0.15,
    horizontal_flip=True,
    fill_mode='nearest'
)

val_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
    os.path.join(DATASET_PATH, 'train'),
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    shuffle=True
)

validation_generator = val_datagen.flow_from_directory(
    os.path.join(DATASET_PATH, 'valid'),
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    shuffle=False
)

num_classes = len(train_generator.class_indices)
class_names = list(train_generator.class_indices.keys())

print(f"\n✅ Dataset loaded!")
print(f"   Classes: {num_classes}")
print(f"   Training images: {train_generator.samples}")
print(f"   Validation images: {validation_generator.samples}")

# Build model
print("\n🏗️  Building model (MobileNetV2)...")

base_model = keras.applications.MobileNetV2(
    input_shape=(IMG_SIZE, IMG_SIZE, 3),
    include_top=False,
    weights='imagenet'
)

base_model.trainable = False

model = keras.Sequential([
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dropout(0.3),
    layers.Dense(256, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(num_classes, activation='softmax')
])

model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=0.001),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

print("✅ Model built successfully!")

# Training
print(f"\n🚀 Starting training ({EPOCHS} epochs)...")
print("   This may take 30-60 minutes...")

os.makedirs('cropguard-ai/model', exist_ok=True)

callbacks = [
    keras.callbacks.EarlyStopping(
        monitor='val_loss',
        patience=3,
        restore_best_weights=True,
        verbose=1
    ),
    keras.callbacks.ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.5,
        patience=2,
        min_lr=1e-7,
        verbose=1
    ),
    keras.callbacks.ModelCheckpoint(
        'cropguard-ai/model/best_checkpoint.h5',
        monitor='val_accuracy',
        save_best_only=True,
        verbose=1
    )
]

history = model.fit(
    train_generator,
    epochs=EPOCHS,
    validation_data=validation_generator,
    callbacks=callbacks,
    verbose=1
)

# Fine-tuning
print("\n🔧 Fine-tuning model...")
base_model.trainable = True

model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=1e-5),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

history_fine = model.fit(
    train_generator,
    epochs=5,
    validation_data=validation_generator,
    callbacks=callbacks,
    verbose=1
)

# Save model
print("\n💾 Saving model...")
model.save('cropguard-ai/model/crop_disease_model.h5')
print("   ✅ Model saved: cropguard-ai/model/crop_disease_model.h5")

# Save class names
with open('cropguard-ai/model/class_names.txt', 'w') as f:
    for name in class_names:
        f.write(f"{name}\n")
print("   ✅ Class names saved: cropguard-ai/model/class_names.txt")

# Evaluation
val_loss, val_accuracy = model.evaluate(validation_generator)

print("\n" + "=" * 70)
print("✅ TRAINING COMPLETE!")
print("=" * 70)
print(f"\nFinal Validation Accuracy: {val_accuracy*100:.2f}%")
print(f"Final Validation Loss: {val_loss:.4f}")
print(f"\nModel location: cropguard-ai/model/crop_disease_model.h5")
print(f"Number of disease classes: {num_classes}")
print("\nNext steps:")
print("1. Model is ready to use!")
print("2. Restart your backend server")
print("3. Test with crop images")
print("=" * 70)
