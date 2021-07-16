import os
from facemorpher import morpher

def morph_emotion_images(emotion, subjects):
    """
    1. Generate morphed images using face morpher
    2. Rename target images indicating morphing level : frame010 -> 25, frame020 -> 50, frame030 -> 75
    3. Remove other unused images
    """
    
    head_direction = 'Rafd090'
    eye_direction = 'frontal'
    
    for subject in subjects:
        
        print('[INFO] Processing', subject...)
        
        ID = subject.split('_')[0]
        
        output_folder_emotion = os.path.join(output_dir, ID, emotion)  # for saving neutral faces
        output_folder_neutral = os.path.join(output_dir, ID, 'neutral')
        check_folder_exists(output_folder_emotion)
        check_folder_exists(output_folder_neutral)
        
        # Generate morphed image pairs
        img_neutral = os.path.join(image_root, f'{head_direction}_{subject}_neutral_{eye_direction}.jpg')
        img_emotion = os.path.join(image_root, f'{head_direction}_{subject}_{emotion}_{eye_direction}.jpg')
        
        # Morph neutral and images with emotions
        imgs = [img_neutral, img_emotion]
        
        
        morpher(imgs, out_frames=output_folder_emotion, num_frames=40)
        rename_target_images(emotion, subject, output_folder_emotion, type='morph')
        remove_unused_images(emotion, output_folder_emotion)
        
        
        # Morph neutral images in order to crop images 
        imgs = [img_neutral, img_neutral]
        morpher(imgs, out_frames=output_folder_neutral, num_frames=3)
        rename_target_images(emotion, subject, output_folder_neutral, type='neutral')
        remove_unused_images(emotion, output_folder_neutral)
        
        
        # Morph raw images
        imgs = [img_emotion, img_emotion]
        morpher(imgs, out_frames=output_folder_emotion, num_frames=3)
        rename_target_images(emotion, subject, output_folder_emotion, type='raw')
        remove_unused_images(emotion, output_folder_emotion)
        
        
        
def rename_target_images(emotion, subject, output_folder, type):
    
    if type == 'morph':    
        old2new = {
            'frame010.png': f'{emotion}_25.png',
            'frame020.png': f'{emotion}_50.png',
            'frame030.png': f'{emotion}_75.png'
        }
                
    elif type == 'neutral':
        old2new = {'frame001.png': 'neutral_0.png'}

    elif type == 'raw':
        old2new = {'frame001.png': f'{emotion}_100.png'}

        
    for oldname, newname in old2new.items():
        old_image = os.path.join(output_folder, oldname)
        new_image = os.path.join(output_folder, f'{subject}_{newname}')

        if os.path.exists(old_image):
            os.rename(old_image, new_image)
            
                
def remove_unused_images(emotion, output_folder):
    
    remove_targets = [f'frame{i:03}.png' for i in range(40)]
    
    for target in remove_targets:
        
        image_path = os.path.join(output_folder, target)
        
        if os.path.exists(image_path):
            os.remove(image_path)
            

if __name__ == '__main__':
            
    image_root = '/WHERE/YOU/SAVE/IMAGES/'
    output_dir = '/WHERE/YOU/WANT/TO/SAVE/MORPHED/IMAGES/'

    files = os.listdir(image_root)

    subjects = set(['_'.join(file.split('_')[1:4]) for file in files])
    emotions = ['happy', 'sad', 'angry', 'surprised', 'fearful', 'disgusted']

    for emotion in emotions:
        print('Emotion:', emotion)
        morph_emotion_images(emotion, subjects)
        print()