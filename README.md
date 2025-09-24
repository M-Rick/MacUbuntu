# MacUbuntu
## A global menu for Ubuntu and Pop!_OS (version 22 only)

The Cosmic Menu script will bring a global menu to the top of the screen in the Gnome desktop.
All previous existing settings are backed up.
The global menu uses XFCE4 Panel and brings most of the features available in XFCE4.

This script will install all the requirements for XFCE4 Panel. The top menu can be customized and other panels can be created.
A new GTK3 CSS script is created in the user profile. Nautilus is modified to bring small icons with tree-view in list view.

It only works in X11 because XFCE4 and appmenu aren't supported yet under Wayland.

Don't forget to save all your desktop configuration first with ```dconf dump / > dconf-settings.ini```.

To disable the global menu, just remove the startup desktop file ```sudo rm -f ~/.config/autostart/xfce4-panel.desktop```

Installation: ```sudo sh 'MacUbuntu.sh' ```

## macOS keybindings
This script adds macOS keybindings in Pop!_OS and Nautilus.
The keyboard is set to map French macOS keyboards. This can be changed later or just comment ```#``` the line to keep your settings. To change the language just replace *fr* with your language code.
Control and Command keys are inverted to bring the CTRL shortcuts behaviour back to the Command key. And it's more convenient to use.
Alt enables special level 3 characters (æ, Æ, œ, Œ, €, ß, ~, \\, \|, etc).
### Screenshots
- \<CMD/META> \<SHIFT> 3 : Global screenshot.
- \<CMD/META> \<SHIFT> 4 : Window screenshot.
- \<CMD/META> \<SHIFT> 5 : Area screenshot.
- \<CMD/META> \<CTRL> \<SHIFT> 3 : Global screenshot clipboard.
- \<CMD/META> \<CTRL> \<SHIFT> 4 : Window screenshot clipboard.
- \<CMD/META> \<CTRL> \<SHIFT> 5 : Area screenshot clipboard. 
 
### Exposé features
- F3 : Toggle Workspace overview
- F4 : Toggle applications Launchpad overview
- F10 : Show Activities overview
- F11 : Hide applications and show desktop
- \<SHIFT> F11 : Toggle fullscreen

Enjoy!

<img width="2048" height="1152" alt="Capture d’écran du 2025-08-20 13-50-19" src="https://github.com/user-attachments/assets/da7c9824-9830-4b90-9dc2-c8d6be8d3e21" />

### 
<img width="2048" height="1152" alt="Capture d’écran du 2025-08-20 15-20-09" src="https://github.com/user-attachments/assets/f676b427-3a79-4bde-8398-ec55201d1796" />


### The Cosmic Pop Shell extension from the Pop!_OS Cosmic Desktop
<img width="2048" height="1152" alt="Capture d’écran du 2025-06-15 20-22-13" src="https://github.com/user-attachments/assets/bb9eff9f-411f-4f6c-9384-2609719115fc" />



### Files color labels and menu enhancements with Nautilus and Nemo
<img width="2048" height="1152" alt="Capture d’écran du 2025-08-31 22-08-54" src="https://github.com/user-attachments/assets/3a02af0f-f650-4562-b8f0-0044eaa3ce2e" />

### 
<img width="2048" height="1152" alt="Capture d’écran du 2025-08-31 17-52-58" src="https://github.com/user-attachments/assets/41d14305-cdcf-47da-aebf-a9a49e701eaa" />

### 
<img width="1920" height="1080" alt="Capture d’écran du 2025-09-24 18-38-17" src="https://github.com/user-attachments/assets/d2b4b666-0737-475c-9c3c-61e4f3f16ef5" />


### 
<img width="2048" height="1152" alt="Capture d’écran du 2025-09-07 19-58-05" src="https://github.com/user-attachments/assets/a64b126e-3af9-4807-8499-725e671ba45f" />

### 
<img width="1920" height="1080" alt="Capture d’écran du 2025-09-24 18-52-36" src="https://github.com/user-attachments/assets/5da71ada-a2aa-4084-986e-0ee852959f67" />




### Pantheon Files can be used as well instead of Nautilus
<img width="2048" height="1152" alt="Capture d’écran du 2025-08-23 17-53-58" src="https://github.com/user-attachments/assets/269e0839-972f-4757-84f1-5887685e421d" />

### 
<img width="2048" height="1152" alt="Capture d’écran du 2025-08-23 17-53-30" src="https://github.com/user-attachments/assets/8a0a9d87-b679-4340-8c06-edb4bbf95059" />

