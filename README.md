# 说明
./main.py为程序主入口  
./conf/config.py, 记录全局配置项  
./log/cz2discuz.log为日志文件  
./lib/chanzhi_class.py为蝉知类, 定义和数据库交互的方法  
./lib/process_XXX.py说明见下表, 都是迁移的功能定义  
./process_htmlbbcode.py是转换帖子正文中html代码为bbcode的功能实现


# 文件结构解释
文件|说明|状态
--|--|--
config.py|环境配置|完成
chanzhi_class.py|工具类|完成
process_user.py|用户迁移|完成
process_forum.py|板块转移|完成
process_thread.py|帖子迁移|完成
process_reply.py|跟帖迁移|完成
process_blog.py|博客迁移|完成
process_article.py|文章迁移|完成
process_htmlbbcode.py|html到bbcode转码|完成



# 文章解析
蝉知  
1, 在eps_article插入文章标题, 内容, 关键词, 发布者等信息  
2, 从eps_category获取文章分类的id  
3, 把分类id, 文章id, 文章类别插入eps_relation表  



discuz  
1, 添加新的分类, 类名, 类id等添加到pre_portal_category表   
2, 文章标题作者信息写入pre_portal_article_title表  
3, 文章正文内容写入pre_portal_article_content表  
[4, 把新分类的地址添加到导航栏, 加入pre_common_nav表  这一步不是发布文章必选项]  


