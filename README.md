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
     > 添加 ``"enable_heartbeat": true ``项
     >
     > 修改 ``use_ws_reverse``项为``true``
     >
     > 修改 ``ws_reverse_url`` 项为 ``ws://127.0.0.1:8080/ws/``
     >
     > 修改 ``ws_reverse_api_url`` 项为 ``ws://127.0.0.1:8080/ws/api/``
     >
     > 修改 ``ws_reverse_event_url`` 项为``ws://127.0.0.1:8080/ws/event/``

### 文件结构

- QQMakeGrassBot

  - bot

    > 主文件，用于启动bot

  - config

    > 参数设置文件

  - datas

    > 数据文件夹，存放数据文件

    - QQ_Group_List	

      > 每行一个，表示需要监控的qq群号

    - UID_List

      > 每行以逗号分隔，对应 *QQ_Group_List* 每一行群所监控的uid列表

    - UID_Name_Dict

      > 每行以逗号分隔，为uid和对应的自定义名称(昵称)

  - dynamics

    > 临时文件夹，运行时生成的临时文件，用于标记动态更新

  - plugins

    > 插件文件夹，存放自定义插件

    - weather

      > 天气查询

### 开发进度

待补充