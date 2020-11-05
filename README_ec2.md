*WARNING: This is a quick and dirty - with the emphasis on dirty - method to get
this running on an EC2 server. This is not scalable*

#How to set up an API server on EC2

1. Create an EC2 server, with sufficient (1GB + 2GB swap recommended per worker) memory
2. Download your .pem file, and use ssh-agent to add it to your identity
```
$ eval $(ssh-agent)
$ ssh-add /path/to/file.pem
```
3. SSH to your EC2 server. Install nginx and gunicorn
```
cd /home/ec2-user
sudo yum install python3
python3 -m venv venv3
source venv3/bin/activate
pip install gunicorn
sudo amazon-linux-extras enable nginx1.12 (or whatever version is available)
sudo yum install nginx1.12
```
4. Use this method to create and initialize a bare git repo and `/var/www/sanskrit_parser`
Ref: https://toroid.org/git-website-howto
```
$ cd /home/ec2-user
$ mkdir sanskrit_parser.git && cd sanskrit_parser.git
$ git init --bare
$ sudo mkdir -p /var/www/sanskrit_parser
$ sudo chown ec2-user /var/www/sanskrit_parser
$ cat > hooks/post-receive
#!/bin/sh
GIT_WORK_TREE=/var/www/sanskrit_parser git checkout -f
$ chmod +x hooks/post-receive
```
5. Exit ssh
6. In your local machine, cd to your git repo for `sanskrit_parser`, then
```
$ git remote add web ssh://your.ec2.server.name/home/ec2-user/sanskrit_parser.git
```
7. Now you can push to the remote repo with
```
$ git push web
```
8. SSH back to your ec2 server and check for files available in `/var/www/sanskrit_parser`. Install python libraries. Check in setup.py and install all libraries needed through pip. Manually test that the server will start using
```
$ cd /var/www/sanskrit_parser/sanskrit_parser/rest_api/
$ /home/ec2-user/venv3/bin/python run.py
```
If the server doesn't start, install any packages it asks for. Test it with a few curl commands, then stop it.
$ Edit nginx.conf to add your server name
```
$ nano /var/www/sanskrit_parser/web/nginx.conf
```
Replace the name "sktparserapi.madathil.org" with your server name. (Only if you're
running a secondary service, not the default one)

Under the TLS section, replace the certificate and the private key with one that you have
generated. You can generate a self-certified key for testing, but we recommend generating
a proper key using letsencrypt.org. This is if you want to enable https. If not, comment out this
section. Beware that most browsers will not let you use this api with mixed https/http. Not enabling
https means the UI must be served from an http (not https) server as well. 

Edit `/var/www/sanskrit_parser/web/sanskrit_parser.service` to increase the
number of workers if desired
10. Copy config files
```
$ mkdir /var/www/sanskrit_parser/sanskrit_parser/rest_api/static
$ sudo cp /var/www/sanskrit_parser/web/nginx.conf /etc/nginx/
$ sudo cp /var/www/sanskrit_parser/web/sanskrit_parser.service /lib/systemd/system/
$ sudo systemctl daemon-reload
$ sudo systemctl restart nginx
$ sudo systemctl start sanskrit_parser
$ sudo systemclt status sanskrit_parser
```
Check if things are ok
Now you should be good to. This instance is running nginx and gunicorn, and will
respond to api queries on the address configured in nginx.conf.
Check it out by running the following command
```
$ curl https://<server name>/sanskrit_parser/v1/tags/rAmaH
``
