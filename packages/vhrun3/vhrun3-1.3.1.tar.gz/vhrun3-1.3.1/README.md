
#### 介绍

基于httprunner==3.1.6版本，根据特定需求二次定制开发

##### 更新日志:
###### 1.0.1
- 1、保留2.x版本的用例分层机制，避免冗余出现api基本信息（url、headers、method等）
- 2、除支持http和https协议外，支持SSH协议，可以远程执行shell命令、文件上传和下载
- 3、兼容支持2.x测试报告，便于测试时调试
- 4、数据驱动改成一个Class N个test_*用例方式，便于用例扫描成独立用例
- 5、支持test_xx的__doc__自动生成，并支持config.variables和parameters变量解析
- 6、yml中config中usefixtures字段，支持pytest指定添加fixture
###### 1.1.3
- 7、支持特定场景下的skipif代码生成
###### 1.1.6
- 8、allure报告增加详细步骤信息
###### 1.1.9
- 9、支持testcse级别的setup和teardown
###### 1.2.0
- 10、Testcae和TestStep支持skipIf
###### 1.2.1
- 11、allure报告中显示Method和url
- 12、修复setup_hooks/teardown_hooks使用$request和$response出现的问题
- 13、支持api中variables与teststep中variables进行合并
- 14、setup_hooks/teardown_hooks中返回的变量可以之后的teststep所使用
###### 1.2.2
- 15、setup_hooks/teardown_hooks中返回的变量显示在allure报告的extract_values中
- 16、支持循环执行teststep直到达到目标条件或超时退出
###### 1.2.3
- 17、循环增强：支持loop_for和loop_while
- 18、环境变量带上进程号+线程号，避免pytest在使用并发插件时出现混乱
###### 1.2.4
- 19、修复v1.2.3中的bug
###### 1.2.5
- 20、teradown_hooks的执行放于extract之后，以便teardown_hooks可以使用extract后的变量
###### 1.2.6
- 21、loop_for支持递归嵌套
###### 1.2.7
- 22、修复allure.step中因“{}”.format引起的错误
###### 1.2.8
- 23、allure中的用例名称支持变量解析
###### 1.3.1
- 24、日志和allure报告添加validate描述
- 25、parameter生成支持变量解析，修复单个字段时值不能为list的bug
- 26、allure报告的validate_list优化
- 27、allure报告增加setup_hooks和teardown_hooks详情
#### 新增SSH部分示例：
###### 1、执行shell命令
```
config:
  name: demo - exec shell cmd
  variables:
    executor: ls
    params: -alh
teststeps:
  - name: api -> shell
    protocol: ssh
    connection:   # 指定目标机器IP、Port、User和Password
      ssh_ip: ${ENV(hostname)}  
      ssh_port: ${ENV(ssh_port)}
      ssh_user: ${ENV(ssh_user)}
      ssh_password: ${ENV(ssh_password)}
    request:
      type: shell   # 指定类型为执行Shell命令
      executor: $executor  # shell自带命令或可执行程序
      params: $params # 字符串或字符串列表
```
###### 2、文件上传
```
config:
  name: demo - upload file
teststeps:
  - name: api -> upload
    protocol: ssh
    connection:
      ssh_ip: ${ENV(hostname)}
      ssh_port: ${ENV(ssh_port)}
      ssh_user: ${ENV(ssh_user)}
      ssh_password: ${ENV(ssh_password)}
    request:
        type: upload # 指定类型为文件上传
        local_path: $local_path  # 相对于本项目根目录的路径
        remote_path: $remote_path  # 远程绝对路径
```

###### 3、文件下载
```
config:
  name: demo - download file
teststeps:
  - name: api -> download
    protocol: ssh
    connection:
      ssh_ip: ${ENV(hostname)}
      ssh_port: ${ENV(ssh_port)}
      ssh_user: ${ENV(ssh_user)}
      ssh_password: ${ENV(ssh_password)}
    request:
        type: download # 指定类型为文件下载
        local_path: $local_path  # 相对于本项目根目录的路径
        remote_path: $remote_path  # 远程绝对路径
```
#### 参考：
```
homepage = "https://github.com/httprunner/httprunner"
repository = "https://github.com/httprunner/httprunner"
documentation = "https://docs.httprunner.org"
blog = "https://debugtalk.com/
```
