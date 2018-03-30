# login 逻辑
flask 可以通过 flask_login 来完成 用户登陆 限制登陆页面 用户跳转 用户展示 用户注册的功能

基础工作

# 1 登录逻辑 current_user login_user

如果当前用户  current_user.is_authorized == ture 跳转到首页
显示登录页面

登陆 post callback
通过 username 查询用户
用户不存或者用户密码不匹配，显示错误信息，继续登录
login_user

# 2 显示当前登录用户
current_user.username

# 3 方法要求登录，所以访问这些页面的时候，需要跳转到登录页面，登陆完成之后在跳转回想要登陆的页面
注册登陆页面
对所有需要登陆的方法，增加@login_required decorator
分析后续跳转回来的逻辑，在登陆页面增加跳转逻辑

# 4 注册逻辑
注册form require equal email telephone
用户自定义 validator
创建用户

# 5 logout


# 需要首先 注入 flask_login ，关联 user_loader ，然后在用户里面添加UserMixin