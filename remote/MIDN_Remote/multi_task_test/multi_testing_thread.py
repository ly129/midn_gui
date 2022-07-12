#
# Example to run the pipeline concurrently
#
import sys
sys.path.insert(0, './cta-core-detection')


import gpu_configuration # load GPU configuration (modify as needed)

import inference as inf # load main library
import threading
import multiprocessing

# Create two functions to run concurrently

def initLoadAndPred1():
    print('prcoess 1 start') 
    # init core prediction object
    corePred1 = inf.CorePredictor() 
    # corePred.loadAlignedBrainFromNpy( 'exampleData/leftAndFlippedRightBrain_sub-0151.npy' ) # load aligned brain as NPY file
    corePred1.loadAlignedBrainFromNifti( './cta-core-detection/exampleData/ctaAligned_sub-0151.nii.gz' ) # load aligned brain as Nifti file
    # Run normalization and ML model
    corePred1.normAndInfer()
    # Output examples
    corePred1.outputSummary2D('./cta-core-detection/exampleData/example2dOuput_sub-0151.png') # 2D image
    print('prcoess 1 stop')

def initLoadAndPred2():
    print('prcoess 2 start')
    corePred2 = inf.CorePredictor() 
    corePred2.loadAlignedBrainFromNifti( './cta-core-detection/exampleData/ctaAligned_sub-0150.nii.gz' ) # load aligned brain as Nifti file
    corePred2.normAndInfer()
    corePred2.outputSummary2D('./cta-core-detection/exampleData/example2dOuput_sub-0150.png') # 2D image
    print('prcoess 2 stop')

# Test with multiple threads
thr1 = threading.Thread(target=initLoadAndPred1, args=(), kwargs={})
thr2 = threading.Thread(target=initLoadAndPred2, args=(), kwargs={})

# run concurrently with threads
thr1.start()
thr2.start()

# Test with multiple processes
#proc1 = multiprocessing.Process(target=initLoadAndPred1)
#proc2 = multiprocessing.Process(target=initLoadAndPred2)

# run concurrently with processes
#proc1.start()
#proc2.start()

