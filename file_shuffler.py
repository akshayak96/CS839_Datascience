import os
import random
from shutil import copyfile

files = []
dir_names = ['training_set', 'test_set']
for dir_name in dir_names:
    if os.path.isdir(dir_name):
        for file_name in os.listdir(dir_name):
            files.append(os.path.join(dir_name, file_name))

random.shuffle(files)
i = 0
for item in files:
    if i < 200:
        dst = os.path.join('training_2', 'markup_training_' + str(i) + '.txt')
    else:
        dst = os.path.join('test_2', 'markup_test_' + str(i) + '.txt')
    copyfile(item, dst)
    i += 1
