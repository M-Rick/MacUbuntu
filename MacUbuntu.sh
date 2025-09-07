#! /bin/sh

## MacUbuntu - Ubuntu with a macOS global menu
## Works only in X11 until XFCE4 and appmenu are ported under Wayland
## Ubuntu 22.04 and higher Vanilla version
## https://github.com/M-Rick/MacUbuntu

#set -e  # Stop in case of errors

# Create necessary directories
mkdir -p ~/.config/xfce4/xfconf/xfce-perchannel-xml
mkdir -p ~/.config/gtk-3.0
mkdir -p ~/.config/autostart
mkdir -p ~/.config/dconf/MacUbuntu
mkdir -p ~/.local/share/applications
mkdir -p ~/.local/share/gnome-shell/extensions
mkdir -p ~/.local/share/nautilus-python/extensions/
mkdir -p ~/.local/share/nemo-python/extensions/
mkdir -p ~/.local/share/icons/Yaru/actions/symbolic

## Backup settings
dconf dump / > ~/.config/dconf/MacUbuntu/dconf.bak

# Install XFCE4 Panel
sudo apt install -y --ignore-missing xfce4-panel xfce4-sntray-plugin xfce4-whiskermenu-plugin xfce4-appmenu-plugin appmenu-gtk2-module appmenu-gtk3-module appmenu-gtk-module-common appmenu-registrar appmenu-qt5 libdbusmenu-glib4 libdbusmenu-gtk3-4 libdbusmenu-gtk4 python3-nautilus neofetch


# Create autostart file
cat > ~/.config/autostart/xfce4-panel.desktop << 'EOF'
[Desktop Entry]
Type=Application
Exec=/usr/bin/xfce4-panel
Hidden=false
NoDisplay=true
X-GNOME-Autostart-enabled=true
Name=XFCE4 Panel
Comment=MacUbuntu Panel
EOF

# Download Ubuntu logo
wget -q https://upload.wikimedia.org/wikipedia/commons/7/7b/Ubuntu-logo-no-wordmark-solid-o-2022.svg -O ~/.config/dconf/MacUbuntu/Ubuntu-logo.svg

# Create XFCE4 panel configuration
cat > ~/.config/xfce4/xfconf/xfce-perchannel-xml/xfce4-panel.xml << EOF
<?xml version="1.0" encoding="UTF-8"?>

<channel name="xfce4-panel" version="1.0">
  <property name="configver" type="int" value="2"/>
  <property name="panels" type="array">
    <value type="int" value="1"/>
    <property name="panel-1" type="empty">
      <property name="position" type="string" value="p=6;x=840;y=15"/>
      <property name="length" type="double" value="70.069444444444444"/>
      <property name="position-locked" type="bool" value="true"/>
      <property name="icon-size" type="uint" value="24"/>
      <property name="size" type="uint" value="32"/>
      <property name="plugin-ids" type="array">
        <value type="int" value="1"/>
        <value type="int" value="2"/>
        <value type="int" value="3"/>
        <value type="int" value="4"/>
      </property>
      <property name="mode" type="uint" value="0"/>
      <property name="background-style" type="uint" value="1"/>
      <property name="background-rgba" type="array">
        <value type="double" value="0.157"/>
        <value type="double" value="0.157"/>
        <value type="double" value="0.157"/>
        <value type="double" value="0.89000000000000000"/>
      </property>
      <property name="enable-struts" type="bool" value="false"/>
      <property name="dark-mode" type="bool" value="true"/>
    </property>
  </property>
  <property name="plugins" type="empty">
    <property name="plugin-1" type="string" value="separator">
      <property name="expand" type="bool" value="false"/>
      <property name="style" type="uint" value="0"/>
    </property>
    <property name="plugin-2" type="string" value="applicationsmenu">
      <property name="show-button-title" type="bool" value="false"/>
      <property name="custom-menu" type="bool" value="true"/>
      <property name="button-icon" type="string" value="$HOME/.config/dconf/MacUbuntu/Ubuntu-logo.svg"/>
      <property name="show-tooltips" type="bool" value="false"/>
      <property name="small" type="bool" value="false"/>
      <property name="custom-menu-file" type="string" value="$HOME/.config/dconf/MacUbuntu/session.menu"/>
      <property name="show-menu-icons" type="bool" value="true"/>
      <property name="show-generic-names" type="bool" value="false"/>
      <property name="button-title" type="string" value="Ubuntu"/>
    </property>
    <property name="plugin-3" type="string" value="separator">
      <property name="style" type="uint" value="0"/>
    </property>
    <property name="plugin-4" type="string" value="appmenu">
      <property name="compact-mode" type="bool" value="false"/>
      <property name="bold-application-name" type="bool" value="true"/>
      <property name="expand" type="bool" value="false"/>
    </property>
  </property>
</channel>
EOF

# XFCE4 panel custom menu
cat > ~/.config/dconf/MacUbuntu/session.menu << 'EOF'
<!DOCTYPE Menu PUBLIC "-//freedesktop//DTD Menu 1.0//EN"
  "http://www.freedesktop.org/standards/menu-spec/1.0/menu.dtd">
<Menu>
    <Name>Applications</Name>
    <DefaultAppDirs/>
    <DefaultDirectoryDirs/>

    <Include>
        <Category>MacUbuntu</Category>
    </Include>

    <Layout>
        <Filename>about.desktop</Filename>
        <Filename>settings.desktop</Filename>
        <Filename>update.desktop</Filename>
        <Separator/>
        <Filename>appcenter.desktop</Filename>
        <Filename>softwares.desktop</Filename>
        <Filename>terminal.desktop</Filename>
        <Separator/>
        <Menu>Power Tools</Menu>
        <Separator/>
        <Filename>monitor.desktop</Filename>
        <Separator/>
        <Filename>suspend.desktop</Filename>
        <Filename>reboot.desktop</Filename>
        <Filename>shutdown.desktop</Filename>
        <Separator/>
        <Filename>lock.desktop</Filename>
        <Filename>logout.desktop</Filename>
    </Layout>
</Menu>

<Exclude>
    <Category>MacUbuntu</Category>
</Exclude>

EOF


echo "Creating MacUbuntu menu items..."

# About
cat > ~/.local/share/applications/about.desktop << 'EOF'
[Desktop Entry]
Type=Application
Name[en]=About this computer
Name[fr]=À propos de cet ordinateur
Exec=gnome-control-center about
Icon=start-here
NoDisplay=false
Categories=MacUbuntu;
EOF

# Settings
cat > ~/.local/share/applications/settings.desktop << 'EOF'
[Desktop Entry]
Type=Application
Name[en]=System settings…
Name[fr]=Réglages système…
Exec=gnome-control-center
Icon=org.gnome.Settings
NoDisplay=false
Categories=MacUbuntu;
EOF

# Update
cat > ~/.local/share/applications/update.desktop << 'EOF'
[Desktop Entry]
Type=Application
Name[en]=Software Updater
Name[fr]=Mises à jour…
Exec=update-manager
Icon=system-software-update
NoDisplay=false
Categories=MacUbuntu;
EOF

# App Center
cat > ~/.local/share/applications/appcenter.desktop << 'EOF'
[Desktop Entry]
Type=Application
Name[en]=Ubuntu App Center
Name[fr]=Centre d’Applications Ubuntu
Exec=snap-store
Icon=snap-store
NoDisplay=false
Categories=MacUbuntu;
EOF

# Softwares
cat > ~/.local/share/applications/softwares.desktop << 'EOF'
[Desktop Entry]
Type=Application
Name[en]=Softwares
Name[fr]=Logiciels
Exec=gnome-software
Icon=org.gnome.Software
NoDisplay=false
Categories=MacUbuntu;
EOF

# Terminal
cat > ~/.local/share/applications/terminal.desktop << 'EOF'
[Desktop Entry]
Type=Application
Name=Terminal
Exec=gnome-terminal
Icon=utilities-terminal
NoDisplay=false
Categories=MacUbuntu;
EOF

# System Monitor
cat > ~/.local/share/applications/monitor.desktop << 'EOF'
[Desktop Entry]
Type=Application
Name[en]=Activity Monitor
Name[fr]=Moniteur d'activité
Exec=gnome-system-monitor
Icon=utilities-system-monitor
NoDisplay=false
Categories=MacUbuntu;
EOF

# System Suspend
cat > ~/.local/share/applications/suspend.desktop << 'EOF'
[Desktop Entry]
Type=Application
Name[en]=System Suspend
Name[fr]=Suspendre l'activité
Exec=systemctl suspend
Icon=system-log-out
NoDisplay=false
Categories=MacUbuntu;
EOF

# System Reboot
cat > ~/.local/share/applications/reboot.desktop << 'EOF'
[Desktop Entry]
Type=Application
Name=Reboot
Name[fr]=Redémarrer…
Exec=systemctl reboot
Icon=system-reboot
NoDisplay=false
Categories=MacUbuntu;
EOF

# System Shutdown
cat > ~/.local/share/applications/shutdown.desktop << 'EOF'
[Desktop Entry]
Type=Application
Name=Shutdown
Name[fr]=Éteindre…
Exec=systemctl poweroff
Icon=system-shutdown
NoDisplay=false
Categories=MacUbuntu;
EOF

# System Lock
cat > ~/.local/share/applications/lock.desktop << 'EOF'
[Desktop Entry]
Type=Application
Name=Lock screen
Name[fr]=Verrouiller l'écran
Exec=loginctl lock-session
Icon=system-lock-screen
NoDisplay=false
Categories=MacUbuntu;
EOF

# System Logout
cat > ~/.local/share/applications/logout.desktop << 'EOF'
[Desktop Entry]
Type=Application
Name=Logout
Name[fr]=Fermer la session
Exec=gnome-session-quit --logout --no-prompt
Icon=system-log-out
NoDisplay=false
Categories=MacUbuntu;
EOF


# Pantheon Files

# Download Pantheon Files icons
wget -q https://github.com/M-Rick/MacUbuntu/raw/main/Icons/view-column-symbolic.svg
mv ~/view-column-symbolic.svg ~/.local/share/icons/Yaru/actions/symbolic

# Install Pantheon Files
echo "Detecting system architecture..."
ARCH=$(uname -m)
case $ARCH in
    x86_64)
        DEBIAN_ARCH="amd64"
        ;;
    aarch64|arm64)
        DEBIAN_ARCH="arm64"
        ;;
    *)
        echo "Unsupported architecture: $ARCH"
        exit 1
        ;;
esac

echo "Architecture detected: $DEBIAN_ARCH"

# Download Pantheon Files for detected architecture
echo "Downloading Pantheon Files for $DEBIAN_ARCH..."
wget https://launchpad.net/~elementary-os/+archive/ubuntu/stable/+files/pantheon-files_7.1.4+r6464+pkg134~ubuntu8.1_${DEBIAN_ARCH}.deb -P ~/.config/dconf/MacUbuntu --no-check-certificate || {
    echo "Warning: Could not download pantheon-files"
}
wget https://launchpad.net/~elementary-os/+archive/ubuntu/stable/+files/libpantheon-files-core0_7.1.4+r6464+pkg134~ubuntu8.1_${DEBIAN_ARCH}.deb -P ~/.config/dconf/MacUbuntu --no-check-certificate || {
    echo "Warning: Could not download libpantheon-files-core0"
}

# Install the downloaded packages
echo "Installing Pantheon Files..."
cd ~/.config/dconf/MacUbuntu && sudo apt install -y ./*${DEBIAN_ARCH}.deb || {
    echo "Warning: Could not install Pantheon Files packages"
}

wget -q https://github.com/M-Rick/MacUbuntu/raw/main/XFCE4/io.elementary.files.desktop
mv ~/io.elementary.files.desktop ~/.local/share/applications/


# Create GTK3 CSS

if [ -f ~/.config/gtk-3.0/gtk.css ]; then
    mv ~/.config/gtk-3.0/gtk.css ~/.config/gtk-3.0/gtk.css.bak
fi

cat > ~/.config/gtk-3.0/gtk.css << 'EOF'
/* Accent Colors */

@define-color STRAWBERRY_100 #ff8c82;
@define-color STRAWBERRY_300 #ed5353;
@define-color STRAWBERRY_500 #c6262e;
@define-color STRAWBERRY_700 #a10705;
@define-color STRAWBERRY_900 #7a0000;

@define-color ORANGE_100 #ffc27d;
@define-color ORANGE_300 #ffa154;
@define-color ORANGE_500 #f37329;
@define-color ORANGE_700 #cc3b02;
@define-color ORANGE_900 #a62100;

@define-color BANANA_100 #fff394;
@define-color BANANA_300 #ffe16b;
@define-color BANANA_500 #f9c440;
@define-color BANANA_700 #d48e15;
@define-color BANANA_900 #ad5f00;

@define-color LIME_100 #d1ff82;
@define-color LIME_300 #9bdb4d;
@define-color LIME_500 #68b723;
@define-color LIME_700 #3a9104;
@define-color LIME_900 #206b00;

@define-color MINT_100 #89ffdd;
@define-color MINT_300 #43d6b5;
@define-color MINT_500 #28bca3;
@define-color MINT_700 #0e9a83;
@define-color MINT_900 #007367;

@define-color BLUEBERRY_100 #8cd5ff;
@define-color BLUEBERRY_300 #64baff;
@define-color BLUEBERRY_500 #3689e6;
@define-color BLUEBERRY_700 #0d52bf;
@define-color BLUEBERRY_900 #002e99;

@define-color BUBBLEGUM_100 #fe9ab8;
@define-color BUBBLEGUM_300 #f4679d;
@define-color BUBBLEGUM_500 #de3e80;
@define-color BUBBLEGUM_700 #bc245d;
@define-color BUBBLEGUM_900 #910e38;

@define-color GRAPE_100 #e4c6fa;
@define-color GRAPE_300 #cd9ef7;
@define-color GRAPE_500 #a56de2;
@define-color GRAPE_700 #7239b3;
@define-color GRAPE_900 #452981;

@define-color COCOA_100 #a3907c;
@define-color COCOA_300 #8a715e;
@define-color COCOA_500 #715344;
@define-color COCOA_700 #57392d;
@define-color COCOA_900 #3d211b;

@define-color SILVER_100 #fafafa;
@define-color SILVER_300 #d4d4d4;
@define-color SILVER_500 #abacae;
@define-color SILVER_700 #7e8087;
@define-color SILVER_900 #555761;

@define-color SLATE_100 #95a3ab;
@define-color SLATE_300 #667885;
@define-color SLATE_500 #485a6c;
@define-color SLATE_700 #273445;
@define-color SLATE_900 #0e141f;

@define-color BLACK_100 #666;
@define-color BLACK_300 #4d4d4d;
@define-color BLACK_500 #333;
@define-color BLACK_700 #1a1a1a;
@define-color BLACK_900 #000;

/* Accent Shades */

@define-color accent_color_100 @BLUEBERRY_100;
@define-color accent_color_300 @BLUEBERRY_300;
@define-color accent_color_500 @BLUEBERRY_500;
@define-color accent_color_700 @BLUEBERRY_700;
@define-color accent_color_900 @BLUEBERRY_900;
@define-color accent_color mix(@BLUEBERRY_300, @BLUEBERRY_500, 0.25);

/* Variables */

@define-color highlight_color white;
@define-color fg_color #333;



/* XFCE4 */

/* XFCE 4 Panel */

.xfce4-panel {
    font-family: 'Ubuntu Sans';
    font-style: normal;
    font-weight: 500;
    font-size: 14px;
    color: white;
}

.xfce4-panel .background {
    border-radius: 14px;
    transition: background-color 0.2s ease, color 0.2s ease;
}

.xfce4-panel menu {
    opacity: 0.94;
    padding: 0px;
    border-style: none;
    transition: background-color 0.2s ease, color 0.2s ease;
}

.xfce4-panel.panel button:checked {
    border-radius: 14px;
}

.xfce4-panel .-vala-panel-appmenu-private > menuitem,
.xfce4-panel .-vala-panel-appmenu-private > menuitem > label {
    box-shadow: none;
    color: white;
}

menubar.-vala-panel-appmenu-bold > menuitem:first-child > label {
    font-family: 'Ubuntu Sans';
    font-style: bold;
    font-weight: bolder;
    font-size: 14px;
}

.-vala-panel-appmenu-private > menuitem > label {
    padding: 0 0px;
}

.-vala-panel-appmenu-private > menuitem:hover {
    background: @theme_selected_bg_color;
}



/* Application Menu */

#applicationmenu-button {
border-radius: 14px;
padding: 0 4px 0 4px;
margin-left: 2px;
}

#applicationmenu-button:hover {
background: rgba(0, 0, 0, 0.8) !important;
border-radius: 14px;
padding: 0 4px 0 4px;
margin-left: 2px;
}

#applicationmenu-button:checked {
background: grey;
border-radius: 14px;
padding: 0 4px 0 4px;
margin-left: 2px;
}


#applicationmenu-button box {
}



/* Menus */

menu {
    font-family: 'Ubuntu Sans';
    font-style: normal;
    font-weight: 500;
    font-size: 14px;
    border: 0.5px solid rgba(128, 128, 128, 0.30);
    border-radius: 5px;
    padding: 5px;
    opacity: 0.96;
    outline: none;
    backdrop-filter: blur(22px);
    box-shadow: 0 1px 0 0 alpha(@highlight_color, 0.3), inset 0 10px 10px rgba(0, 0, 0, 0.05), inset 0 0 10px 10px rgba(0, 0, 0, 0.05);
}

menu menuitem {
    padding: 5px 10px 5px 10px;
    margin: 2px 5px 2px 5px;
}

menu menuitem:hover {
    border-radius: 8px;
}

menu menuitem:hover .color-button {

}

menu menuitem:hover:not(.color-button),
menu menuitem:not(.color-button):hover {
    background: @theme_selected_bg_color;
}

menu menuitem:first-child {

}

menu separator {
    background-color: rgba(128, 128, 128, 0.3);
    min-height: 1px;
    margin: 5px 10px;
}

/* Termminal */
.menu, .context-menu, .popover {
    opacity: 0.96;
    border-radius: 5px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(22px);
    transition: background-color 0.2s ease, color 0.2s ease;
}

.popup menuitem {
    font-family: 'Ubuntu Sans';
    font-style: normal;
    font-weight: 500;
    font-size: 14px;
    padding: 5px 10px 5px 10px;
    margin: 2px 5px 2px 5px;
}

/* Popup buttons */
.popup {

}

popover {
    opacity: 0.96;
    border-radius: 14px;
    backdrop-filter: blur(22px);
    box-shadow: 0 1px 0 0 alpha(@highlight_color, 0.3), inset 0 10px 10px rgba(0, 0, 0, 0.03), inset 0 0 10px 10px rgba(0, 0, 0, 0.03);
}

popover menuitem {
    font-family: 'Ubuntu Sans';
    font-style: normal;
    font-weight: 500;
    font-size: 14px;
    padding: 3px 10px 3px 10px;
    margin: 0px 5px 0px 5px;
}

popover .pop {
    font-family: 'Ubuntu Sans';
    font-style: normal;
    font-weight: 500;
    font-size: 14px;
    padding: 5px 10px 5px 10px;
    margin: 0px 5px 0px 5px;
}

menubar > menuitem label {

}

menu menuitem .keycap {
    opacity: 0.0;
    font-size: 0;
    background: none;
    margin: -5;
    padding: 0;
    border: none;
    box-shadow: none;
    min-width: 0;
}



/* Pantheon */

.io-elementary-files image[icon-name="view-column-symbolic"],
window.pantheon-files image[icon-name="view-column-symbolic"] {
    -gtk-icon-source: -gtk-icontheme("view-list-symbolic");
}

.sidebar,
.sidebar list,
.sidebar .view,
.sidebar.view {
    font-family: 'Ubuntu Sans';
    font-style: normal;
    font-weight: 500;
    padding: 4px 0px 4px 0px;
    margin: 3px 3px 3px 2px;
}

.sidebar list row,
.sidebar > label {
    font-size: 1.03em;
    padding: 8px 14px 7px 14px;
    margin: 2px 5px 2px 5px;
    border-radius: 6px;
    min-height: 22px;
}

.sidebar image {
    -gtk-icon-theme: "Yaru";
    -gtk-icon-style: symbolic;
}


/* Color tags Pantheon Files */

.color-button check,
.color-button check:checked,
.color-button radio,
.color-button radio:checked {
    background-image: none;
    border: 1px solid rgba(128, 128, 128, 0.5);
    border-radius: 50%;
    box-shadow: 0 1px 0 0 alpha(@highlight_color, 0.3), inset 0 1px 1px rgba(0, 0, 0, 0.05), inset 0 0 1px 1px rgba(0, 0, 0, 0.05);
    min-height: 1.000000001rem;
    min-width: 1.000000001rem;
    padding: 0.250000001rem;
    opacity: 1.0;
    color: white;
}

.color-button check:checked,
.color-button radio:checked {
    min-height: calc(1rem - 1px);
    min-width: calc(1rem - 1px);
}

.color-button.red check, .color-button.red radio,
.color-button.strawberry check, .color-button.strawberry radio {
    background-color: @STRAWBERRY_300;
    -gtk-icon-shadow: 0 1px 1px @STRAWBERRY_500;
}
.color-button.red check:checked, .color-button.red radio:checked,
.color-button.strawberry check:checked, .color-button.strawberry radio:checked {
    border: 3px solid @STRAWBERRY_300;
}

.color-button.orange check, .color-button.orange radio {
    background-color: @ORANGE_300;
    -gtk-icon-shadow: 0 1px 1px @ORANGE_500;
}
.color-button.orange check:checked, .color-button.orange radio:checked {
    border: 3px solid @ORANGE_300;
}

.color-button.yellow check, .color-button.yellow radio,
.color-button.banana check, .color-button.banana radio {
    background-color: @BANANA_500;
    -gtk-icon-shadow: 0 1px 1px @BANANA_700;
}
.color-button.yellow check:checked, .color-button.yellow radio:checked,
.color-button.banana check:checked, .color-button.banana radio:checked {
    border: 3px solid @BANANA_500;
}

.color-button.green check, .color-button.green radio,
.color-button.lime check, .color-button.lime radio {
    background-color: @LIME_500;
}
.color-button.green check:checked, .color-button.green radio:checked,
.color-button.lime check:checked, .color-button.lime radio:checked {

    border: 3px solid @LIME_500;
}

.color-button.blue check, .color-button.blue radio,
.color-button.blueberry check, .color-button.blueberry radio {
    background-color: @BLUEBERRY_500;
    -gtk-icon-shadow: 0 1px 1px @BLUEBERRY_700;
}
.color-button.blue check:checked, .color-button.blue radio:checked,
.color-button.blueberry check:checked, .color-button.blueberry radio:checked {
    border: 3px solid @BLUEBERRY_500;
}

.color-button.purple check, .color-button.purple radio,
.color-button.grape check, .color-button.grape radio {
    background-color: @GRAPE_500;
    -gtk-icon-shadow: 0 1px 1px @GRAPE_700;
}
.color-button.purple check:checked, .color-button.purple radio:checked,
.color-button.grape check:checked, .color-button.grape radio:checked {
    border: 3px solid @GRAPE_500;
}

.color-button.brown check, .color-button.brown radio,
.color-button.cocoa check, .color-button.cocoa radio {
    background-color: @COCOA_300;
    -gtk-icon-shadow: 0 1px 1px @COCOA_500;
}
.color-button.brown check:checked, .color-button.brown radio:checked,
.color-button.cocoa check:checked, .color-button.cocoa radio:checked {
    border: 3px solid @COCOA_300;
}

.color-button.mint check, .color-button.mint radio {
    background-color: @MINT_500;
    -gtk-icon-shadow: 0 1px 1px @MINT_700;
}

.color-button.mint check:checked, .color-button.mint radio:checked {
    border: 3px solid @MINT_500;
}

.color-button.pink check, .color-button.pink radio,
.color-button.bubblegum check, .color-button.bubblegum radio {
    background-color: @BUBBLEGUM_500;
    -gtk-icon-shadow: 0 1px 1px @BUBBLEGUM_700;
}
.color-button.pink check:checked, .color-button.pink radio:checked,
.color-button.bubblegum check:checked, .color-button.bubblegum radio:checked {
    border: 3px solid @BUBBLEGUM_500;
}

.color-button.slate check, .color-button.slate radio {
    background-color: @SLATE_300;
    -gtk-icon-shadow: 0 1px 1px @SLATE_500;
}
.color-button.slate check:checked, .color-button.slate radio:checked {
    border: 3px solid @SLATE_300;
}

.color-button.auto radio {
    background-position: -1px -1px;
    background-repeat: no-repeat;
    background-size: calc(100% + 2px);
    opacity: 1.0;
}




/* Progressbar */

progressbar {
    height: 10px;
}

progressbar.vertical progress,
progressbar.vertical trough, levelbar.vertical block {
    background-image: linear-gradient(to right, alpha(@highlight_color, 0.2), rgba(255, 255, 255, 0));
}

progressbar.vertical progress:backdrop,
progressbar.vertical trough:backdrop, levelbar.vertical block:backdrop {
    background-image: linear-gradient(to right, alpha(@highlight_color, 0.35), alpha(@highlight_color, 0.3));
}

progressbar {
    border-radius: 0.1666666677rem;
}

progressbar progress,
progressbar trough {
    border: 1px solid rgba(0, 0, 0, 0.2);
    border-radius: 0.1666666677rem;
}

progressbar progress {
    background-color: @accent_color;
    box-shadow: inset 0 -1px 0 0 alpha(@highlight_color, 0.2), inset 0 1px 0 0 alpha(@highlight_color, 0.3), inset 1px 0 0 0 alpha(@highlight_color, 0.07), inset -1px 0 0 0 alpha(@highlight_color, 0.07);
}

progressbar progress:backdrop {
    background-color: #dfdfdf;
}

progressbar trough {
    background-color: #fafafa;
    box-shadow: inset 0 -1px 0 0 alpha(@highlight_color, 0.2), inset 0 1px 0 0 alpha(@highlight_color, 0.3), inset 1px 0 0 0 alpha(@highlight_color, 0.07), inset -1px 0 0 0 alpha(@highlight_color, 0.07), 0 1px 1px rgba(0, 0, 0, 0.05);
}

progressbar.horizontal progress {
    margin-left: -1px;
    margin-right: -1px;
}

progressbar.horizontal progress:not(.pulse) {
    animation: progress 1.5s cubic-bezier(0.4, 0, 0.2, 1) infinite;
    background-size: cover, 48px 100%;
    background-repeat: no-repeat;
    background-image: linear-gradient(to bottom, alpha(@highlight_color, 0.2), rgba(255, 255, 255, 0)), linear-gradient(to right, rgba(255, 255, 255, 0), rgba(255, 255, 255, 0.25) 60%, rgba(255, 255, 255, 0));
}

progressbar.horizontal progress:not(.pulse).right {
    animation-direction: reverse;
}

progressbar.horizontal progress:backdrop {
    animation: none;
    background-image: none;
}

progressbar.vertical progress {
    margin: -1px 0;
}

progressbar.flat progress, tab progressbar.tab-close-button progress,
tab progressbar.tab-indicator progress,
progressbar.flat trough,
tab progressbar.tab-close-button trough,
tab progressbar.tab-indicator trough {
    box-shadow: none;
    border: none;
    border-radius: 0.500000001rem;
    margin: 0;
    height: 10px;
}

progressbar.flat progress, tab progressbar.tab-close-button progress,
tab progressbar.tab-indicator progress,
progressbar.flat progress:backdrop,
progressbar.flat .horizontal progress {
    animation: none;
    background: alpha(@fg_color, 0.78);
}

progressbar.flat trough, tab progressbar.tab-close-button trough,
tab progressbar.tab-indicator trough {
    background: alpha(@fg_color, 0.15);
}


button.back-button:dir(ltr) {
    background-image: -gtk-icontheme("go-previous-symbolic"),
    linear-gradient(to bottom, alpha(@highlight_color, 0.2), rgba(255, 255, 255, 0));
    padding-left: calc(0.750000001rem + 16px);
    background-position: 0.500000001rem 50%, center, center;
}

button.back-button:dir(rtl) {
    background-image: -gtk-icontheme("go-next-symbolic"),
    linear-gradient(to bottom, alpha(@highlight_color, 0.2), rgba(255, 255, 255, 0));
    padding-right: calc(0.750000001rem + 16px);
    background-position: calc(100% - 0.500000001rem) 50%, center, center;
}
EOF

## GTK settings

## GTK3

GTK3=$HOME/.config/gtk-3.0
if [ ! -d "$GTK3" ]; then
  mkdir $GTK3
fi

if [ ! -f $GTK3/settings.ini ]; then
  cat > ~/.config/gtk-3.0/settings.ini << 'EOF'
[Settings]
gtk-enable-mnemonics = 0
gtk-modules = appmenu-gtk-module
gtk-shell-shows-app-menu = true
gtk-shell-shows-menubar = true
EOF
else
  cp $GTK3/settings.ini $GTK3/settings.bak
  if ! grep -q 'appmenu-gtk-module' "$GTK3/settings.ini" ; then
    echo 'gtk-modules = appmenu-gtk-module' >> $GTK3/settings.ini
  fi
  if ! grep -q 'gtk-enable-mnemonics' "$GTK3/settings.ini" ; then
    echo 'gtk-enable-mnemonics = 0' >> $GTK3/settings.ini
  fi
  if ! grep -q 'gtk-shell-shows-app-menu' "$GTK3/settings.ini" ; then
    echo 'gtk-shell-shows-app-menu = true' >> $GTK3/settings.ini
  fi
  if ! grep -q 'gtk-shell-shows-menubar' "$GTK3/settings.ini" ; then
    echo 'gtk-shell-shows-menubar = true' >> $GTK3/settings.ini
  fi
fi

## GTK2

GTK2=$HOME/.config/gtk-2.0
if [ ! -d "$GTK2" ]; then
  mkdir $GTK2
fi

if [ ! -f $GTK2/gtkrc ]; then
    cat > ~/.config/gtk-2.0/gtkrc << 'EOF'
gtk-enable-mnemonics = 0
gtk-modules = appmenu-gtk-module
EOF
else
  cp $GTK2/gtkrc $GTK2/gtkrc.bak
  if ! cat $GTK2/gtkrc | grep 'appmenu-gtk-module' ; then
    echo 'gtk-modules = appmenu-gtk-module' >> $GTK2/gtkrc
  fi
  if ! cat $GTK2/gtkrc | grep 'gtk-enable-mnemonics' ; then
    echo 'gtk-enable-mnemonics = 0' >> $GTK2/gtkrc
  fi
fi

## Nautilus
#[org/gnome/nautilus/list-view]
cat > ~/.config/dconf/MacUbuntu/nautilus-list-view.dconf << 'EOF'
[/]
default-column-order=['name', 'size', 'type', 'owner', 'group', 'permissions', 'where', 'date_modified', 'date_modified_with_time', 'date_accessed', 'recency', 'starred', 'detailed_type']
default-visible-columns=['name', 'size', 'type', 'date_modified', 'starred']
default-zoom-level='small'
use-tree-view=true
EOF

dconf load / < ~/.config/dconf/MacUbuntu/nautilus-list-view.dconf

# Nautilus Extensions

# Duplicate
wget https://github.com/M-Rick/MacUbuntu/raw/main/Nautilus/Duplicate-Nautilus.py -P ~/.local/share/nautilus-python/extensions/

# Link
wget https://github.com/M-Rick/MacUbuntu/raw/main/Nautilus/Link-Nautilus.py -P ~/.local/share/nautilus-python/extensions/

# Lock
wget https://github.com/M-Rick/MacUbuntu/raw/main/Nautilus/Lock-Nautilus.py -P ~/.local/share/nautilus-python/extensions/

# Labels
wget https://github.com/M-Rick/MacUbuntu/raw/main/Nautilus/Labels-Nautilus.py -P ~/.local/share/nautilus-python/extensions/


# Nemo Extensions

# Duplicate
wget https://github.com/M-Rick/MacUbuntu/raw/main/Nemo/Duplicate-Nemo.py -P ~/.local/share/nemo-python/extensions/

# Lock
wget https://github.com/M-Rick/MacUbuntu/raw/main/Nemo/Lock-Nemo.py -P ~/.local/share/nemo-python/extensions/

# Labels
wget https://github.com/M-Rick/MacUbuntu/raw/main/Nemo/Labels-Nemo.py -P ~/.local/share/nemo-python/extensions/



## Gnome Shell extensions

# Configure Blur My Shell
# [org/gnome/shell/extensions/blur-my-shell]
cat > ~/.config/dconf/MacUbuntu/blur-my-shell.dconf << 'EOF'
[/]
settings-version=2

[appfolder]
blur=false
brightness=0.6
sigma=30
style-dialogs=3

[coverflow-alt-tab]
pipeline='pipeline_default'

[dash-to-dock]
blur=false
brightness=0.6
override-background=false
pipeline='pipeline_default_rounded'
sigma=30
static-blur=true
style-dash-to-dock=0

[dash-to-panel]
blur-original-panel=true

[lockscreen]
pipeline='pipeline_default'

[overview]
blur=true
pipeline='pipeline_default'
style-components=1

[panel]
blur=false
brightness=0.6
override-background=true
pipeline='pipeline_default'
sigma=30
static-blur=false

[screenshot]
pipeline='pipeline_default'

[window-list]
blur=true
brightness=0.6
sigma=30
EOF

dconf load /org/gnome/shell/extensions/blur-my-shell/ < ~/.config/dconf/MacUbuntu/blur-my-shell.dconf

# Configure Just Perfection
# [org/gnome/shell/extensions/just-perfection]
cat > ~/.config/dconf/MacUbuntu/just-perfection.dconf << 'EOF'
[/]
clock-menu-position=0
clock-menu-position-offset=1
panel-button-padding-size=6
EOF

dconf load /org/gnome/shell/extensions/just-perfection/ < ~/.config/dconf/MacUbuntu/just-perfection.dconf


# Configure Pop Shell
# [org/gnome/shell/extensions/pop-shell]
cat > ~/.config/dconf/MacUbuntu/pop-shell.dconf << 'EOF'
[/]
active-hint-border-radius=uint32 0
gap-inner=uint32 1
gap-outer=uint32 1
show-title=true
tile-by-default=false
EOF

dconf load /org/gnome/shell/extensions/pop-shell/ < ~/.config/dconf/MacUbuntu/pop-shell.dconf


# Configure tray Icons Reloaded
# [org/gnome/shell/extensions/trayIconsReloaded]
cat > ~/.config/dconf/MacUbuntu/tray-icons-reloaded.dconf << 'EOF'
[/]
icon-size=22
icons-limit=0
tray-position='left'
EOF

dconf load /org/gnome/shell/extensions/trayIconsReloaded/ < ~/.config/dconf/MacUbuntu/tray-icons-reloaded.dconf


# Install Short Panel extension
echo "Installing Short Panel extension..."
if [ ! -f ~/.local/share/gnome-shell/extensions/short-panel@yourdomain.com/metadata.json ]; then
    wget https://github.com/M-Rick/short-panel/releases/download/v1.0.0/short-panel@yourdomain.com.zip -P ~/.config/dconf/MacUbuntu || {
        echo "Warning: Could not download Short Panel extension"
    }
    unzip -q ~/.config/dconf/MacUbuntu/short-panel@yourdomain.com.zip -d ~/.config/dconf/MacUbuntu/
    mv ~/.config/dconf/MacUbuntu/short-panel/short-panel@yourdomain.com ~/.local/share/gnome-shell/extensions/
fi

# Install Pop!_OS Window Tiling
echo "Installing Pop Shell extension..."
if [ ! -f ~/.local/share/gnome-shell/extensions/pop-shell@system76.com/metadata.json ]; then
    wget https://github.com/M-Rick/pop-shell/releases/download/v1.2.1/pop-shell@system76.com.zip -P ~/.config/dconf/MacUbuntu || {
        echo "Warning: Could not download Pop Shell extension"
    }
    unzip -q ~/.config/dconf/MacUbuntu/pop-shell@system76.com.zip -d ~/.config/dconf/MacUbuntu/
    mv ~/.config/dconf/MacUbuntu/pop-shell@system76.com ~/.local/share/gnome-shell/extensions/
fi

# Legacy (GTK3) Theme Scheme Auto Switcher
# https://extensions.gnome.org/extension/4998/legacy-gtk3-theme-scheme-auto-switcher/
echo "Installing Legacy (GTK3) Theme Scheme Auto Switcher extension..."
if [ -f ~/.local/share/gnome-shell/extensions/legacyschemeautoswitcher@joshimukul29.gmail.com/metadata.json ]; then
    rm -dR ~/.local/share/gnome-shell/extensions/legacyschemeautoswitcher@joshimukul29.gmail.com
fi
wget https://github.com/M-Rick/MacUbuntu/raw/main/Extensions/legacyschemeautoswitcher%40joshimukul29.gmail.com.zip -P ~/.config/dconf/MacUbuntu || {
echo "Warning: Could not download Legacy (GTK3) Theme Scheme Auto Switcher extension"
}
unzip -q ~/.config/dconf/MacUbuntu/legacyschemeautoswitcher@joshimukul29.gmail.com.zip -d ~/.config/dconf/MacUbuntu/
mv ~/.config/dconf/MacUbuntu/legacyschemeautoswitcher@joshimukul29.gmail.com ~/.local/share/gnome-shell/extensions/

# Tray Icons Reloaded
# https://extensions.gnome.org/extension/2890/tray-icons-reloaded/
echo "Installing Tray Icons Reloaded extension..."
gdbus call --session --dest org.gnome.Shell.Extensions --object-path /org/gnome/Shell/Extensions --method org.gnome.Shell.Extensions.InstallRemoteExtension "trayIconsReloaded@selfmade.pl" 2>/dev/null || {
    echo "Warning: Could not install Tray Icons Reloaded extension"
}

# App Hider
# https://extensions.gnome.org/extension/5895/app-hider/
echo "Installing App Hider extension..."
gdbus call --session --dest org.gnome.Shell.Extensions --object-path /org/gnome/Shell/Extensions --method org.gnome.Shell.Extensions.InstallRemoteExtension "app-hider@lynith.dev" 2>/dev/null || {
    echo "Warning: Could not install App Hider extension"
}

# Blur My Shell
# https://extensions.gnome.org/extension/3193/blur-my-shell/
echo "Installing Blur My Shell extension..."
gdbus call --session --dest org.gnome.Shell.Extensions --object-path /org/gnome/Shell/Extensions --method org.gnome.Shell.Extensions.InstallRemoteExtension "blur-my-shell@aunetx" 2>/dev/null || {
    echo "Warning: Could not install Blur My Shell extension"
}

# Just Perfection
# https://extensions.gnome.org/extension/3843/just-perfection/
echo "Installing Just Perfection extension..."
gdbus call --session --dest org.gnome.Shell.Extensions --object-path /org/gnome/Shell/Extensions --method org.gnome.Shell.Extensions.InstallRemoteExtension "just-perfection-desktop@just-perfection" 2>/dev/null || {
    echo "Warning: Could not install Just Perfection extension"
}

# Night Light Slider
# https://extensions.gnome.org/extension/7846/night-light-slider/
echo "Installing Night Light Slider extension..."
gdbus call --session --dest org.gnome.Shell.Extensions --object-path /org/gnome/Shell/Extensions --method org.gnome.Shell.Extensions.InstallRemoteExtension "night-light-slider@devoscarm.github.com" 2>/dev/null || {
    echo "Warning: Could not install Night Light Slider extension"
}

# Rounded Window Corners Reborn
# https://extensions.gnome.org/extension/7048/rounded-window-corners-reborn/
echo "Installing Rounded Window Corners Reborn extension..."
gdbus call --session --dest org.gnome.Shell.Extensions --object-path /org/gnome/Shell/Extensions --method org.gnome.Shell.Extensions.InstallRemoteExtension "rounded-window-corners@fxgn" 2>/dev/null || {
    echo "Warning: Could not install Rounded Window Corners Reborn extension"
}

# Install and configure Ding extension (desktop icons) if not on Ubuntu
if [ ! -f /etc/os-release ] || ! grep -q "Ubuntu" /etc/os-release; then
    echo "Installing Ding extension for desktop icons..."
    gdbus call --session --dest org.gnome.Shell.Extensions --object-path /org/gnome/Shell/Extensions --method org.gnome.Shell.Extensions.InstallRemoteExtension "ding@rastersoft.com" 2>/dev/null || {
    echo "Warning: Could not install Ding extension"
    }
    sleep 1
    gnome-extensions enable ding@rastersoft.com
fi

# Wait a moment for extensions to be processed
sleep 2

# Gnome Shell Extensions Activation
echo "Activating GNOME Shell extensions..."
gnome-extensions disable ubuntu-appindicators@ubuntu.com 2>/dev/null || true
gnome-extensions enable app-hider@lynith.dev 2>/dev/null || true
gnome-extensions enable blur-my-shell@aunetx 2>/dev/null || true
gnome-extensions enable just-perfection-desktop@just-perfection 2>/dev/null || true
gnome-extensions enable legacyschemeautoswitcher@joshimukul29.gmail.com 2>/dev/null || true
gnome-extensions enable night-light-slider@devoscarm.github.com 2>/dev/null || true
gnome-extensions enable pop-shell@system76.com 2>/dev/null || true
#gnome-extensions enable quick-settings-audio-panel@rayzeq.github.io 2>/dev/null || true
gnome-extensions enable rounded-window-corners@fxgn 2>/dev/null || true
gnome-extensions enable short-panel@yourdomain.com 2>/dev/null || true
gnome-extensions enable trayIconsReloaded@selfmade.pl 2>/dev/null || true


# Dconf setup

# MacUbuntu Overview
echo "Organizing applications in GNOME Overview..."
current_folders=$(dconf read /org/gnome/desktop/app-folders/folder-children)
if echo "$current_folders" | grep -q "'MacUbuntu'"; then
    echo "MacUbuntu folder already exists"
else
    if [ "$current_folders" = "@as []" ] || [ -z "$current_folders" ]; then
        new_folders="['MacUbuntu']"
    else
        new_folders=$(echo "$current_folders" | sed "s/]/, 'MacUbuntu']/")
    fi
    dconf write /org/gnome/desktop/app-folders/folder-children "$new_folders"
fi

dconf write /org/gnome/desktop/app-folders/folders/MacUbuntu/name "'MacUbuntu'"
dconf write /org/gnome/desktop/app-folders/folders/MacUbuntu/apps "['about.desktop', 'settings.desktop', 'update.desktop', 'appcenter.desktop', 'softwares.desktop', 'terminal.desktop', 'monitor.desktop', 'suspend.desktop', 'reboot.desktop', 'shutdown.desktop', 'lock.desktop', 'logout.desktop']"
dconf write /org/gnome/desktop/app-folders/folders/MacUbuntu/translate false


# App Hider
echo "Configuring App Hider to hide MacUbuntu elements..."
# Read existing hidden apps (in case extension was already installed)
existing_hidden=$(dconf read /org/gnome/shell/extensions/app-hider/hidden-apps 2>/dev/null || echo "@as []")
# Create new list with MacUbuntu elements
if [ "$existing_hidden" = "@as []" ] || [ -z "$existing_hidden" ]; then
    # No existing hidden apps
    new_hidden="['MacUbuntu', 'about.desktop', 'settings.desktop', 'update.desktop', 'appcenter.desktop', 'softwares.desktop', 'terminal.desktop', 'monitor.desktop', 'suspend.desktop', 'reboot.desktop', 'shutdown.desktop', 'lock.desktop', 'logout.desktop']"
else
    # Add to existing list (remove closing bracket, add our items)
    new_hidden=$(echo "$existing_hidden" | sed "s/]/, 'MacUbuntu', 'about.desktop', 'settings.desktop', 'update.desktop', 'appcenter.desktop', 'softwares.desktop', 'terminal.desktop', 'monitor.desktop', 'suspend.desktop', 'reboot.desktop', 'shutdown.desktop', 'lock.desktop', 'logout.desktop']/")
fi
# Apply the configuration
dconf write /org/gnome/shell/extensions/app-hider/hidden-apps "$new_hidden"


# Just Perfection
#gsettings set org.gnome.shell.extensions.just-perfection panel-icon-size 16

# Ding
if gnome-extensions list | grep -q "ding@"; then
    gsettings set org.gnome.shell.extensions.ding start-corner 'top-right'
    gsettings set org.gnome.shell.extensions.ding arrangeorder 'KIND'
fi

# Configure Flatpak for global menu support (if Flatpak is installed)
if command -v flatpak >/dev/null 2>&1; then
    echo "Configuring Flatpak for global menu support..."
    flatpak override --user --talk-name=com.canonical.AppMenu.Registrar
fi

# Set environment variables for global menu
echo "Setting up environment variables..."
if ! grep -q "export GTK_MODULES" ~/.bashrc; then
    echo "export GTK_MODULES=\${GTK_MODULES:+\$GTK_MODULES:}appmenu-gtk-module" >> ~/.bashrc
fi

if ! grep -q "export UBUNTU_MENUPROXY" ~/.bashrc; then
    echo "export UBUNTU_MENUPROXY=1" >> ~/.bashrc
fi

update-icon-caches ~/.local/share/icons/Yaru
chmod +x ~/.local/share/applications/*.desktop
update-desktop-database ~/.local/share/applications/

rm -f ~/.config/dconf/MacUbuntu/*.zip

echo ""
echo "==================================================="
echo "MacUbuntu configuration completed successfully!"
echo "==================================================="
echo ""
echo "Next steps:"
echo "1. Log out and log back in (or restart your session)"
echo "2. Press Alt+F2, type 'r', and press Enter to restart GNOME Shell"
echo "3. Check that XFCE4 panel starts automatically"
echo "4. Manually install any extensions that failed via GNOME Extensions website"
echo ""
echo "Note: Some extensions may require manual installation from:"
echo "https://extensions.gnome.org"
echo ""
echo "Enjoy your macOS-style Ubuntu desktop!"
echo ""
