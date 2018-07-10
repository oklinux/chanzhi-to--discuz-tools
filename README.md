/*
 * @Author: wjsaya(www.wjsaya.top) 
 * @Date: 2018-07-10 11:48:35 
 * @Last Modified by:   wjsaya(www.wjsaya.top) 
 * @Last Modified time: 2018-07-10 11:48:35 
 */
# 项目地址:
https://github.com/wjsaya/chanzhi2discuz  

# 说明
./main.py为程序主入口  
./conf/config.py, 记录全局配置项  
./log/cz2discuz.log为日志文件  
./lib/chanzhi_class.py为蝉知类, 定义和数据库交互的方法  
./lib/process_XXX.py说明见下表, 都是迁移的功能定义  

# 文件结构解释
文件|说明|状态
--|--|--
config.py|环境配置|完成
chanzhi_class.py|工具类|完成
process_user.py|用户迁移|完成
process_forum.py|板块转移|完成
process_thread.py|帖子迁移|完成
process_reply.py|跟帖迁移|完成
