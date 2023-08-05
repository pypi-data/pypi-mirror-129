# cloud_time_saver

cloud_time_saver is a python command-line application, that lets us control our AWS environment automatically without leaving the terminal.
It is designed to be used only on the Linux operating system.

# Introduction

The goal of this application is to speed up and simplify working with AWS and thus save users a lot of time.

In addition, it personally never suited me to use the AWS CLI, so I decided to do something similar, only my application was adapted for easier understanding and use.

# Installation steps

## Preinstallation 
Before installation please make sure that you have python3 installed.

After that one more thing. For this program to work you must have AWS account configured on your system.
If you do not have a configured account, you must first install AWS CLI.
Then create a new user in the AWS console. When done, run the AWS configure command and add credentials for the created user to it.
On Ubuntu OS that should look similar to this:
```bash
 /* installing AWS CLI */

 sudo apt-get install awscli

 /* now create new user in AWS Console */

 /* running aws configure will prompt you for user credentials */

 aws configure
```
 <sub><sup>If you get errors when running application regarding to your AWS User settings, you can run: pip3 install --upgrade awscli</sup></sub>

## Installation
Now when we are done with configuring our account we can install cloud_time_saver with this command:
```bash
pip install cloud-time-saver
```
If you want to run the cloud_time_saver command globally you should consider adding the installation directory to your PATH variable.


# Options
When you run cloud_time_saver you will have 3 options to choose from:
1. run ( starts application )
2. help ( provides you with documentation )
3. exit ( exits application )

## help
I recommend running the help command first, and seeing what kind of commands we can run. At first glance, this app may be a bit confusing, but a good look at the documentation should resolve disagreements.
This is how the help page looks like:
![image1](https://raw.githubusercontent.com/JaSamLudiMoskri/cloud_time_saver_prod/main/Screenshot%202021-11-27%20141217.png)

![image2](https://raw.githubusercontent.com/JaSamLudiMoskri/cloud_time_saver_prod/main/Screenshot%202021-11-27%20141300.png)


 



