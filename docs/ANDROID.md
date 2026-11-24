# Android prototype acceptance

Use current Termux with Python 3.11 or newer and Git. Keep the checkout and database in Termux private storage, not shared Downloads. No APK is provided.

```sh
pkg install python git -y
git clone --branch omega/verification-005 https://github.com/shiyamprimetrade-sketch/S-Omega.git ~/S-Omega
cd ~/S-Omega
python -m unittest discover -s tests -v
python acceptance.py
```

Expected: successful unit suite and eight true acceptance results. Record Python version, git rev-parse HEAD and both command outputs. Physical Android execution is not yet verified. The demo uses disposable data and a random ephemeral key; it never executes the inspected artifact. Do not reuse production secrets or databases.
