-- Rime Lua 扩展 https://github.com/hchunhui/librime-lua
-- 文档 https://github.com/hchunhui/librime-lua/wiki/Scripting

-- v 模式 symbols 优先（全拼）
v_filter = require("v_filter")

-- 长词优先（全拼）
long_word_filter = require("long_word_filter")

-- 降低部分英语单词在候选项的位置
-- 可在方案中配置要降低的单词
reduce_english_filter = require("reduce_english_filter")

-- 以词定字
-- 可在 default.yaml key_binder 下配置快捷键，默认为左右中括号 [ ]
select_character = require("select_character")

-- 日期时间
-- 可在方案中配置触发关键字。
date_translator = require("date_translator")

-- Unicode，U 开头
unicode = require("unicode")

-- 数字、人民币大写，R 开头
number_translator = require("number_translator")





-- 默认未启用：

-- 九宫格，手机用。
-- 在 engine/filters 增加 - lua_filter@t9_preedit
t9_preedit = require("t9_preedit")

-- 根据是否在用户词典，在结尾加上一个星号 *
-- 在 engine/filters 增加 - lua_filter@is_in_user_dict
-- 在方案里写配置项：
-- is_in_user_dict: true     为输入过的内容加星号
-- is_in_user_dict: flase    为未输入过的内容加星号
is_in_user_dict = require("is_in_user_dict")

-- 词条隐藏、降频
-- 在 engine/processors 增加 - lua_processor@cold_word_drop_processor
-- 在 engine/filters 增加 - lua_filter@cold_word_drop_filter
-- 在 key_binder 增加快捷键：
-- turn_down_cand: "Control+j"  # 匹配当前输入码后隐藏指定的候选字词 或候选词条放到第四候选位置
-- drop_cand: "Control+d"       # 强制删词, 无视输入的编码
cold_word_drop_processor = require("cold_word_drop.processor")
cold_word_drop_filter = require("cold_word_drop.filter")
