# Posting pictures to VK group
This script will help you to post random comic of [this comics]('https://xkcd.com) to the choosed group.

Also in the `main function` you have to add `group ID` of the group you want it to be posted(you have to be a member of that group)  
and `your user ID`

```python
vk_group_id = 'group ID'  
user_id = 'user ID'
```

## How to install
`Python3` should be already installed. Then use pip (or pip3, if there is a conflict with `Python2`) to install dependencies:   

```
pip install -r requirements.txt
```  
## setting up .env variables   
  You will  have to set your environment variables up, with `.env` file where you going to store
  your `VK_SERVICE_TOKEN`
  
[About VK Service Token](https://vk.com/dev/access_token?f=3.%20Сервисный%20ключ%20доступа)  



 You can use [Notepad++](https://notepad-plus-plus.org/downloads/) to create `.env` file for Windows,
or [CotEditor](https://coteditor.com/) for MacOS.
  
##### This is an example of how it looks like inside of your .env file. 
(You can choose your own variable names if you want)  
```
VK_SERVICE_TOKEN=Your_ServiceToken
```

Variables has to be with CAPITAL letters and without any spaces at all!  

### Project Goals  
To make life easier
 
