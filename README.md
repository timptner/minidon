# Raspberry Pi Display

## Development

For a rapid development with quick feedback loops it is recommended to set up a remote server in PyCharm.
Create a new sftp connection under `Settings > Build, Exec., Depl. > Deployment`.
Don't forget to also configure the correct local/remote folder mapping.

When successfully configured you can sync files via upload/download under `Tools > Deployment` (or right click menu).

To test your changes create a new remote session (`View > Tool Windows > Terminal > New Predefined Session`).

Create a virtual environment and install required packages.
You also need to install `spidev`, which is only possible on development boards.

```shell
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt
python3 -m pip install --upgrade --force-reinstall spidev 
```

If the display is already in use on the remote board you need to stop the running service.

```shell
sudo systemctl stop stats.service
```

Don't forget to start it afterwards. A Reboot will also start the service again.
