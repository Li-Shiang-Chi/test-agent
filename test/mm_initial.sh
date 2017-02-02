sudo service master_monitord restart
sudo mmsh addshelf s1 127.0.0.1
sudo mmsh addhost h2 192.168.1.22 86 s1
sudo mmsh addhost h1 192.168.1.21 88 s1
