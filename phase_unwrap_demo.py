import numpy as np
import matplotlib.pyplot as plt

# Example: generate a wrapped phase map
x = np.linspace(0, 4 * np.pi, 100)
y = np.linspace(0, 4 * np.pi, 100)
X, Y = np.meshgrid(x, y)
wrapped_phase = np.angle(np.exp(1j * (X + Y)))  # Wrapped between -π and π

# # Show the wrapped phase map
# plt.imshow(wrapped_phase, cmap='jet')
# plt.title('Wrapped Phase Map')
# plt.colorbar()
# plt.show()

# Unwrap along axis 0 (rows)
unwrapped_phase = np.unwrap(wrapped_phase, axis=0)

# Then unwrap along axis 1 (columns)
unwrapped_phase = np.unwrap(unwrapped_phase, axis=1)

fig, axs = plt.subplots(2, 1, figsize=(10, 10))

axs[0].imshow(wrapped_phase, cmap='jet')
axs[0].set_title('Wrapped Phase Map')

axs[1].imshow(unwrapped_phase, cmap='jet')
axs[1].set_title('Unwrapped Phase Map')

fig.colorbar(axs[0].imshow(wrapped_phase, cmap='jet'), ax=axs[0], label='Phase (radians)')
fig.colorbar(axs[1].imshow(unwrapped_phase, cmap='jet'), ax=axs[1], label='Phase (radians)')

fig.tight_layout()
plt.show()









