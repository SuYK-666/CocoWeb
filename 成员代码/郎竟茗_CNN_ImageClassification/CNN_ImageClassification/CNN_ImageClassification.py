import os
import cv2
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow.keras import layers, models, optimizers
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.metrics import confusion_matrix
import seaborn as sns
# 数据集
base_path = r'D:\Downloads\EZ猫狗分类\cats_and_dogs_filtered'
train_dir = os.path.join(base_path, 'train')
val_dir = os.path.join(base_path, 'validation')
# 常用训练参数
img_size = (150, 150)
batch_size = 32
epochs = 10 

# 训练集数据增强，，防过拟合
train_datagen = ImageDataGenerator(
    rescale=1./255,          
    rotation_range=25,       
    width_shift_range=0.15,  
    height_shift_range=0.15, 
    horizontal_flip=True,    # 左右翻转
    fill_mode='nearest')
# 验证集直接归一化
val_datagen = ImageDataGenerator(rescale=1./255)
# 从文件夹抓图，打标签
train_gen = train_datagen.flow_from_directory(
    train_dir,
    target_size=img_size,
    batch_size=batch_size,
    class_mode='binary')# 猫狗二分类，binary
val_gen = val_datagen.flow_from_directory(
    val_dir,
    target_size=img_size,
    batch_size=batch_size,
    class_mode='binary')


# CNN网络结构
my_model = models.Sequential([
    # 第一层卷积
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(150, 150, 3)),
    layers.MaxPooling2D(2, 2),
    # 第二层
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D(2, 2),
    # 第三层和第四层
    layers.Conv2D(128, (3, 3), activation='relu'),
    layers.MaxPooling2D(2, 2), 
    layers.Conv2D(128, (3, 3), activation='relu'),
    layers.MaxPooling2D(2, 2),
    layers.Flatten(),
    # dropout一半神经元，防过拟合
    layers.Dropout(0.5), 
    layers.Dense(512, activation='relu'),# 512个神经元
    layers.Dense(1, activation='sigmoid')# 输出狗的概率（0猫，1狗）
])
my_model.compile(
    optimizer=optimizers.Adam(learning_rate=1e-4),
    loss='binary_crossentropy',
    metrics=['accuracy']
)# Adam优化器
my_model.summary()

#训练
print("\n--- 开始训练 ---")
history = my_model.fit(
    train_gen,
    epochs=epochs,
    validation_data=val_gen)
#存模型
my_model.save('cat_dog_model.h5')
#训练效果check
acc = history.history['accuracy']
val_acc = history.history['val_accuracy']
loss = history.history['loss']
val_loss = history.history['val_loss']
plt.figure(figsize=(10, 4))
#准确率曲线
plt.subplot(1, 2, 1)
plt.plot(acc, label='Train Acc')
plt.plot(val_acc, label='Val Acc')
plt.title('Accuracy')
plt.legend()
#损失曲线
plt.subplot(1, 2, 2)
plt.plot(loss, label='Train Loss')
plt.plot(val_loss, label='Val Loss')
plt.title('Loss')
plt.legend()
plt.show()

# Grad-CAM 可视化
def plot_gradcam(model, img_array):
    last_conv_layer = 'conv2d_3'# 最后一个卷积层
    # build临时模型，输出卷积层特征和预测值
    grad_model = models.Model([model.inputs], [model.get_layer(last_conv_layer).output, model.output])
    with tf.GradientTape() as tape:
        conv_output, preds = grad_model(img_array)
        loss = preds[:, 0]
    grads = tape.gradient(loss, conv_output)# 求梯度
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
    conv_output = conv_output[0]
    heatmap = conv_output @ pooled_grads[..., tf.newaxis]
    heatmap = tf.squeeze(heatmap)
    heatmap = np.maximum(heatmap, 0) / np.max(heatmap)# 归一化
    plt.matshow(heatmap.numpy())
    plt.title('Grad-CAM图')
    plt.show()

#show数据结果
sample_batch, _ = next(val_gen)# 随机抽一张图测试
plot_gradcam(my_model, sample_batch[0:1])
val_gen.reset()#混淆矩阵图
y_true = val_gen.classes
predictions = my_model.predict(val_gen)
y_pred = np.where(predictions > 0.5, 1, 0)
cm = confusion_matrix(y_true, y_pred)
plt.figure(figsize=(6, 5))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',xticklabels=['Cat', 'Dog'], yticklabels=['Cat', 'Dog'])
plt.title('Confusion Matrix')
plt.ylabel('True Label')
plt.xlabel('Pred Label')
plt.show()