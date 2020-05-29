# QQMakeGrassBot
基于CoolQ和nonebot的简单qq群聊生草机器人

### 环境要求

1. 环境
   - python3
   - CoolQ Air/Pro

2. python模块
   - nonebot
   - requests
   - APScheduler
   - ujson
   - msgpack

3. 酷Q插件

   - HTTP API

     > 首次运行后生成默认配置
     >
     > 修改use_ws_reverse项为true
     >
     > 修改ws_reverse_api_url为``ws://127.0.0.1:8080/ws/api/``
     >
     > 修改ws_reverse_event_url为``ws://127.0.0.1:8080/ws/event/``

### 文件结构

- QQMakeGrassBot

  - data_files

    > **以下文件需要结尾留一行空行**

    - QQ_Group_List	

      > 每行一个，表示需要监控的qq群号

    - UID_List

      > 每行以逗号分隔，对应 *QQ_Group_List* 每一行群所监控的uid列表

    - UID_Name_Dict

      > 每行以逗号分隔，为uid和对应的自定义名称(昵称)

  - dynamic_files

    > 运行时生成的临时文件，用于标记动态更新

### 开发进度

待补充