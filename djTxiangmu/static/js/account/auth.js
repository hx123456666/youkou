$(function(){
  let $loginBtn = $(".login-btn");
  $loginBtn.click(function () {
    // 验证会做两层 前端防止频繁的发送请求
    let telVal = $("input[name=telephone]").val();
    let pwdVal = $("input[name=password]").val();
    let remember = $("input[name=remember]");
    // console.log(`${telVal}, ${pwdVal}`)
    if(telVal && pwdVal){
       $.ajax({
      url: "/account/login/",
      method: "post",
      data: {
        "telephone": telVal,
        "password": pwdVal,
      },
      dataType: "json",
      success: res=>{
        // console.log('success');
        console.log(res);
        if(res["code"]===2){
          message.showSuccess("登录成功");
          setTimeout(()=>{
              window.location.href = '/';
          }, 2500)
        }else{
          message.showError(res["msg"]);
        }
      },
      error: err=>{
        // // 当 ajax 出现问题的时候 返回
        // console.log('error');
        // console.log(err);
        logError(err);
      }
      })
    }else {
      message.showError("手机号和密码不能为空");
    }

  });
});