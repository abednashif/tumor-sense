import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import applications

# Load the data
train_data_gen = ImageDataGenerator(rescale=1./255,
                                    shear_range=0.2,
                                    rotation_range=2,
                                    zoom_range=0.2,
                                    horizontal_flip=True,
                                    vertical_flip=True)
training_set = train_data_gen.flow_from_directory(directory="../../Datasets/BrainTumorSplitData_images/Training",
                                                  target_size=(224,224),
                                                  class_mode='categorical',
                                                  batch_size=32)

validation_data_gen = ImageDataGenerator(rescale=1./255)
validation_set = validation_data_gen.flow_from_directory(directory="../../Datasets/BrainTumorSplitData_images/Testing",
                                                        target_size=(224,224),
                                                        class_mode='categorical',
                                                        batch_size=32)

# Get all available Keras Applications models
all_models = [model for model in dir(applications) if callable(getattr(applications, model))]

# Test each model
results = {}
for model_name in all_models:
    if 'ResNet' in model_name or 'Inception' in model_name or 'Xception' in model_name or 'VGG' in model_name:  # These models require input shape (224, 224, 3)
        model = getattr(applications, model_name)(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
    else:
        continue  # Skip models that don't have (224, 224, 3) input shape

    x = model.output
    x = tf.keras.layers.GlobalAveragePooling2D()(x)
    x = tf.keras.layers.Dense(1024, activation='relu')(x)
    predictions = tf.keras.layers.Dense(training_set.num_classes, activation='softmax')(x)
    model = tf.keras.Model(inputs=model.input, outputs=predictions)

    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    history = model.fit(training_set, epochs=2, validation_data=validation_set)
    results[model_name] = history.history['val_accuracy']

    # Free up memory
    tf.keras.backend.clear_session()

# Display results
for model_name, accuracies in results.items():
    print(f"{model_name}: Mean Validation Accuracy: {sum(accuracies)/len(accuracies)}")
