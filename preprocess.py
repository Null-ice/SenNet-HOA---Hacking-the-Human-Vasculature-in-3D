from glob import glob
import os


# mode = 'train' 
# data_dir = '/storage/blood-vessel-segmentation'

def prepare_datadirs(mode, data_dir, m):
    '''
    mode: 'train' or 'submit'
    '''
    if 'train' in mode:
        train_folder  = [
            'kidney_1_dense',
        ]
        
        valid_folder = [
            'kidney_3_dense'
        ]
        
        train_file = []
        train_mask = []
        valid_file = []
        valid_mask = []
        
        for image_folder in train_folder:
            f = glob(f'{data_dir}/train/{image_folder}/images/*.tif')
            f = sorted(f)
            train_file.append(f)
            
            if image_folder == 'kidney_3_dense':
                image_folder = 'kidney_3_sparse'
            
            if m == 'vessel':
                f = glob(f'{data_dir}/train/{image_folder}/labels/*.tif')
                f = sorted(f)
                train_mask.append(f)
                
            else:
                f = glob(f'/storage/{image_folder}/{image_folder}/kidney-mask/*.png')
                f = sorted(f)
                train_mask.append(f)
            
        for image_folder in valid_folder:
            if m == 'vessel':
                f = glob(f'{data_dir}/train/{image_folder}/labels/*.tif')
                f = sorted(f)
                valid_mask.append(f)
            
            else:
                f = glob(f'/storage/{image_folder}/{image_folder}/kidney-mask/*.png')
                f = sorted(f)
                valid_mask.append(f)

            if image_folder == 'kidney_3_dense':
                image_folder = 'kidney_3_sparse'
            
            f = glob(f'{data_dir}/train/{image_folder}/images/*.tif')
            f = sorted(f)
            valid_file.append(f)
            if image_folder == 'kidney_3_sparse':
                new_valid_file = []
                for mask_folder, image_folder in zip(valid_mask, valid_file):
                    mask_filenames = {os.path.splitext(os.path.basename(f))[0] for f in mask_folder}
                    filtered_images = [f for f in image_folder if os.path.splitext(os.path.basename(f))[0] in mask_filenames]
                    new_valid_file.append(filtered_images)
                valid_file = new_valid_file
        
        print('len(valid_file) :', len(valid_file[0]))
        print('len(valid_mask) :', len(valid_mask[0]))

        print('len(train_file) :', len(train_file[0]))
        print('len(train_mask) :', len(train_mask[0]))
        
        return train_file, train_mask, valid_file, valid_mask
            
            
    if 'submit' in mode:
        valid_file = []
        valid_folder = sorted(glob(f'{data_dir}/test/*'))
        for image_folder in valid_folder:
            f = sorted(glob(f'{image_folder}/images/*.tif'))
            valid_file.append(f)

        glob_file = glob(f'{data_dir}/kidney_5/images/*.tif')
        if len(glob_file)==3:
            mode = 'submit-fake' #fake submission to save gpu time when submitting
        
        return valid_file





