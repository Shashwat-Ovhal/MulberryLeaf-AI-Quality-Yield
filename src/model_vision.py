import tensorflow as tf
from tensorflow.keras import layers, models, applications

class LeafQualityModel:
    def __init__(self, input_shape=(224, 224, 3), num_classes=3):
        self.input_shape = input_shape
        self.num_classes = num_classes
        self.model = self._build_model()
    
    def _build_model(self):
        """Builds the CNN using MobileNetV2 as input base."""
        base_model = applications.MobileNetV2(
            input_shape=self.input_shape,
            include_top=False,
            weights='imagenet'
        )
        base_model.trainable = False  # Freeze base layers for initial training

        model = models.Sequential([
            base_model,
            layers.GlobalAveragePooling2D(),
            layers.Dropout(0.2),
            layers.Dense(128, activation='relu'),
            layers.Dense(self.num_classes, activation='softmax')
        ])
        
        return model
    
    def compile(self, learning_rate=0.001):
        self.model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
    def summary(self):
        self.model.summary()
        
    def save(self, path):
        self.model.save(path)
    
    @staticmethod
    def preprocess_image(img_path, target_size=(224, 224)):
        """
        Loads and preprocesses a single image.
        Returns: numpy array of shape (1, 224, 224, 3)
        """
        # Load image
        img = tf.keras.utils.load_img(img_path, target_size=target_size)
        img_array = tf.keras.utils.img_to_array(img)
        
        # MobileNetV2 expects inputs [-1, 1], but check specific preprocessing
        # applications.mobilenet_v2.preprocess_input does scaling
        img_array = applications.mobilenet_v2.preprocess_input(img_array)
        img_array = tf.expand_dims(img_array, 0) # Create batch axis
        return img_array

if __name__ == "__main__":
    # Test instantation
    model = LeafQualityModel()
    model.summary()
    print("LeafQualityModel definition successful.")
