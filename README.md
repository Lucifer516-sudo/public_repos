# public_repos
# timer.py
## To install this program on termux:
## Requirements:
* Termux app 
* Termux-api app( plugin)
## Note download the above from the f-droid store using the below link:
* [Termux App](https://f-droid.org/repo/com.termux_118.apk)
* [Termux-api Plugin](https://f-droid.org/repo/com.termux.api_51.apk)

## On Termux:
* Install `termux-api` package , `python`, `wget` using the below command .Just copy and paste it on the terminal 
```
termux-setup-storage 
apt update -y && apt upgrade -y 
apt install termux-api python wget -y 
```
* Now download the program script using wget package and install the necessary modules , and yes there are better ways to do this , we can use pipx though... now , copy and paste the code below...
```
wget https://raw.githubusercontent.com/Lucifer516-sudo/public_repos/release/timer.py
pip install typer[all]
cp timer.py ~/usr/bin/data/data/com.termux/files/usr/bin/timer

```
* now run it 
```
timer 1 --format ms # timer for 1minute in the format  min& seconds 
```
yeah done ...
