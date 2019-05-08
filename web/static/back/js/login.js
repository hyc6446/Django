
layui.use(['laypage', 'layedit','jquery','form','carousel'], function(){
  var   $ = layui.jquery,
        laypage = layui.laypage
        form = layui.form,
        carousel = layui.carousel
        layedit = layui.layedit;

	// 背景图片轮播
	carousel.render({
		elem: '#login_carousel',
		width: '100%',
		height: '100%',
		interval: 4000,
		arrow: 'none',
		anim: 'fade',
		indicator: 'none'
	});

	// 验证码值存储变量
	//var vailCode;
	// 执行获取验证码
	//refCode();

	// 点击刷新验证码
	$("#refCode_login_img").on("click", function() {
		//refCode();
	});

	// 获取验证码
//	function refCode() {
//		$.ajax({
//			url: "user/imageVailCode.do",
//			type: "post",
//			success: function(result) {
//				vailCode = result.data.rand;
//				$("#refCode_login_img").prop("src", "data:image/jpg;base64," + result.data.image);
//				$("#code").val("");
//			}
//		});
//	}

	// 自定义验证规则
	form.verify({
          account: function(value){ //value：表单的值、
            if(!new RegExp("^[a-zA-Z][a-zA-Z0-9_]{4,15}$").test(value)){
              return '管理员名称须已字母开头，允许5-16位字符，允许字母数字下划线';
            }
          }
        ,password: [/(.+){6,12}$/, '密码必须6到12位']
		,code: function(value) {
			if(value.toUpperCase() != vailCode) {
				refCode();
				return "验证码不正确";
			}
		}
	});

	//监听提交  
	form.on("submit(login)", function() {
		$.ajax({
			url: "/admin/login.html",
			type: "POST",
			data: {
				"account": $("#account").val(),
				"password": $("#password").val()
			},
			success: function(result) {
				if(result.code == 1) {
				    layer.msg(result.msg, {time: 1000, icon:6,offset: '20px',anim: 6},function(){
					    location = result.href;
				    });
				} else {
//					refCode();
					$("#password").val("");
				    layer.msg(result.msg, {time: 1000, icon:5,offset: '20px',anim: 6});
				}
			}
		});

		return false;
	});

})