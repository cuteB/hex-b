from hexalattice.hexalattice import *
import matplotlib.pyplot as plt

def draw():
    hex_centers, _ = create_hex_grid(
        n=0,
        do_plot=True
        )

    plt.show();
