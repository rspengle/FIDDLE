from matplotlib import pylab as pl
import numpy as np
import h5py
import os, io, sys
sys.path.append('../dev/')
from viz_sequence import *
import pdb
from math import sqrt
import tensorflow as tf

def plot_prediction(pred_vec, orig_vec=None, save_dir='../results/', name='profile_prediction', strand='Single'):
    pl.ioff()
    fig, axarr = pl.subplots(pred_vec.values()[0].shape[0],len(pred_vec))
    if strand=='Double':
        to_size = pred_vec.values()[0].shape[1]/2
        for ix in range(pred_vec.values()[0].shape[0]):
            for jx, key in enumerate(pred_vec.keys()):
                if orig_vec is not None:
                    # pdb.set_trace()
                    axarr[ix, jx].plot(orig_vec[key][ix, 0, :]/np.sum(orig_vec[key][ix,:,:]+ 1e-7), label=key+'_Original', color='g')
                    axarr[ix, jx].plot(-orig_vec[key][ix, 1, :]/np.sum(orig_vec[key][ix,:,:]+ 1e-7), color='g')
                axarr[ix, jx].plot(pred_vec[key][ix, :to_size], label=key+'_Prediction', color='r')
                axarr[ix, jx].plot(-pred_vec[key][ix, to_size:], color='r')
                axarr[ix, jx].axis('off')
        axarr[0, 0].set_title(pred_vec.keys()[0])
        axarr[0, 1].set_title(pred_vec.keys()[1])


    else:
        for ix in range(pred_vec.values()[0].shape[0]):
            for jx, key in enumerate(pred_vec.keys()):
                if orig_vec is not None:
                    # pdb.set_trace()
                    axarr[ix, jx].plot(orig_vec[key][ix,0, :] / np.max(orig_vec[key][ix,0, :] + 1e-7),
                                       label=key + '_Original', color='g')
                axarr[ix, jx].plot(pred_vec[key][ix, :]/np.max(pred_vec[key][ix, :]), label=key + '_Prediction', color='r')
                axarr[ix, jx].axis('off')

        axarr[0, 1].set_title(pred_vec.keys()[0])
        axarr[0, 1].set_title(pred_vec.keys()[1])

    pl.savefig(os.path.join(save_dir,name+'.png'),format='png')
    pl.close(fig)



def put_kernels_on_grid(kernel, pad = 1):

    ''' modified from @kukuruza: https://gist.github.com/kukuruza/03731dc494603ceab0c5
    Visualize conv. features as an image (mostly for the 1st layer).
    Place kernel into a grid, with some paddings between adjacent filters.
    Args:
      kernel:            tensor of shape [Y, X, NumChannels, NumKernels]
      (grid_Y, grid_X):  shape of the grid. Require: NumKernels == grid_Y * grid_X
                           User is responsible of how to break into two multiples.
      pad:               number of black pixels around each filter (between them)
    Return:
      Tensor of shape [(Y+2*pad)*grid_Y, (X+2*pad)*grid_X, NumChannels, 1].
    '''
    # get shape of the grid. NumKernels == grid_Y * grid_X
    def factorization(n):
        for i in range(int(sqrt(float(n))), 0, -1):
            if n % i == 0:
                if i == 1: print('Who would enter a prime number of filters')
                return (i, int(n / i))
    (grid_Y, grid_X) = factorization (kernel.get_shape()[3].value)
    print ('grid: %d = (%d, %d)' % (kernel.get_shape()[3].value, grid_Y, grid_X))

    x_min = tf.reduce_min(kernel)
    x_max = tf.reduce_max(kernel)

    kernel1 = (kernel - x_min) / (x_max - x_min)

    # pad X and Y
    x1 = tf.pad(kernel1, tf.constant( [[pad,pad],[pad, pad],[0,0],[0,0]] ), mode = 'CONSTANT')

    # X and Y dimensions, w.r.t. padding
    Y = kernel1.get_shape()[0] + 2 * pad
    X = kernel1.get_shape()[1] + 2 * pad

    channels = kernel1.get_shape()[2]

    # put NumKernels to the 1st dimension
    x2 = tf.transpose(x1, (3, 0, 1, 2))
    # organize grid on Y axis
    x3 = tf.reshape(x2, tf.stack([grid_X, Y * grid_Y, X, channels]))

    # switch X and Y axes
    x4 = tf.transpose(x3, (0, 2, 1, 3))
    # organize grid on X axis
    x5 = tf.reshape(x4, tf.stack([1, X * grid_X, Y * grid_Y, channels]))

    # back to normal order (not combining with the next step for clarity)
    x6 = tf.transpose(x5, (2, 1, 3, 0))

    # to tf.image_summary order [batch_size, height, width, channels],
    #   where in this case batch_size == 1
    x7 = tf.transpose(x6, (3, 0, 1, 2))

    # scaling to [0, 255] is not necessary for tensorboard
    return x7


def visualize_filters():

    raise NotImplementedError

def plot_weights(array,
                 height_padding_factor=0.2,
                 length_padding=1.0,
                 subticks_frequency=1.0,
                 colors=default_colors,
                 plot_funcs=default_plot_funcs,
                 highlight={},
                 ax=[]):
    # fig = plt.figure(figsize=(20,2))
    # ax = fig.add_subplot(111)
    plot_weights_given_ax(ax=ax, array=array,
        height_padding_factor=height_padding_factor,
        length_padding=length_padding,
        subticks_frequency=subticks_frequency,
        colors=colors,
        plot_funcs=plot_funcs,
        highlight=highlight)

def visualize_dna(weigths, pred_vec, save_dir='../results/', name='dna_prediction'):
    pl.ioff()
    fig = pl.figure(figsize=(20,20))
    for ix in range(pred_vec.shape[0]):
        ax = fig.add_subplot(pred_vec.shape[0], 1, ix+1)
        H = abs((.25 * np.log2(.25 + 1e-7) - pred_vec[ix, :, :, 0] * np.log2(pred_vec[ix, :,:,0] + 1e-7)).sum(axis=0))
        H = np.tile(H, 4).reshape(4, pred_vec.shape[2], 1)
        plot_weights(weigths[ix] * H,
                     height_padding_factor=0.2,
                     length_padding=1.0,
                     colors=default_colors,
                     subticks_frequency=pred_vec.shape[2]/2,
                     plot_funcs=default_plot_funcs,
                     highlight={},
                     ax=ax)
    pl.savefig(os.path.join(save_dir, name + '.png'), format='png')
    pl.close(fig)


def main():
    raise NotImplementedError


if __name__=='__main__':
    main()