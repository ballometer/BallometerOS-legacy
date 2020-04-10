# Ansible

With ansible we can automate the software installation and configuration on the pi.

## Usage

First create a file in this folder called ```inventory``` on your host computer (I use windows subsystem for linux) and add the following content

```ini
[ballometer]
ballometer1 ansible_host=your-ballometer-ip-address
```

Then create a file in this folder called ```secrets.yml``` and put the credentials for the online service in it:

```yml
username: "my-secret-username"
password: "my-secret-password"
```

Now you can run the playbook ```ballometer.yml``` against your pi with 

```bash
$ ansible-playbook -i inventory ballometer.yml
```

To run only parts of the installation, use

```bash
$ ansible-playbook -i inventory ballometer.yml --tags "tag-name"
```
