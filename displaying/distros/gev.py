import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
from scipy.stats import genextreme as gev

x = np.linspace(20, 100, 1000)
mu = 36
eta = 0.1
sigma = 1.3

# Add every font at the specified location
font_dir = ['/home/tcarrasco/result/fonts/Merriweather',
            '/home/tcarrasco/result/fonts/arial']
for font in font_manager.findSystemFonts(font_dir):
    font_manager.fontManager.addfont(font)

plt.rcParams['font.family'] = 'arial'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = False

fig, axs = plt.subplots(2, 2, figsize=(10, 10), sharex=False, sharey=False)

ax = axs[0, 0]
plt.sca(ax)
y = gev.pdf(x, eta, mu, sigma)
plt.plot(x, y, c='k', lw=1.0)
plt.legend(['Control\n(mu, sig, eta)\n(36, 1.3, 0.1)'])
plt.ylim([0, 0.30])
plt.xlim([30, 50])
plt.ylabel('PDF')

ax = axs[0, 1]
plt.sca(ax)
y = gev.pdf(x, eta, mu, sigma)
plt.plot(x, y, c='k', lw=1.0)
y = gev.pdf(x, eta, mu+10, sigma)
plt.plot(x, y, c='red', lw=1.0)
y = gev.pdf(x, eta, mu-10, sigma)
plt.plot(x, y, c='blue', lw=1.0)
plt.legend(['Control', 'mu+10ºC', 'mu-10ºC'])
plt.ylim([0, 0.30])
plt.xlim([20, 60])


ax = axs[1, 0]
plt.sca(ax)
y = gev.pdf(x, eta, mu, sigma)
plt.plot(x, y, c='k', lw=1.0)
y = gev.pdf(x, eta, mu, sigma*2)
plt.plot(x, y, c='red', lw=1.0)
y = gev.pdf(x, eta, mu, sigma/2)
plt.plot(x, y, c='blue', lw=1.0)
plt.legend(['Control', 'sig x 2', 'sig / 2'])
plt.ylim([0, 0.65])
plt.xlim([20, 50])
plt.ylabel('PDF')
plt.xlabel('Tmax (ºC)')

ax = axs[1, 1]
plt.sca(ax)
y = gev.pdf(x, eta, mu, sigma)
plt.plot(x, y, c='k', lw=1.0)
y = gev.pdf(x, eta*2, mu, sigma)
plt.plot(x, y, c='red', lw=1.0)
y = gev.pdf(x, eta/2, mu, sigma)
plt.plot(x, y, c='blue', lw=1.0)
plt.legend(['Control', 'eta x 2', 'eta / 2'])
plt.ylim([0, 0.30])
plt.xlim([30, 50])
plt.xlabel('Tmax (ºC)')

plt.tight_layout()
plt.savefig('/home/tcarrasco/result/images/png/ditro_gev.png', dpi=300)
