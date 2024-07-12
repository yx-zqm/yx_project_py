> 离线安装和下载 
pip debug --verbose
>
```
pip download -d ./utility/pip_windows/  --python-version 3.8 --platform win32 -r requirements.txt -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com --only-binary=:all:
pip download -d ./utility/pip_windows/ -r requirements.txt -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com 

pip install --no-index --find-links=D:\weixili\ais\autorpt\utility\pip_linux -r requirements.txt
```