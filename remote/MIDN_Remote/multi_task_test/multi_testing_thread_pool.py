#
# Example to run the pipeline concurrently
#
import sys
sys.path.insert(0, './cta-core-detection')

import gpu_configuration # load GPU configuration (modify as needed)

import inference as inf # load main library
import threading
from multiprocessing.dummy import Pool as ThreadPool

# Create two functions to run concurrently

def initLoadAndPred(input_file):
    print('prcoess start - {} '.format (input_file) ) 
    # init core prediction object
    corePred1 = inf.CorePredictor() 
    # corePred.loadAlignedBrainFromNpy( 'exampleData/leftAndFlippedRightBrain_sub-0151.npy' ) # load aligned brain as NPY file
    corePred1.loadAlignedBrainFromNifti( input_file ) # load aligned brain as Nifti file
    # Run normalization and ML model
    corePred1.normAndInfer()
    # Output examples
    corePred1.outputSummary2D(input_file.replace('.nii.gz','.png')) # 2D image
    print('prcoess stop - {} '.format (input_file) )
    return input_file.replace('.nii.gz','.png') +  ' - Processed '

p = ThreadPool(2)


input_files =['./cta-core-detection/exampleData/ctaAligned_sub-0151.nii.gz','./cta-core-detection/exampleData/ctaAligned_sub-0150.nii.gz']

results1 = p.map(initLoadAndPred,['./cta-core-detection/exampleData/ctaAligned_sub-0151.nii.gz'])
results2 = p.map(initLoadAndPred,['./cta-core-detection/exampleData/ctaAligned_sub-0150.nii.gz'])

p.close()
p.join()

print(results1)
print(results2)





