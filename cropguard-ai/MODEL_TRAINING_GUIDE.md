# CropGuard AI - Model Training Guide

## 🎯 Current Status

**Issue**: The AI service was using a dummy implementation that analyzed only image brightness, causing all images to get similar results.

**Solution**: Updated `ai_service.py` to:
- Load real TensorFlow/Keras models
- Properly preprocess images (RGB, resize to 224x224, normalize)
- Use improved fallback with RGB channel analysis
- Provide varied predictions based on image features

---

## 📋 What You Need to Do

### Option 1: Use a Pre-trained Model (Recommended for Quick Start)

If you have a trained model file (`.h5` or `.keras`):

1. **Create model directory**:
   ```bash
   mkdir model
   ```

2. **Place your model file**:
   - Copy your trained model to: `model/crop_disease_model.h5`
   - Or update `MODEL_PATH` in `backend/config.py`

3. **Update disease classes** in `backend/services/ai_service.py`:
   ```python
   CLASSES = [
       "Healthy",
       "Your Disease 1",
       "Your Disease 2",
       # ... add all your disease classes
   ]
   ```

4. **Restart the backend server**

### Option 2: Train Your Own Model

#### Step 1: Prepare Your Dataset

**Directory Structure**:
```
dataset/
├── train/
│   ├── Healthy/
│   │   ├── img1.jpg
│   │   ├── img2.jpg
│   │   └── ...
│   ├── Bacterial_Blight/
│   │   ├── img1.jpg
│   │   └── ...
│   ├── Brown_Spot/
│   └── ...
├── validation/
│   ├── Healthy/
│   ├── Bacterial_Blight/
│   └── ...
└── test/
    ├── Healthy/
    └── ...
```

**Requirements**:
- At least 100-200 images per disease class
- Images should be clear crop leaf photos
- Balanced dataset (similar number of images per class)

#### Step 2: Install Training Dependencies

```bash
pip install tensorflow keras matplotlib scikit-learn
```

#### Step 3: Train the Model

Create `train_model.py` in your project root:

```python
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os

# Configuration
IMG_SIZE = 224
BATCH_SIZE = 32
EPOCHS = 50
DATASET_PATH = "dataset"

# Disease classes (update based on your dataset)
CLASSES = [
    "Healthy",
    "Bacterial_Blight",
    "Brown_Spot",
    "Leaf_Blast",
    "Leaf_Scald",
    "Narrow_Brown_Spot"
]

# Data augmentation for training
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)

# Only rescaling for validation
val_datagen = ImageDataGenerator(rescale=1./255)

# Load training data
train_generator = train_datagen.flow_from_directory(
    os.path.join(DATASET_PATH, 'train'),
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='categorical'
)

# Load validation data
validation_generator = val_datagen.flow_from_directory(
    os.path.join(DATASET_PATH, 'validation'),
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='categorical'
)

# Build the model
def create_model(num_classes):
    base_model = keras.applications.MobileNetV2(
        input_shape=(IMG_SIZE, IMG_SIZE, 3),
        include_top=False,
        weights='imagenet'
    )
    
    # Freeze base model
    base_model.trainable = False
    
    # Add custom layers
    model = keras.Sequential([
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.Dense(256, activation='relu'),
        layers.Dropout(0.5),
        layers.Dense(num_classes, activation='softmax')
    ])
    
    return model

# Create and compile model
num_classes = len(CLASSES)
model = create_model(num_classes)

model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=0.001),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# Print model summary
model.summary()

# Train the model
history = model.fit(
    train_generator,
    epochs=EPOCHS,
    validation_data=validation_generator,
    callbacks=[
        keras.callbacks.EarlyStopping(
            monitor='val_loss',
            patience=5,
            restore_best_weights=True
        ),
        keras.callbacks.ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=3
        )
    ]
)

# Save the model
os.makedirs('model', exist_ok=True)
model.save('model/crop_disease_model.h5')
print("Model saved to model/crop_disease_model.h5")

# Evaluate on test set (if available)
if os.path.exists(os.path.join(DATASET_PATH, 'test')):
    test_datagen = ImageDataGenerator(rescale=1./255)
    test_generator = test_datagen.flow_from_directory(
        os.path.join(DATASET_PATH, 'test'),
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        class_mode='categorical'
    )
    
    test_loss, test_acc = model.evaluate(test_generator)
    print(f"Test accuracy: {test_acc:.4f}")
```

#### Step 4: Run Training

```bash
python train_model.py
```

This will:
- Load your dataset
- Train a MobileNetV2-based model
- Save the trained model to `model/crop_disease_model.h5`

#### Step 5: Update Disease Classes

After training, update the `CLASSES` list in `backend/services/ai_service.py` to match your dataset classes.

---

## 🔍 Testing the Model

### Test with Different Images

1. Upload various crop images
2. Check that predictions vary based on image content
3. Verify confidence scores make sense
4. Check severity levels

### Expected Behavior

**With Real Model**:
- Different images → Different predictions
- Confidence varies based on image clarity
- Predictions match trained disease classes

**With Fallback (No Model)**:
- Uses RGB channel analysis
- Green-dominant images → "Healthy"
- Dark/high-variation images → Disease predictions
- Still provides varied results

---

## 📊 Improving Model Accuracy

### 1. Collect More Data
- Aim for 500+ images per class
- Include various lighting conditions
- Different crop varieties
- Various disease stages

### 2. Data Augmentation
- Already included in training script
- Helps model generalize better

### 3. Fine-tuning
After initial training, unfreeze base model layers:

```python
# Unfreeze base model
base_model.trainable = True

# Recompile with lower learning rate
model.compile(
    optimizer=keras.optimizers.Adam(1e-5),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# Train for more epochs
model.fit(train_generator, epochs=20, validation_data=validation_generator)
```

### 4. Try Different Architectures
- ResNet50
- EfficientNet
- InceptionV3

---

## 🐛 Troubleshooting

### Model Not Loading

**Check**:
- Model file exists at correct path
- TensorFlow is installed: `pip install tensorflow`
- Check backend terminal for error messages

### Poor Predictions

**Possible causes**:
- Insufficient training data
- Imbalanced dataset
- Model not trained long enough
- Wrong image preprocessing

### Out of Memory

**Solutions**:
- Reduce batch size
- Use smaller model (MobileNetV2 instead of ResNet)
- Reduce image size to 128x128

---

## 📚 Recommended Datasets

### Public Crop Disease Datasets

1. **PlantVillage Dataset**
   - 54,000+ images
   - 38 disease classes
   - Available on Kaggle

2. **Rice Disease Dataset**
   - Specific to rice crops
   - Multiple disease types

3. **Tomato Disease Dataset**
   - Common tomato diseases
   - Well-labeled images

### Download from Kaggle

```bash
# Install kaggle CLI
pip install kaggle

# Download dataset (example)
kaggle datasets download -d vipoooool/new-plant-diseases-dataset
```

---

## ✅ Checklist

- [ ] Collect/download crop disease dataset
- [ ] Organize into train/validation/test folders
- [ ] Install TensorFlow: `pip install tensorflow`
- [ ] Run training script
- [ ] Model saved to `model/crop_disease_model.h5`
- [ ] Update `CLASSES` in `ai_service.py`
- [ ] Restart backend server
- [ ] Test with various images
- [ ] Verify predictions are varied and accurate

---

## 🚀 Quick Test (Without Training)

The improved fallback will now give you **varied predictions** based on:
- RGB channel analysis
- Green dominance (healthy plants are greener)
- Brightness and variation
- Random selection within categories

This is much better than the old brightness-only approach, but **training a real model is highly recommended** for production use.

---

## 📞 Need Help?

Common issues and solutions are in the main `TESTING_GUIDE.md`. Check backend terminal logs for detailed error messages.
