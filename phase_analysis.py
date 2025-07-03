import numpy as np
from modules.image_process import png_to_array
from pathlib import Path
import matplotlib.pyplot as plt
# import plotly.express as px

def isoclinic_phase(I1, I2, I3, I4, method='arctan2'):
    """
    Calculate the phase of the isoclinic state.
    """
    if method == 'arctan2':
        return 0.25*np.arctan2(I3-I2, I4-I1)
    elif method == 'arctan':
        return 0.25*np.arctan((I3-I2)/(I4-I1))
    else:
        raise ValueError(f"Invalid method: {method}")

def isochromatic_phase(iso_phase, I5, I6, I7, I8, I9, I10, method='arctan2'):
    """
    Calculate the phase of the isochromatic state.
    """
    numerator = (I9-I7)*np.sin(2*iso_phase) + (I8-I10)*np.cos(2*iso_phase)
    denominator = (I5-I6)
    if method == 'arctan2':
        return np.arctan2(numerator, denominator)
    elif method == 'arctan':
        return np.arctan(numerator/denominator)
    else:
        raise ValueError(f"Invalid method: {method}")


folder = Path('R:/Pockels_data/STRESS IMAGING/Polariscope-Test')
I1 = png_to_array(folder / 'I1.png')
I2 = png_to_array(folder / 'I2.png')
I3 = png_to_array(folder / 'I3.png')
I4 = png_to_array(folder / 'I4.png')
I5 = png_to_array(folder / 'I5.png')
I6 = png_to_array(folder / 'I6.png')
I7 = png_to_array(folder / 'I7.png')
I8 = png_to_array(folder / 'I8.png')
I9 = png_to_array(folder / 'I9.png')
I10 = png_to_array(folder / 'I10.png')


# phase1 = isoclinic_phase(I1, I2, I3, I4, method='arctan')
# phase1_unwrap = np.unwrap(phase1, axis=0)
# phase1_unwrap = np.unwrap(phase1_unwrap, axis=1)

phase2 = isoclinic_phase(I1, I2, I3, I4, method='arctan2')
phase2_unwrap = np.unwrap(phase2, axis=0, period=np.pi)
phase2_unwrap = np.unwrap(phase2_unwrap, axis=1, period=np.pi)

delta = isochromatic_phase(phase2, I5, I6, I7, I8, I9, I10, method='arctan2')
delta_unwrap = np.unwrap(delta, axis=0)
delta_unwrap = np.unwrap(delta_unwrap, axis=1)

fig, axs = plt.subplots(2, 2, figsize=(10, 10))

axs[0,0].imshow(phase2, cmap='jet')
axs[0,0].set_title('arctan method')

axs[0, 1].imshow(phase2_unwrap, cmap='jet')
axs[0, 1].set_title('arctan method unwrapped')

axs[1,0].imshow(delta, cmap='jet')
axs[1,0].set_title('arctan2 method')

axs[1, 1].imshow(delta_unwrap, cmap='jet')
axs[1, 1].set_title('arctan2 method unwrapped')

fig.colorbar(axs[0,0].imshow(phase2, cmap='jet'), ax=axs[0,0], label='Phase (radians)')
fig.colorbar(axs[1,0].imshow(delta, cmap='jet'), ax=axs[1,0], label='Phase (radians)')
fig.colorbar(axs[0,1].imshow(phase2_unwrap, cmap='jet'), ax=axs[0,1], label='Phase (radians)')
fig.colorbar(axs[1,1].imshow(delta_unwrap, cmap='jet'), ax=axs[1,1], label='Phase (radians)')

fig.tight_layout()
plt.show()


