#mysql所在主机ip
HOSTNAME = '127.0.0.1'
#mysql监听的端口号，默认3306
PORT = 3306
#连接mysql的用户名（自己的）
USERNAME = 'root'
#连接mysql的密码（自己的）
PASSWORD = '123456'
#mysql上的数据库名称(需要先创建完成)
DATABASE = 'web_learn'
#app.config中配置flask连接数据库配置
SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4'

MAIL_SERVER = "smtp.qq.com"
MAIL_USE_SSL = True
MAIL_PORT = "465"
MAIL_USERNAME = "2893385008@qq.com"
MAIL_PASSWORD = "elpyxjdigqgbdhce" #授权码不是qq密码
MAIL_DEFAULT_SENDER = "2893385008@qq.com"

SECRET_KEY = 'DAFDSFSDGGdfafdasfd'
