function bindEmailCaptchaClick() {
  $("#captcha-btn").click(function (event) {
      // this: 代表当前按钮的 jQuery 对象,也就是html中这个按钮
      var $this = $(this);
      // 阻止默认的事件(防止form中获取验证码按钮提交整个表单)
      event.preventDefault();

      //获取input邮箱的值
      var email = $("input[name='email']").val();
      //应用ajax来实现异步传输
      $.ajax({
          //配置请求url，可以加ip和端口号也可以不加（默认是当前域名下）
          url: "/auth/captcha/email?email=" + email,
          //配置请求方法：get、post，与路由中app.route("/auth/captcha/email",method=["POST"])对应
          //一般从服务器上取数据用get，向服务器提交数据用post，具体情况还要具体分析
          method: "GET",
          //处理成功，返回数据result
          success: function (result) {
              var code = result['code'];
              if (code == 200) {
                  var countdown = 60;
                  // 开始倒计时之前，取消按钮的点击事件
                  $this.off("click");
                  //定义定时器setInterval（1000间隔时间后开始执行函数）
                  var timer = setInterval(function () {
                      //定义按钮上的文本为倒计时
                      $this.text(countdown);
                      countdown -= 1;
                      // 倒计时结束时执行
                      if (countdown <= 0) {
                          // 清除定时器
                          clearInterval(timer);
                          // 按钮文本恢复原样
                          $this.text("获取验证码");
                          // 重新绑定点击事件
                          bindEmailCaptchaClick();
                      }
                  }, 1000);
                   $("#success-message").text("邮箱验证码发送成功!").show();
                    setTimeout(function () {
                        $("#success-message").hide(); // 3秒后隐藏消息
                    }, 3000);
              } else {
                  alert(result['message']);
              }
          },
          error: function (error) { //失败返回
              console.log(error);
          }
      });
  });
}

// 整个网页加载完成后再执行
$(function () {
  bindEmailCaptchaClick();
});
