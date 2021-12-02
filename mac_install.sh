# Install bmmcli on Mac.
app_name="bmmcli"
echo "Downloading zipped $app_name"
echo "please enter your root password:"
sudo curl -s "" -o "/tmp/$app_name.zip"
echo "Extracting $app_name to bin folder"
sudo unzip -o "/tmp/$app_name.zip" -d /usr/local/bin/
me=$(whoami)
echo "Downloading default config file $app_name"
sudo curl -s "" -o "/Users/$me/bmm_config"