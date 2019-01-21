
# 图片验证码redis有效期，单位秒
IMAGE_CODE_REDIS_EXPIRES = 5 * 60

# 短信验证码有效期，单位分钟
SMS_CODE_REDIS_EXPIRES = 5 * 60

# 发送间隔
SEND_SMS_CODE_INTERVAL = 60

# 短信发送模板
SMS_CODE_TEMP_ID = 1

# 短信验证码位数
SMS_CODE_NUMS = 6

# 用户session信息过期时间，单位秒，这是设置为5天
USER_SESSION_EXPIRES = 5 * 24 * 60 * 60