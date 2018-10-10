# -*- coding: utf-8 -*-

"""
Created on Tue Sep  11 15:42 2018

@author: deepchem
"""

from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals
import os
import deepchem as dc
import pandas as pd
from tf_features import tf_descriptors
from deepchem.data import DiskDataset

def load_tf(samp_num=0,
            reload=True,
            split='random',
            frac_train_and_valid=0.9,
            data_time=10,
            data_num=1,
            data_dir='/home/hdd2/lifei/sam/script/tmm/data'):
    tf_tasks = ['values']
    dataset_file = (data_dir + "/fingerprint_" + str(samp_num) + '.csv')
    
    save_dir=os.path.join(os.path.dirname(dataset_file), '.'.join(os.path.basename(dataset_file).split('.')[:-1]))
    dataset_dir,test_dir = os.path.join(save_dir,'dataset'), os.path.join(save_dir,'test')
    
    if os.path.isdir(save_dir):
        if reload:
            dataset,train_dataset, valid_dataset, test_dataset =DiskDataset(data_dir=dataset_dir), DiskDataset(data_dir=os.path.join(save_dir,('train_vaild_'+ str(data_num)),'train')), DiskDataset(data_dir=os.path.join(save_dir,('train_vaild_'+ str(data_num)),'valid')),DiskDataset(data_dir=test_dir)
            all_dataset = (dataset,train_dataset, valid_dataset, test_dataset)
            return all_dataset
    else:
        print("About to featurize TF dataset.")
        featurizer = dc.feat.UserDefinedFeaturizer(tf_descriptors)
        loader = dc.data.UserCSVLoader(
            tasks=tf_tasks, id_field="compounds", featurizer=featurizer)
        if not os.path.exists(dataset_dir):
            os.makedirs(dataset_dir)
        dataset = loader.featurize(dataset_file, data_dir=dataset_dir,shard_size=8192)
        splitters = {
          'index': dc.splits.IndexSplitter(),
          'random': dc.splits.RandomSplitter(),
          'scaffold': dc.splits.ScaffoldSplitter()
          }
        splitter = splitters[split]
        if not os.path.exists(test_dir):
            os.makedirs(test_dir)
        train_valid, test_dataset = splitter.train_test_split(dataset,test_dir=test_dir, frac_train=frac_train_and_valid)
        test_df = pd.DataFrame(test_dataset.ids)
        test_df.to_csv(os.path.join(test_dir,'test.csv'))
        for i in range(data_time):
            train_valid_dir = os.path.join(save_dir,('train_vaild_'+ str(i+1)))
            train_dir,valid_dir = os.path.join(train_valid_dir,'train'),os.path.join(train_valid_dir,'valid')
            for i in (train_dir,valid_dir):
                if not os.path.exists(i):
                    os.makedirs(i)
            train_dataset_t,vaild_dataset_t = splitter.train_test_split(train_valid, train_dir=train_dir, test_dir=valid_dir, frac_train=8.0/9)
            train_df, vaild_df= pd.DataFrame(train_dataset_t.ids), pd.DataFrame(vaild_dataset_t.ids)
            train_df.to_csv(train_dir+'/train.csv')
            vaild_df.to_csv(valid_dir+'/valid.csv')
        train_dataset, valid_dataset = DiskDataset(data_dir=os.path.join(save_dir,('train_vaild_'+ str(data_num)),'train')), DiskDataset(data_dir=os.path.join(save_dir,('train_vaild_'+ str(data_num)),'valid'))
        all_dataset = (dataset,train_dataset, valid_dataset, test_dataset)
        return all_dataset

        
if __name__ == '__main__':
    load_tf(samp_num=1000, reload=True, split='random', frac_train_and_valid=0.9, data_time=10, data_num=1)